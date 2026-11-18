import asyncio
from nodetect import launch
from nodetect.core.solver import TurnstileSolver

async def test_turnstile():
    # হেডলেস ছাড়া ব্রাউজার ওপেন হবে যাতে ইন্টারঅ্যাকশন দেখতে পারো
    session = await launch(headless=False)
    page = session.page

    print("Navigating to Turnstile test page...")
    await page.goto("https://seleniumbase.io/apps/turnstile")

    print("Waiting for Turnstile widget and solving...")
    token = await TurnstileSolver.solve_and_wait(page, timeout_sec=25)

    if token:
        print(f"Turnstile Solved Successfully! Token: {token[:35]}...")
    else:
        print("Turnstile widget passed or manual verification required.")

    await asyncio.sleep(5)
    await session.close()

if __name__ == "__main__":
    asyncio.run(test_turnstile())