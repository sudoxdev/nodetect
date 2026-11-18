"""
Core Stealth Engine for PhantomVault.
Binds Playwright browser runtime, stealth evasions, profile persistence, and humanized controls.
"""
from typing import Optional, Dict, Any, List
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright, BrowserContext, Page

from nodetect.config import STEALTH_CHROME_ARGS
from nodetect.profile.fingerprint import Fingerprint
from nodetect.profile.manager import ProfileManager, ProfileRecord
from nodetect.core.patches import build_stealth_script
from nodetect.core.humanizer import Humanizer
from nodetect.core.tls_session import TLSSession
from nodetect.core.solver import TurnstileSolver
from nodetect.core.cookies import CookieVault
from nodetect.core.iuam import CloudflareIUAM
from nodetect.core.proxy_pool import ProxyPool


class StealthSession:
    """
    Active browser session wrapper holding Playwright context, page, and profile metadata.
    """

    def __init__(self, record: ProfileRecord, context: BrowserContext, page: Page, manager: ProfileManager, pw_instance: Any = None):
        self.record = record
        self.context = context
        self.page = page
        self.manager = manager
        self.pw_instance = pw_instance
        self._bind_human_helpers()

    def _bind_human_helpers(self):
        """Attaches organic interaction, speed acceleration, and challenge solving helpers directly to page instance."""
        async def stealth_click(selector: str, fast: bool = False):
            await Humanizer.click_element_async(self.page, selector, fast=fast)

        async def stealth_type(selector: str, text: str, wpm: int = 85, fast: bool = False):
            await Humanizer.type_text_async(self.page, selector, text, wpm=wpm, fast=fast)

        async def stealth_scroll(delta_y: int, steps: int = 6, fast: bool = False):
            await Humanizer.smooth_scroll_async(self.page, delta_y, steps=steps, fast=fast)

        async def solve_turnstile(timeout_sec: int = 15) -> bool:
            return await TurnstileSolver.solve_turnstile_async(self.page, timeout_sec=timeout_sec)

        async def harvest_turnstile_token(timeout_sec: int = 15) -> Optional[str]:
            return await TurnstileSolver.harvest_token_async(self.page, timeout_sec=timeout_sec)

        async def wait_for_cloudflare(timeout_sec: int = 25) -> bool:
            """Waits for Cloudflare IUAM / Just a moment... spinning shield to clear."""
            return await CloudflareIUAM.wait_for_clear(self.page, timeout_sec=timeout_sec)

        async def enable_turbo_mode(block_images: bool = True, block_fonts: bool = True, block_media: bool = True):
            """
            Accelerates scraping speed by 3x-5x by blocking heavy visual assets while preserving DOM and JS.
            """
            patterns = []
            if block_images:
                patterns.extend([".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico"])
            if block_fonts:
                patterns.extend([".woff", ".woff2", ".ttf", ".otf"])
            if block_media:
                patterns.extend([".mp4", ".mp3", ".webm", ".avi"])

            async def _interceptor(route):
                req_url = route.request.url.lower()
                if any(ext in req_url for ext in patterns) or route.request.resource_type in ["image", "media", "font"]:
                    await route.abort()
                else:
                    await route.continue_()

            await self.page.route("**/*", _interceptor)

        setattr(self.page, "stealth_click", stealth_click)
        setattr(self.page, "stealth_type", stealth_type)
        setattr(self.page, "stealth_scroll", stealth_scroll)
        setattr(self.page, "solve_turnstile", solve_turnstile)
        setattr(self.page, "harvest_turnstile_token", harvest_turnstile_token)
        setattr(self.page, "wait_for_cloudflare", wait_for_cloudflare)
        setattr(self.page, "enable_turbo_mode", enable_turbo_mode)
        setattr(self, "solve_turnstile", solve_turnstile)
        setattr(self, "harvest_turnstile_token", harvest_turnstile_token)
        setattr(self, "wait_for_cloudflare", wait_for_cloudflare)
        setattr(self, "enable_turbo_mode", enable_turbo_mode)

    async def get_cookies(self) -> List[Dict[str, Any]]:
        """Retrieve current cookies from browser context."""
        return await self.context.cookies()

    async def export_cookies_json(self, file_path: str):
        """Exports cookies in standard EditThisCookie JSON format."""
        cookies = await self.get_cookies()
        CookieVault.export_json(cookies, file_path)

    async def export_cookies_netscape(self, file_path: str):
        """Exports cookies in standard Netscape format for cURL/wget."""
        cookies = await self.get_cookies()
        CookieVault.export_netscape(cookies, file_path)

    async def import_cookies_json(self, file_path: str):
        """Imports cookies from an EditThisCookie JSON file into the active context."""
        cookies = CookieVault.import_json(file_path)
        await self.context.add_cookies(cookies)

    async def export_to_tls_session(self) -> TLSSession:
        """
        Creates a high-performance curl_cffi session inheriting the current browser's
        cookies, user-agent, and proxy.
        """
        cookies = await self.get_cookies()
        session = TLSSession(
            fingerprint=self.record.fingerprint,
            proxy=self.record.proxy
        )
        session.import_playwright_cookies(cookies)
        return session

    async def save_state(self):
        """Dumps storage state (cookies, localStorage) into ProfileManager."""
        state = await self.context.storage_state()
        self.manager.save_session_state(self.record.profile_id, state)

    async def close(self):
        """Saves session state and closes browser context and Playwright process cleanly."""
        try:
            await self.save_state()
        except Exception:
            pass
        try:
            await self.context.close()
        except Exception:
            pass
        if self.pw_instance:
            try:
                await self.pw_instance.stop()
            except Exception:
                pass


