"""
Example 03: Hybrid Flow - Playwright Stealth Challenge Solving -> High-Speed curl_cffi TLS Sync
"""
import asyncio
from nodetect import StealthEngine


async def main():
    engine = StealthEngine()

    print("[*] Launching browser to acquire authenticated session cookies...")
    session = await engine.launch(profile_id="api_harvester", headless=True)
    page = session.page

    await page.goto("https://httpbin.org/cookies/set?auth_token=super_secret_9988&role=admin")
    print("[*] Cookies established in browser context.")

    # Export to high-speed TLS Session
    print("[*] Syncing cookies into curl_cffi Chrome impersonation session...")
    tls = await session.export_to_tls_session()

    await session.close()
    print("[+] Browser closed. Continuing with ultra-fast raw TLS client!")

    # Perform request via curl_cffi using exact browser cookies & JA3 fingerprint
    resp = tls.get("https://httpbin.org/cookies")
    print("[+] Fast TLS Response Status:", resp.status_code)
    print("[+] Cookie payload received by server:\n", resp.text)
    tls.close()


if __name__ == "__main__":
    asyncio.run(main())

