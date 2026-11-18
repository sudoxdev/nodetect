"""
Example 07: Automated Cloudflare Turnstile & Challenge Solver Demo
Demonstrates autonomous widget detection, organic cursor navigation, and verification.
"""
import asyncio
from nodetect import StealthEngine


async def main():
    engine = StealthEngine()
    profile_id = "turnstile_solver_demo"

    print(f"[*] Launching PhantomVault Engine [Profile: {profile_id}]...")
    session = await engine.launch(profile_id=profile_id, headless=False)
    page = session.page

    # Target: 2Captcha Cloudflare Turnstile Live Demo Portal
    target_url = "https://2captcha.com/demo/cloudflare-turnstile"
    print(f"[*] Navigating to Turnstile challenge testbed: {target_url}")
    await page.goto(target_url, wait_until="domcontentloaded")
    await asyncio.sleep(2)

    print("[*] Initiating autonomous Turnstile widget detection & solve...")
    # Calls the built-in TurnstileSolver
    solved = await session.solve_turnstile(timeout_sec=20)

    if solved:
        print("[bold green]✔ Cloudflare Turnstile Solved Successfully![/bold green]")
        # Submit the verified form
        submit_btn = await page.query_selector('button[type="submit"]')
        if submit_btn:
            await page.stealth_click('button[type="submit"]')
            await asyncio.sleep(2)
            print("[+] Form submitted with verified challenge token.")
    else:
        print("[yellow]Notice: Widget not resolved within timeout (or already passed).[/yellow]")

    await session.close()
    print("[+] Session closed cleanly.")


if __name__ == "__main__":
    asyncio.run(main())

