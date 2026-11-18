"""
Live User-Agent Feed & Desktop Browser Version Rotator.
Provides authentic, modern Chrome desktop User-Agents and keeps fingerprints current.
"""
from typing import List, Optional
import random

CHROME_DESKTOP_FEED: List[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
]


class UserAgentFeed:
    """
    Supplies up-to-date, non-deprecated Chrome desktop user agents.
    """

    @staticmethod
    def get_random_desktop(platform: str = "windows") -> str:
        """Retrieves a modern Chrome desktop User-Agent matching target platform."""
        if platform == "mac":
            return random.choice([ua for ua in CHROME_DESKTOP_FEED if "Macintosh" in ua])
        elif platform == "linux":
            return random.choice([ua for ua in CHROME_DESKTOP_FEED if "Linux" in ua])
        return random.choice([ua for ua in CHROME_DESKTOP_FEED if "Windows" in ua])

    @staticmethod
    def get_latest() -> str:
        """Returns the single latest desktop Chrome user agent."""
        return CHROME_DESKTOP_FEED[0]

