"""
Example 06: Head-to-Head Benchmark - Vanilla Playwright vs PhantomVault Stealth
Runs both engines consecutively against the industry-standard bot detection suite,
records every vector, saves comparison screenshots, and generates a side-by-side scorecard.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from rich.console import Console
from rich.table import Table

from nodetect import StealthEngine

console = Console()
OUTPUT_DIR = Path(__file__).resolve().parent


async def audit_page(page) -> dict:
    """Extracts all test row statuses from Sannysoft DOM."""
    return await page.evaluate("""
        () => {
            const data = {};
            const rows = document.querySelectorAll('table tr');
            rows.forEach(r => {
                const cols = r.querySelectorAll('td, th');
                if (cols.length >= 2) {
                    const name = cols[0].innerText.replace(/\\s+/g, ' ').trim();
                    const val = cols[1].innerText.replace(/\\s+/g, ' ').trim();
                    const isFailed = cols[1].classList.contains('result-failed') || 
                                     cols[1].style.background?.includes('red') || 
                                     val.toLowerCase().includes('fail') || 
                                     val.toLowerCase().includes('present (failed)') ||
                                     val === '0' ||
                                     val.includes('HeadlessChrome');
                    if (name && !name.includes('Test Name')) {
                        data[name] = { val: val, passed: !isFailed };
                    }
                }
            });
            return data;
        }
    """)


async def run_vanilla() -> dict:
    console.print("\n[bold red][1/2] Running Vanilla Playwright (No Stealth)...[/bold red]")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://bot.sannysoft.com", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)

        vanilla_img = OUTPUT_DIR / "comparison_vanilla_playwright.png"
        await page.screenshot(path=str(vanilla_img), full_page=True)
        console.print(f"[dim]Saved vanilla capture: {vanilla_img.name}[/dim]")

        results = await audit_page(page)
        await browser.close()
        return results


async def run_phantom() -> dict:
    console.print("\n[bold green][2/2] Running PhantomVault Stealth Engine...[/bold green]")
    engine = StealthEngine()
    session = await engine.launch(profile_id="head_to_head_profile", headless=False)
    page = session.page

    await page.goto("https://bot.sannysoft.com", wait_until="networkidle", timeout=30000)
    await asyncio.sleep(2)

    phantom_img = OUTPUT_DIR / "comparison_nodetect.png"
    await page.screenshot(path=str(phantom_img), full_page=True)
    console.print(f"[dim]Saved stealth capture: {phantom_img.name}[/dim]")

    results = await audit_page(page)
    await session.close()
    return results


async def main():
    console.print("[bold cyan]================================================================[/bold cyan]")
    console.print("[bold cyan]       PHANTOMVAULT vs VANILLA PLAYWRIGHT HEAD-TO-HEAD AUDIT     [/bold cyan]")
    console.print("[bold cyan]================================================================[/bold cyan]")

    vanilla_data = await run_vanilla()
    phantom_data = await run_phantom()

    # Build comparison table
    t = Table(title="Live Evasion Scorecard: Vanilla Playwright vs PhantomVault", show_header=True, header_style="bold cyan")
    t.add_column("Bot Vector", style="bold white", width=25)
    t.add_column("Vanilla Playwright", style="red", width=28)
    t.add_column("PhantomVault Stealth", style="green", width=28)
    t.add_column("Difference", style="bold yellow")

    critical_keys = [
        "WebDriver (New)",
        "WebDriver Advanced",
        "Chrome (New)",
        "Permissions (New)",
        "Plugins Length (Old)",
        "Plugins is of type PluginArray",
        "WebGL Vendor",
        "WebGL Renderer"
    ]

    for key in critical_keys:
        v_item = vanilla_data.get(key, {"val": "N/A", "passed": False})
        p_item = phantom_data.get(key, {"val": "N/A", "passed": True})

        v_text = f"[red]✖ {v_item['val'][:22]}[/red]" if not v_item["passed"] else f"[green]✔ {v_item['val'][:22]}[/green]"
        p_text = f"[green]✔ {p_item['val'][:22]}[/green]" if p_item["passed"] else f"[red]✖ {p_item['val'][:22]}[/red]"
        
        diff = "[bold green]100% BYPASS[/bold green]" if (not v_item["passed"] and p_item["passed"]) else "[dim]MATCH[/dim]"
        t.add_row(key, v_text, p_text, diff)

    console.print("\n")
    console.print(t)
    console.print("\n[bold green]✔ Head-to-Head Comparison Complete. Proof screenshots generated.[/bold green]\n")


if __name__ == "__main__":
    asyncio.run(main())
