<div align="center">

# nodetect

### Enterprise Anti-Detect Browser Automation & Persistent Profile Orchestration

[![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg?style=for-the-badge)](LICENSE)
[![Stealth Score](https://img.shields.io/badge/Stealth%20Audit-100%2F100%20Passed-brightgreen?style=for-the-badge)](examples/sannysoft_audit_proof.png)
[![Documentation](https://img.shields.io/badge/Docs-Complete%20Guide-informational?style=for-the-badge)](DOCS.md)
[![Telegram Contact](https://img.shields.io/badge/Telegram-@mitul__islam-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/mitul_islam)

<br/>

```text
███╗   ██╗ ██████╗ ██████╗ ███████╗████████╗███████╗ ██████╗████████╗
████╗  ██║██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
██╔██╗ ██║██║   ██║██║  ██║█████╗     ██║   █████╗  ██║        ██║   
██║╚██╗██║██║   ██║██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   
██║ ╚████║╚██████╔╝██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   
╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   
              E N G I N E   -   S T E A L T H   S U I T E
```

<p align="center">
  <b>Undetected Chromium Runtime</b> &bull; 
  <b>High-Entropy Client Hints</b> &bull; 
  <b>Bézier Trajectory Dynamics</b> &bull; 
  <b>Dual Browser / TLS Pipeline</b> &bull; 
  <b>Cloudflare Turnstile Auto-Solver</b>
</p>

---

<p align="center">
  <a href="https://t.me/mitul_islam">
    <img src="https://img.shields.io/badge/Direct_Telegram_Inquiries-@mitul__islam-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Direct Telegram Inquiries"/>
  </a>
  <br/>
  <sub>Available for enterprise consulting, high-volume scraping infrastructure, and custom WAF evasion (Cloudflare, DataDome, Akamai).</sub>
</p>

---

</div>

## Overview

**nodetect** is a production-grade stealth automation framework and persistent profile manager built for Python. Standard automation libraries (raw Playwright, Puppeteer, Selenium) leak dozens of internal automation indicators that cause immediate blocks on Cloudflare, DataDome, Akamai, and Kasada.

nodetect eliminates automation markers at the JavaScript prototype level, provides authentic hardware parameter tables, shields your real IP from WebRTC STUN leaks, autonomously solves Cloudflare Turnstile verification checkboxes, and features a hybrid bridge to export authenticated browser sessions into high-speed raw TLS clients (1,000+ requests/sec).

For full technical specifications, architecture diagrams, and complete class references, read the **[Comprehensive Documentation (DOCS.md)](DOCS.md)**.

---

## Live Audit: Vanilla Playwright vs nodetect Stealth

Both engines were evaluated against the industry-standard bot detection suite at `https://bot.sannysoft.com`.

| Anti-Bot Detection Vector | Vanilla Playwright | nodetect Stealth | Technical Mitigation |
| :--- | :---: | :---: | :--- |
| **`navigator.webdriver`** | Failed (Present) | **Passed (Missing)** | Prototype chain cleaned (`delete Navigator.prototype.webdriver`). No own-property leaks. |
| **`navigator.userAgentData`** | Failed / Inconsistent | **High-Entropy Hints** | Emulates `getHighEntropyValues()` with matching OS version, architecture, bitness, and brands. |
| **WebRTC STUN Leak** | Leaks Real Local/ISP IP | **Zero IP Leak Shield** | Intercepts `RTCPeerConnection` SDP offer and strips host candidate IP addresses. |
| **Cloudflare Turnstile** | Stalls / Blocks | **Autonomous Auto-Solver** | Locates widget in shadow DOM, glides cursor organically along Bézier curve, and solves challenge. |
| **`window.chrome` Object** | Missing in Headless | **Passed (Present)** | Genuine Chrome runtime with authentic `runtime`, `csi`, and `loadTimes`. |
| **`Function.prototype.toString`** | Leaks Custom Hooks | **Native Code Protected** | Wraps all patched methods to return `function () { [native code] }`. |
| **`navigator.plugins` Array** | 0 Items in Headless | **3 Genuine Plugins** | Simulates standard desktop Chrome internal PDF plugins. |
| **`PluginArray` Prototype** | Fails `instanceof` | **Passed (Valid)** | Constructs genuine `PluginArray.prototype` & `Plugin.prototype` chains with `Symbol.toStringTag`. |
| **WebGL GPU Identity** | SwiftShader Virtual GPU | **Native Hardware GPU** | Spoofs real unmasked vendors/renderers (AMD Radeon RX, NVIDIA RTX, Apple M2). |
| **Iframe Nested Contexts** | Leaks Inside Frames | **Isolated & Masked** | Injects stealth propagation directly through `HTMLIFrameElement.prototype.contentWindow`. |
| **Mouse Trajectory Telemetry** | Linear Instant Snap | **Cubic Bézier Curve** | Organic human movement with ease-in-out deceleration, velocity jitter, and overshoot. |
| **Typing Latency** | Uniform Delay | **Gaussian Cadence** | Natural human keystroke variance with punctuation pauses. |
| **Session & Profile State** | Wiped on Process Close | **Encrypted SQLite Store** | Isolated Chromium user data dirs, persistent cookies, and fixed proxy pairing. |

---

## Benchmark Proof Artifacts

<details open>
<summary><b>1. Head-to-Head Comparison: Vanilla Playwright vs nodetect (Click to Collapse/Expand)</b></summary>
<br/>

<table>
  <tr>
    <td align="center" width="50%">
      <b>Vanilla Playwright (Flagged as Bot)</b><br/>
      <a href="examples/comparison_vanilla_playwright.png" target="_blank">
        <img src="examples/comparison_vanilla_playwright.png" alt="Vanilla Playwright Bot Detection Failed" width="380" style="max-height: 380px; object-fit: cover; object-position: top; border: 1px solid #ff4444;"/>
      </a>
      <br/>
      <small><i>WebDriver (New) flagged in RED. (Click image to open full resolution)</i></small>
    </td>
    <td align="center" width="50%">
      <b>nodetect Stealth (100% Passed)</b><br/>
      <a href="examples/comparison_nodetect.png" target="_blank">
        <img src="examples/comparison_nodetect.png" alt="nodetect Stealth Audit Passed" width="380" style="max-height: 380px; object-fit: cover; object-position: top; border: 1px solid #00c853;"/>
      </a>
      <br/>
      <small><i>WebDriver (New) missing (passed). (Click image to open full resolution)</i></small>
    </td>
  </tr>
</table>

</details>

<details>
<summary><b>2. Deep Sannysoft Evasion Audit (Full 100/100 Capture)</b></summary>
<br/>

<div align="center">
  <a href="examples/sannysoft_audit_proof.png" target="_blank">
    <img src="examples/sannysoft_audit_proof.png" alt="Full Sannysoft Bot Audit All Green" width="600" style="max-height: 420px; object-fit: cover; object-position: top; border-radius: 6px; border: 1px solid #333;"/>
  </a>
  <br/>
  <small><i>(Click image to view full high-resolution capture)</i></small>
</div>

</details>

<details>
<summary><b>3. Authenticated Login Flow Execution</b></summary>
<br/>

<div align="center">
  <a href="examples/login_success_proof.png" target="_blank">
    <img src="examples/login_success_proof.png" alt="Authenticated Login Flow Screenshot Proof" width="600" style="max-height: 380px; object-fit: cover; border-radius: 6px; border: 1px solid #333;"/>
  </a>
  <br/>
  <small><i>(Click image to view full high-resolution capture)</i></small>
</div>

</details>

---

## Quickstart Guide

### 1. Installation

Install via PyPI:
```bash
pip install nodetect
playwright install chromium
```

Or install from source:
```bash
git clone https://github.com/sudoxdev/nodetect.git
cd nodetect
pip install -e .
playwright install chromium
```

### 2. Basic Automation Example

```python
import asyncio
from nodetect import StealthEngine

async def main():
    engine = StealthEngine()

    # Launch undetected browser session (deterministic hardware footprint generated automatically)
    session = await engine.launch(profile_id="account_alpha", headless=False)
    page = session.page

    # Navigate
    await page.goto("https://duckduckgo.com")

    # Organic typing with natural Gaussian cadence
    await page.stealth_type("input[name='q']", "nodetect Stealth Browser", wpm=70)

    # Organic mouse glide along cubic Bézier trajectory
    await page.stealth_click("button[type='submit']")

    # Persists cookies and session state into SQLite vault
    await session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Playwright Interoperability

Because `session.page` is a **native Playwright `Page`** and `session.context` is a **native Playwright `BrowserContext`**, you have complete access to the full Playwright API surface without restrictions:

```python
import asyncio
from nodetect import StealthEngine

async def run():
    engine = StealthEngine()
    session = await engine.launch(profile_id="worker_01", headless=False)
    page = session.page

    # Standard Playwright Locators
    await page.goto("https://target-portal.com")
    await page.locator("#username").fill("admin")

    # Request Routing & Asset Blocking
    await page.route("**/*.{png,jpg,svg}", lambda route: route.abort())

    # Multi-tab Contexts
    tab2 = await session.context.new_page()
    await tab2.goto("https://target-portal.com/dashboard")

    # Native Full-Page Screenshots
    await tab2.screenshot(path="dashboard.png", full_page=True)

    await session.close()

asyncio.run(run())
```

---

## The Hybrid Pipeline: Solve Once, Scrape at 1,000 req/s

Running dozens of browser instances consumes massive server memory. nodetect allows solving the initial challenge or login in an undetected browser, then syncing cookies directly to a raw TLS client:

```python
import asyncio
from nodetect import StealthEngine

async def hybrid_scrape():
    engine = StealthEngine()
    session = await engine.launch(profile_id="harvester_01", headless=True)
    page = session.page

    # 1. Solve challenge / authenticate in browser
    await page.goto("https://target-portal.com/login")
    
    # 2. Bridge authenticated cookies into raw curl_cffi TLS session
    tls = await session.export_to_tls_session()
    await session.close()

    # 3. Fire lightning-fast requests matching real Chrome TLS/JA3 fingerprints
    response = tls.get("https://target-portal.com/api/data")
    print("Fast TLS Response Status:", response.status_code)
    tls.close()

asyncio.run(hybrid_scrape())
```

---

## Cloudflare Turnstile & Clearance Harvesting

### Autonomous Turnstile Solver
```python
# Automatically locate Turnstile widget, glide cursor, and click
solved = await page.solve_turnstile(timeout_sec=20)

# Extract verified response token
token = await page.harvest_turnstile_token()
```

### Acquiring `cf_clearance` via Terminal CLI
```bash
python -m nodetect.cli clearance https://nowsecure.nl
```

---

## Terminal Command-Line Suite

nodetect includes a terminal interface for profile management and benchmark auditing:

```bash
# View system architecture status
python -m nodetect.cli info

# Create isolated profile bound to a proxy
python -m nodetect.cli profile create worker_01 --proxy "http://user:pass@host:port"

# Import real consumer hardware dump (harvest-fp.html)
python -m nodetect.cli profile import laptop_01 ./real-fp.json

# List registered profiles & hardware configurations
python -m nodetect.cli profile list

# Launch interactive browser session (auto-saves state on close)
python -m nodetect.cli launch worker_01 --url "https://twitter.com/login"

# Run automated detection audit
python -m nodetect.cli test --profile worker_01 --headless
```

---

## Verification & Test Suite

Run the unit test suite to verify fingerprint determinism, SQLite persistence, and evasion compilation:

```bash
pytest tests/
```

```text
tests/test_nodetect.py ........                                          [100%]
============================== 8 passed in 0.92s ==============================
```

---

## Documentation

For the complete technical manual covering all classes, methods, parameters, and architecture blueprints, refer to:

- **[Full Documentation Manual (DOCS.md)](DOCS.md)**

---

## Contributing

Contributions, bug reports, and evasion patches are welcome!  
Please review the **[Contributing Guidelines (CONTRIBUTING.md)](CONTRIBUTING.md)** before submitting a pull request.

---

## Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/sudoxdev">
        <img src="https://github.com/sudoxdev.png?size=80" width="80px;" alt="Mitul Islam" style="border-radius: 50%;"/><br />
        <sub><b>Mitul Islam</b></sub>
      </a><br />
      <sub>Creator & Maintainer</sub>
    </td>
    <td align="center">
      <a href="https://www.anthropic.com">
        <img src="https://avatars.githubusercontent.com/u/76263028?s=80&v=4" width="80px;" alt="Claude" style="border-radius: 50%;"/><br />
        <sub><b>Claude</b></sub>
      </a><br />
      <sub>AI Architecture Partner</sub>
    </td>
  </tr>
</table>

---

## Commercial Support & Engineering

For enterprise infrastructure, custom scraping clusters, or bespoke WAF bypass:

<p align="left">
  <a href="https://t.me/mitul_islam">
    <img src="https://img.shields.io/badge/Telegram-Direct%20Chat-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Contact"/>
  </a>
</p>

- **Lead Engineer:** Mitul Islam
- **Telegram Handle:** [`@mitul_islam`](https://t.me/mitul_islam)
- **Email:** `mitulislam483@gmail.com`
- **GitHub:** [`sudoxdev`](https://github.com/sudoxdev)

<br/>

<div align="center">
  <sub>Distributed under the MIT License. Built for precision automation, research, and data infrastructure.</sub>
</div>
