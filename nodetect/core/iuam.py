"""
Cloudflare IUAM (Under Attack Mode) & 5-Second Challenge Auto-Pass Waiter.
Monitors DOM state and automatically resolves spinning verification shields.
"""
import asyncio
from typing import Any


class CloudflareIUAM:
    """
    Detects Cloudflare 5-second verification barriers and awaits redirection.
    """

    @staticmethod
    async def is_challenge_active(page: Any) -> bool:
        """Determines if the page is currently held on a Cloudflare challenge shield."""
        try:
            title = await page.title()
            if "just a moment" in title.lower():
                return True
            
            # Check for Cloudflare challenge identifiers
            is_cf = await page.evaluate("""
                () => {
                    return !!(
                        document.querySelector('#challenge-running') ||
                        document.querySelector('#challenge-stage') ||
                        document.querySelector('#cf-wrapper') ||
                        document.querySelector('.ray_id')
                    );
                }
            """)
            return is_cf
        except Exception:
            return False

    @staticmethod
    async def wait_for_clear(page: Any, timeout_sec: int = 25) -> bool:
        """
        Polls until the Cloudflare 'Just a moment...' barrier clears and the target page loads.
        Returns True if passed successfully, False if timed out.
        """
        start_time = asyncio.get_event_loop().time()

        # If not on a challenge screen, return immediately
        if not await CloudflareIUAM.is_challenge_active(page):
            return True

        while asyncio.get_event_loop().time() - start_time < timeout_sec:
            await asyncio.sleep(1)
            active = await CloudflareIUAM.is_challenge_active(page)
            if not active:
                # Small grace period for DOM stabilization after redirection
                await asyncio.sleep(1)
                return True

        return False

