"""
nodetect - High-Performance Stealth Browser Automation & Persistent Profile Orchestrator
"""

__version__ = "1.0.1"

import sys
import warnings
from typing import Optional

# Suppress Windows asyncio proactor pipe deallocation artifact
warnings.filterwarnings("ignore", category=ResourceWarning)
if sys.platform == "win32":
    try:
        from asyncio.proactor_events import _ProactorBasePipeTransport
        _ProactorBasePipeTransport.__del__ = lambda self: None
    except Exception:
        pass

from nodetect.core.engine import StealthEngine, StealthSession
from nodetect.core.tls_session import TLSSession
from nodetect.core.humanizer import Humanizer
from nodetect.core.solver import TurnstileSolver
from nodetect.core.clearance import ClearanceHarvester
from nodetect.core.proxy_pool import ProxyPool
from nodetect.core.cookies import CookieVault
from nodetect.core.ua_feed import UserAgentFeed
from nodetect.core.iuam import CloudflareIUAM
from nodetect.profile.manager import ProfileManager, ProfileRecord
from nodetect.profile.fingerprint import Fingerprint
from nodetect.profile.harvester import Harvester


async def launch(
    profile_id: str = "default_profile",
    headless: bool = False,
    proxy: Optional[str] = None,
    proxy_pool: Optional[ProxyPool] = None,
    platform_type: str = "windows",
    turbo_mode: bool = False
) -> StealthSession:
    """
    Convenience one-liner function to initialize and launch an undetected browser instance.
    Supports proxy pools, automated stealth evasions, and persistent storage.

    Usage:
        import nodetect as pv
        session = await pv.launch()
        await session.page.goto("https://site.com")
        await session.close()
    """
    engine = StealthEngine()
    return await engine.launch(
        profile_id=profile_id,
        headless=headless,
        proxy=proxy,
        proxy_pool=proxy_pool,
        platform_type=platform_type,
        turbo_mode=turbo_mode
    )


__all__ = [
    "launch",
    "StealthEngine",
    "StealthSession",
    "TLSSession",
    "Humanizer",
    "TurnstileSolver",
    "ClearanceHarvester",
    "ProxyPool",
    "CookieVault",
    "UserAgentFeed",
    "CloudflareIUAM",
    "ProfileManager",
    "ProfileRecord",
    "Fingerprint",
    "Harvester"
]
