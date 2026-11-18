"""
High-Speed TLS & JA3/JA4 Impersonation Session Engine.
Wraps curl_cffi with realistic header generation and seamless Playwright cookie sync.
"""
from typing import Dict, Any, Optional, List
import json
from curl_cffi import requests

from nodetect.profile.fingerprint import Fingerprint


class TLSSession:
    """
    Ultra-fast HTTP client impersonating real modern Chrome TLS fingerprints (JA3/JA4, HTTP/2).
    Designed to continue scraping and API interactions without headless browser overhead.
    """

    def __init__(self, fingerprint: Optional[Fingerprint] = None, proxy: Optional[str] = None, impersonate: str = "chrome120"):
        self.fingerprint = fingerprint
        self.impersonate = impersonate
        self.proxy = proxy
        self.session = requests.Session(impersonate=self.impersonate)

        if self.proxy:
            self.session.proxies = {"http": self.proxy, "https": self.proxy}

        self._configure_default_headers()

    def _configure_default_headers(self):
        """Sets modern Chrome client hints and navigational headers."""
        ua = self.fingerprint.user_agent if self.fingerprint else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        platform = f'"{self.fingerprint.platform}"' if self.fingerprint else '"Windows"'

        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": platform,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }
        self.session.headers.update(headers)

    def import_playwright_cookies(self, cookies: List[Dict[str, Any]]):
        """Imports cookies directly from Playwright's context.cookies() list."""
        for c in cookies:
            self.session.cookies.set(
                name=c["name"],
                value=c["value"],
                domain=c.get("domain", ""),
                path=c.get("path", "/")
            )

    def export_cookies_dict(self) -> Dict[str, str]:
        """Returns cookies as simple key-value dictionary."""
        return self.session.cookies.get_dict()

    def get(self, url: str, **kwargs) -> requests.Response:
        """Perform stealth GET request matching Chrome JA3/JA4."""
        return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """Perform stealth POST request matching Chrome JA3/JA4."""
        return self.session.post(url, **kwargs)

    def close(self):
        """Close underlying connection pool."""
        self.session.close()

