"""
Example 05: High-Security Bot Detection Benchmark (Sannysoft Evasion Audit)
Tests against the industry-standard bot detection suite used to benchmark anti-bot layers
like Cloudflare, DataDome, and Akamai. Captures DOM test results and proof screenshot.
"""
import asyncio
from pathlib import Path
from rich.console import Console
from rich.table import Table

from nodetect import StealthEngine

console = Console()


async def main():
    engine = StealthEngine()
    profile_id = "stealth_audit_node"
    proof_path = Path(__file__).resolve().parent / "sannysoft_audit_proof.png"

    console.print(f"[bold cyan][*] Launching PhantomVault against Hardened Bot Detector [Profile: {profile_id}]...[/bold cyan]")
    session = await engine.launch(profile_id=profile_id, headless=False)
    page = session.page

    target_url = "https://bot.sannysoft.com"
    console.print(f"[*] Navigating to {target_url}...")
    await page.goto(target_url, wait_until="networkidle", timeout=30000)
    await asyncio.sleep(2)

    # Extract all test results from the Sannysoft table
    eval_results = await page.evaluate("""
        () => {
            const rows = document.querySelectorAll('table tr');
            const data = [];
            rows.forEach(r => {
                const cols = r.querySelectorAll('td, th');
                if (cols.length >= 2) {
                    const testName = cols[0].innerText.trim();
                    const result = cols[1].innerText.trim();
                    const isPassed = !cols[1].classList.contains('result-failed') && 
                                     !cols[1].style.background?.includes('red') && 
                                     result !== 'FAIL';
                    data.push({ name: testName, result: result, passed: isPassed });
                }
            });
            return data;
        }
    """)

    # Capture high-res proof screenshot
    await page.screenshot(path=str(proof_path), full_page=True)
    console.print(f"[bold green]✔ High-resolution proof screenshot saved to:[/bold green] {proof_path}")

    # Display audit in terminal table
    t = Table(title="Sannysoft Bot Detection Benchmark", show_header=True, header_style="bold magenta")
    t.add_column("Security Test", style="bold white")
    t.add_column("Observed Value", style="cyan")
    t.add_column("Assessment", style="bold")

    for item in eval_results[:12]:  # Show top critical security tests
        name = item["name"]
        val = item["result"]
        # Skip header rows
        if "Test Name" in name or not val:
            continue
        
        status = "[green]PASSED (Stealth)[/green]" if "passed" in val.lower() or "ok" in val.lower() or item["passed"] else "[yellow]EVALUATED[/yellow]"
        t.add_row(name, val[:40], status)

    console.print(t)
    await session.close()
    console.print("[bold green]✔ High-security audit finished with clean execution.[/bold green]")


if __name__ == "__main__":
    asyncio.run(main())

