"""
Persistent Profile & Session Manager for PhantomVault.
Manages isolated browser storage, cookies, proxy pairings, and hardware fingerprints via SQLite.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager
import json
import sqlite3
from typing import Optional, List, Dict, Any

from nodetect.config import DEFAULT_VAULT_DIR, DATABASE_PATH, PROFILES_DIR
from nodetect.profile.fingerprint import Fingerprint


@dataclass
class ProfileRecord:
    profile_id: str
    name: str
    fingerprint: Fingerprint
    proxy: Optional[str]
    storage_state: Optional[Dict[str, Any]]
    created_at: str
    last_used_at: str

    @property
    def user_data_dir(self) -> Path:
        """Returns the isolated Chromium user data directory for this profile."""
        path = PROFILES_DIR / self.profile_id / "browser_data"
        path.mkdir(parents=True, exist_ok=True)
        return path


class ProfileManager:
    """
    Coordinates creation, lifecycle, and disk persistence of anti-detect browser profiles.
    """

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_init()

    @contextmanager
    def _get_connection(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_init(self):
        """Initializes database schema if not present."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    profile_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    fingerprint_json TEXT NOT NULL,
                    proxy TEXT,
                    storage_state_json TEXT,
                    created_at TEXT NOT NULL,
                    last_used_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def create_profile(
        self,
        profile_id: str,
        name: Optional[str] = None,
        proxy: Optional[str] = None,
        platform_type: str = "windows",
        timezone_id: str = "America/New_York"
    ) -> ProfileRecord:
        """Creates and stores a new isolated profile with a deterministic hardware fingerprint."""
        now = datetime.now(timezone.utc).isoformat()
        display_name = name or f"Profile-{profile_id}"
        fp = Fingerprint.generate(profile_id=profile_id, platform_type=platform_type, timezone=timezone_id)

        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO profiles 
                (profile_id, name, fingerprint_json, proxy, storage_state_json, created_at, last_used_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                profile_id,
                display_name,
                json.dumps(fp.to_dict()),
                proxy,
                None,
                now,
                now
            ))
            conn.commit()

        record = self.get_profile(profile_id)
        assert record is not None
        # Ensure user data directory exists
        record.user_data_dir.mkdir(parents=True, exist_ok=True)
        return record

    def get_profile(self, profile_id: str) -> Optional[ProfileRecord]:
        """Loads profile and fingerprint record by profile_id."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT profile_id, name, fingerprint_json, proxy, storage_state_json, created_at, last_used_at
                FROM profiles WHERE profile_id = ?
            """, (profile_id,))
            row = cursor.fetchone()

        if not row:
            return None

        fp_dict = json.loads(row[2])
        fp = Fingerprint.from_dict(fp_dict)
        storage_state = json.loads(row[4]) if row[4] else None

        return ProfileRecord(
            profile_id=row[0],
            name=row[1],
            fingerprint=fp,
            proxy=row[3],
            storage_state=storage_state,
            created_at=row[5],
            last_used_at=row[6]
        )

    def list_profiles(self) -> List[ProfileRecord]:
        """Returns all registered profiles."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT profile_id, name, fingerprint_json, proxy, storage_state_json, created_at, last_used_at
                FROM profiles ORDER BY last_used_at DESC
            """)
            rows = cursor.fetchall()

        records: List[ProfileRecord] = []
        for r in rows:
            fp_dict = json.loads(r[2])
            fp = Fingerprint.from_dict(fp_dict)
            storage_state = json.loads(r[4]) if r[4] else None
            records.append(ProfileRecord(
                profile_id=r[0],
                name=r[1],
                fingerprint=fp,
                proxy=r[3],
                storage_state=storage_state,
                created_at=r[5],
                last_used_at=r[6]
            ))
        return records

    def save_session_state(self, profile_id: str, storage_state: Dict[str, Any]):
        """Persists Playwright storage state (cookies, origins, localStorage)."""
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE profiles 
                SET storage_state_json = ?, last_used_at = ?
                WHERE profile_id = ?
            """, (json.dumps(storage_state), now, profile_id))
            conn.commit()

    def touch_profile(self, profile_id: str):
        """Updates last used timestamp."""
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute("UPDATE profiles SET last_used_at = ? WHERE profile_id = ?", (now, profile_id))
            conn.commit()

    def delete_profile(self, profile_id: str):
        """Removes profile from database and wipes stored browser data."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM profiles WHERE profile_id = ?", (profile_id,))
            conn.commit()

        # Clean directory if exists
        profile_path = PROFILES_DIR / profile_id
        if profile_path.exists():
            import shutil
            shutil.rmtree(profile_path, ignore_errors=True)
