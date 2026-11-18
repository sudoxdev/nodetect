"""
Example 04: Complete Authenticated Login Flow & Session Persistence Proof
Demonstrates humanized stealth credentials submission, navigation, screenshot capture,
and authenticated cookie handover into high-speed TLS session.
"""
import asyncio
from pathlib import Path
from nodetect import StealthEngine


async def main():
    engine = StealthEngine()
    profile_id = "client_demo_session"
    proof_path = Path(__file__).resolve().parent / "login_success_proof.png"

    print(f"[*] Initializing PhantomVault Stealth Engine [Profile: {profile_id}]...")
    session = await engine.launch(profile_id=profile_id, headless=False)
    page = session.page

    # 1. Navigate to target authentication endpoint
    target_url = "https://practicetestautomation.com/practice-test-login/"
    print(f"[*] Navigating to authentication portal: {target_url}")
    await page.goto(target_url, wait_until="domcontentloaded")
    await asyncio.sleep(1)

    # 2. Organic Humanized Typing of Username
    print("[*] Submitting username with natural Gaussian cadence...")
    await page.stealth_type("#username", "student", wpm=65)
    await asyncio.sleep(0.5)

    # 3. Organic Humanized Typing of Password
    print("[*] Submitting password with micro-delay jitter...")
    await page.stealth_type("#password", "Password123", wpm=70)
    await asyncio.sleep(0.5)

    # 4. Bézier Glided Mouse Movement and Click
    print("[*] Gliding mouse along Bézier trajectory to Submit button...")
    await page.stealth_click("#submit")

    # 5. Wait for authenticated dashboard page
    print("[*] Awaiting successful login transition...")
    await page.wait_for_selector(".post-title", timeout=15000)
    await asyncio.sleep(1.5)

    # 6. Capture full-page proof screenshot
    await page.screenshot(path=str(proof_path), full_page=True)
    print(f"[bold green]✔ Screenshot proof captured successfully:[/bold green] {proof_path}")

    # 7. Handover cookies into raw high-speed TLS session
    print("[*] Bridging authenticated browser cookies into curl_cffi TLS engine...")
    tls = await session.export_to_tls_session()

    cookies = tls.export_cookies_dict()
    print(f"[+] Synced Authenticated Cookies: {list(cookies.keys())}")

    # 8. Safely persist state to SQLite vault and close
    await session.close()
    tls.close()
    print("[bold green]✔ Complete Login & Session Persistence Flow Finished Successfully![/bold green]")


if __name__ == "__main__":
    asyncio.run(main())

