"""
Example 01: Quickstart Stealth Automation with PhantomVault
"""
import asyncio
from nodetect import StealthEngine


async def main():
    engine = StealthEngine()

    print("[*] Launching undetected browser instance for profile 'demo_user'...")
    session = await engine.launch(profile_id="demo_user", headless=False)
    page = session.page

    print("[*] Navigating to target site...")
    await page.goto("https://duckduckgo.com")

    print("[*] Performing organic human typing...")
    await page.stealth_type("input[name='q']", "PhantomVault Stealth Browser", wpm=70)

    print("[*] Organic mouse movement and click...")
    await page.stealth_click("button[type='submit']")

    await asyncio.sleep(3)
    print("[*] Saving state and closing...")
    await session.close()
    print("[+] Done!")


if __name__ == "__main__":
    asyncio.run(main())

