"""
Cloudflare cf_clearance Cookie Harvester & High-Speed Scraping Bridge.
Inspired by request-level solvers like cfsolve, but combining DOM-resilience with TLS session handover.
"""
import asyncio
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

from nodetect.core.engine import StealthEngine
from nodetect.core.tls_session import TLSSession


class ClearanceHarvester:
    """
    Acquires Cloudflare cf_clearance cookies and Turnstile tokens,
    then automatically initializes a matching TLS session for high-speed requests.
    """

    @staticmethod
    async def acquire_clearance(
        url: str,
        profile_id: str = "cf_clearance_node",
        proxy: Optional[str] = None,
        timeout_sec: int = 35,
        headless: bool = False
    ) -> Tuple[Optional[str], Optional[TLSSession]]:
        """
        Navigates to a Cloudflare protected endpoint, solves IUAM / Turnstile challenges,
        extracts cf_clearance cookie, and returns an initialized TLSSession bound to the same IP/UA.
        """
        engine = StealthEngine()
        session = await engine.launch(profile_id=profile_id, proxy=proxy, headless=headless)
        page = session.page

        await page.goto(url, wait_until="domcontentloaded")

        # Check for Turnstile widget and auto-solve if present
        try:
            await session.solve_turnstile(timeout_sec=10)
        except Exception:
            pass

        start_time = asyncio.get_event_loop().time()
        clearance_token = None

        while asyncio.get_event_loop().time() - start_time < timeout_sec:
            cookies = await session.get_cookies()
            for c in cookies:
                if c["name"] == "cf_clearance":
                    clearance_token = c["value"]
                    break

            if clearance_token:
                break
            await asyncio.sleep(1)

        if not clearance_token:
            await session.close()
            return None, None

        # Build matched TLS session using exact same cookies, UA, and proxy
        tls_session = await session.export_to_tls_session()
        await session.close()

        return clearance_token, tls_session

