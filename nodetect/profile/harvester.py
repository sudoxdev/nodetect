"""
Real Browser Fingerprint Harvester & JSON Importer Engine.
Loads full hardware parameters (WebGL GLenums, precision tables, audio sums) from real browser captures.
"""
from pathlib import Path
import json
from typing import Dict, Any, Optional

from nodetect.profile.fingerprint import Fingerprint
from nodetect.profile.manager import ProfileManager, ProfileRecord


class Harvester:
    """
    Coordinates extraction of authentic consumer device fingerprints and imports them into PhantomVault.
    """

    @staticmethod
    def load_from_file(file_path: Path) -> Dict[str, Any]:
        """Loads and parses raw JSON exported from harvest-fp.html."""
        if not file_path.exists():
            raise FileNotFoundError(f"Harvested fingerprint file not found at: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def import_to_profile(
        profile_id: str,
        json_path: Path,
        name: Optional[str] = None,
        proxy: Optional[str] = None,
        manager: Optional[ProfileManager] = None
    ) -> ProfileRecord:
        """
        Converts a real-fp.json dump into a persistent ProfileRecord.
        """
        mgr = manager or ProfileManager()
        raw_data = Harvester.load_from_file(json_path)
        fp = Fingerprint.from_harvested_json(profile_id=profile_id, raw_json=raw_data)

        # Store into database
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        display_name = name or f"Harvested-{profile_id}"

        with mgr._get_connection() as conn:
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

        record = mgr.get_profile(profile_id)
        assert record is not None
        record.user_data_dir.mkdir(parents=True, exist_ok=True)
        return record