class StealthEngine:
    """
    Main entry point for launching undetected browser instances.
    """

    def __init__(self, manager: Optional[ProfileManager] = None):
        self.manager = manager or ProfileManager()

    async def launch(
        self,
        profile_id: str,
        headless: bool = False,
        proxy: Optional[str] = None,
        proxy_pool: Optional[ProxyPool] = None,
        platform_type: str = "windows",
        turbo_mode: bool = False
    ) -> StealthSession:
        """
        Launches an isolated Chromium instance loaded with profile fingerprint and stealth evasions.
        Supports automatic proxy rotation if proxy_pool is supplied.
        """
        resolved_proxy = proxy
        if resolved_proxy is None and proxy_pool is not None:
            resolved_proxy = proxy_pool.get_next()

        record = self.manager.get_profile(profile_id)
        if not record:
            record = self.manager.create_profile(
                profile_id=profile_id,
                proxy=resolved_proxy,
                platform_type=platform_type
            )
        elif resolved_proxy and resolved_proxy != record.proxy:
            record.proxy = resolved_proxy

        fp = record.fingerprint
        pw = await async_playwright().start()

        proxy_config = None
        if record.proxy:
            proxy_config = {"server": record.proxy}

        # Geolocation configuration if present
        geo_config = None
        permissions = None
        if fp.latitude is not None and fp.longitude is not None:
            geo_config = {"latitude": fp.latitude, "longitude": fp.longitude, "accuracy": 20}
            permissions = ["geolocation"]

        # Launch persistent context
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=str(record.user_data_dir),
            headless=headless,
            args=STEALTH_CHROME_ARGS + [
                f"--window-size={fp.viewport_width},{fp.viewport_height}"
            ],
            user_agent=fp.user_agent,
            viewport={"width": fp.viewport_width, "height": fp.viewport_height},
            device_scale_factor=fp.device_pixel_ratio,
            color_scheme="dark",
            locale=fp.locale,
            timezone_id=fp.timezone_id,
            geolocation=geo_config,
            permissions=permissions,
            proxy=proxy_config,
            ignore_https_errors=True
        )

        # Inject stealth evasions into all pages
        stealth_js = build_stealth_script(fp)
        await context.add_init_script(stealth_js)

        # Acquire page and execute stealth script on initial page context
        if len(context.pages) > 0:
            page = context.pages[0]
            try:
                await page.evaluate(stealth_js)
            except Exception:
                pass
        else:
            page = await context.new_page()
            try:
                await page.evaluate(stealth_js)
            except Exception:
                pass

        self.manager.touch_profile(profile_id)
        session = StealthSession(record=record, context=context, page=page, manager=self.manager, pw_instance=pw)
        if turbo_mode:
            await session.enable_turbo_mode()
        return session
