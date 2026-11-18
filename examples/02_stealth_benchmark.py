"""
Example 02: Verification against Bot Detection Test Suites
"""
import asyncio
from nodetect import StealthEngine


async def main():
    engine = StealthEngine()

    print("[*] Launching stealth audit session...")
    session = await engine.launch(profile_id="audit_profile", headless=False)
    page = session.page

    print("[*] Navigating to SannySoft Bot Detection...")
    await page.goto("https://bot.sannysoft.com", wait_until="networkidle")

    # Take screenshot of the test results
    screenshot_path = "sannysoft_result.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"[+] Benchmark screenshot saved to: {screenshot_path}")

    await session.close()


if __name__ == "__main__":
    asyncio.run(main())

