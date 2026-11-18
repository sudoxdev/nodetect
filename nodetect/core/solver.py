"""
Cloudflare Turnstile & CAPTCHA Interactive Autonomous Solver & Token Harvester.
Detects Turnstile / Challenge iframes, shadow roots, automates humanized verification,
and extracts verified tokens for high-speed API scrapers.
"""
import asyncio
import random
from typing import Optional, Any
from nodetect.core.humanizer import Humanizer


class TurnstileSolver:
    """
    Automated resolver for Cloudflare Turnstile and interactive anti-bot checkboxes.
    """

    @staticmethod
    async def find_turnstile_box(page: Any) -> Optional[Any]:
        """Scans page for Cloudflare Turnstile iframes or widget containers."""
        # 1. Check active frames
        for frame in page.frames:
            if "challenges.cloudflare.com" in frame.url or "turnstile" in frame.url:
                try:
                    frame_elem = await frame.frame_element()
                    if frame_elem and await frame_elem.is_visible():
                        return frame_elem
                except Exception:
                    pass

        # 2. Check DOM selectors
        selectors = [
            'iframe[src*="challenges.cloudflare.com"]',
            'iframe[src*="turnstile"]',
            'iframe[title*="Cloudflare"]',
            'div[id*="cf-turnstile"] iframe',
            '.cf-turnstile iframe'
        ]
        for sel in selectors:
            try:
                frame_elem = await page.query_selector(sel)
                if frame_elem and await frame_elem.is_visible():
                    return frame_elem
            except Exception:
                pass
        return None

    @staticmethod
    async def solve_turnstile_async(page: Any, timeout_sec: int = 15) -> bool:
        """
        Locates Turnstile widget on page, organically glides cursor to checkbox,
        clicks it with human cadence, and awaits verified token.
        """
        start_time = asyncio.get_event_loop().time()

        # 1. Wait for widget iframe to become visible
        frame_element = None
        while asyncio.get_event_loop().time() - start_time < timeout_sec:
            frame_element = await TurnstileSolver.find_turnstile_box(page)
            if frame_element:
                break
            await asyncio.sleep(0.5)

        if not frame_element:
            return False

        # 2. Get frame bounding box
        box = await frame_element.bounding_box()
        if not box:
            return False

        # Target coordinates: Cloudflare Turnstile checkbox is near left edge of widget
        target_x = box["x"] + min(35.0, box["width"] * 0.15) + random.uniform(2, 8)
        target_y = box["y"] + (box["height"] / 2.0) + random.uniform(-3, 3)

        # 3. Organic mouse glide with deceleration
        await Humanizer.move_mouse_async(page, target_x, target_y, steps=25)
        await asyncio.sleep(random.uniform(0.1, 0.25))

        # 4. Human click
        await page.mouse.down()
        await asyncio.sleep(random.uniform(0.05, 0.12))
        await page.mouse.up()

        # 5. Await verification token population
        while asyncio.get_event_loop().time() - start_time < timeout_sec:
            token = await page.evaluate("""
                () => {
                    const el = document.querySelector('[name="cf-turnstile-response"]') || 
                               document.querySelector('input[name*="turnstile"]') ||
                               document.querySelector('#cf-chl-widget-');
                    return el && el.value && el.value.length > 10 ? el.value : null;
                }
            """)
            if token and len(token) > 20:
                return True
            await asyncio.sleep(0.5)

        return False

    @staticmethod
    async def harvest_token_async(page: Any, timeout_sec: int = 15) -> Optional[str]:
        """
        Solves Cloudflare Turnstile and extracts the verified token string.
        Useful for feeding tokens directly into high-throughput API requests.
        """
        success = await TurnstileSolver.solve_turnstile_async(page, timeout_sec=timeout_sec)
        if not success:
            return None

        token = await page.evaluate("""
            () => {
                const el = document.querySelector('[name="cf-turnstile-response"]') || 
                           document.querySelector('input[name*="turnstile"]') ||
                           document.querySelector('#cf-chl-widget-');
                return el && el.value && el.value.length > 10 ? el.value : null;
            }
        """)
        return token

    # Convenient Developer Aliases
    @classmethod
    async def solve(cls, page: Any, timeout_sec: int = 15) -> bool:
        return await cls.solve_turnstile_async(page, timeout_sec=timeout_sec)

    @classmethod
    async def solve_and_wait(cls, page: Any, timeout_sec: int = 15) -> Optional[str]:
        return await cls.harvest_token_async(page, timeout_sec=timeout_sec)
