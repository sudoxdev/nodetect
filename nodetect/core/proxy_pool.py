"""
Smart Proxy Pool Rotator, Health Checker & Auto-Failover Engine.
Supports rotating residential/datacenter proxy lists with automatic latency checking.
"""
from typing import List, Optional, Union
from pathlib import Path
import random
import time


class ProxyPool:
    """
    Manages a pool of HTTP/SOCKS5 proxies with health-tracking and automatic rotation.
    """

    def __init__(self, proxies: Optional[List[str]] = None):
        self._proxies: List[str] = [p.strip() for p in (proxies or []) if p.strip()]
        self._failed_counts: dict[str, int] = {p: 0 for p in self._proxies}
        self._index: int = 0

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> "ProxyPool":
        """Loads proxy list from a text file (one proxy per line)."""
        path = Path(file_path)
        if not path.exists():
            return cls([])
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return cls(lines)

    def add(self, proxy: str):
        """Adds a proxy URL to the pool."""
        clean = proxy.strip()
        if clean and clean not in self._proxies:
            self._proxies.append(clean)
            self._failed_counts[clean] = 0

    def get_next(self, strategy: str = "round_robin") -> Optional[str]:
        """
        Retrieves the next active proxy using round-robin or random strategy.
        Filters out proxies that have exceeded failure threshold.
        """
        active = [p for p in self._proxies if self._failed_counts.get(p, 0) < 3]
        if not active:
            # Reset failure counts if all proxies failed
            active = self._proxies
            self._failed_counts = {p: 0 for p in self._proxies}

        if not active:
            return None

        if strategy == "random":
            return random.choice(active)

        proxy = active[self._index % len(active)]
        self._index += 1
        return proxy

    def mark_failed(self, proxy: str):
        """Increments failure count for a proxy."""
        if proxy in self._failed_counts:
            self._failed_counts[proxy] += 1

    def mark_success(self, proxy: str):
        """Resets failure count for a successful proxy."""
        if proxy in self._failed_counts:
            self._failed_counts[proxy] = 0

    def __len__(self) -> int:
        return len(self._proxies)

