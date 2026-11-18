"""
Cookie Exporter & Importer Engine.
Supports EditThisCookie JSON format, Playwright storage state, and standard Netscape formats.
"""
from pathlib import Path
import json
from typing import List, Dict, Any, Union


class CookieVault:
    """
    Handles translation and disk persistence of cookies between browser contexts,
    EditThisCookie extensions, and cURL / Netscape cookie files.
    """

    @staticmethod
    def export_json(cookies: List[Dict[str, Any]], file_path: Union[str, Path]):
        """Exports cookies in standard EditThisCookie compatible JSON array."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2)

    @staticmethod
    def import_json(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Imports cookies from an EditThisCookie JSON file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Cookie file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def export_netscape(cookies: List[Dict[str, Any]], file_path: Union[str, Path]):
        """
        Exports cookies into standard Netscape HTTP Cookie File format (cURL, Wget compatible).
        Format: domain, flag, path, secure, expiration, name, value
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Netscape HTTP Cookie File",
            "# Exported by PhantomVault",
            ""
        ]
        for c in cookies:
            domain = c.get("domain", "")
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path_val = c.get("path", "/")
            secure = "TRUE" if c.get("secure", False) else "FALSE"
            expires = str(int(c.get("expires", 0))) if c.get("expires", 0) > 0 else "0"
            name = c.get("name", "")
            value = c.get("value", "")
            lines.append(f"{domain}\t{flag}\t{path_val}\t{secure}\t{expires}\t{name}\t{value}")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

