# nodetect Documentation & Technical Reference Manual

Welcome to the comprehensive technical documentation for **nodetect**, the enterprise-grade anti-detect browser automation and persistent profile orchestration engine in Python.

---

## Table of Contents

1. [Architecture & Design Principles](#1-architecture--design-principles)
2. [Installation & Prerequisites](#2-installation--prerequisites)
3. [Python SDK API Reference](#3-python-sdk-api-reference)
   - [StealthEngine](#stealthengine)
   - [StealthSession & Native Playwright Interop](#stealthsession--native-playwright-interop)
   - [TLSSession](#tlssession)
   - [TurnstileSolver](#turnstilesolver)
   - [ClearanceHarvester](#clearanceharvester)
   - [ProfileManager & Fingerprint](#profilemanager--fingerprint)
   - [Harvester](#harvester)
4. [Complete Automation Workflows](#4-complete-automation-workflows)
   - [Workflow A: Standard Undetected Form & Scraping](#workflow-a-standard-undetected-form--scraping)
   - [Workflow B: Native Playwright Feature Integration](#workflow-b-native-playwright-feature-integration)
   - [Workflow C: The Hybrid Browser-to-TLS Handover](#workflow-c-the-hybrid-browser-to-tls-handover)
   - [Workflow D: Cloudflare Turnstile & Clearance Harvesting](#workflow-d-cloudflare-turnstile--clearance-harvesting)
5. [Hardware Fingerprint Harvesting Workflow](#5-hardware-fingerprint-harvesting-workflow)
6. [CLI Command Reference](#6-cli-command-reference)
7. [Enterprise Best Practices & Evasion Guidelines](#7-enterprise-best-practices--evasion-guidelines)

---

## 1. Architecture & Design Principles

Modern web application firewalls (Cloudflare, DataDome, Akamai, Kasada) identify bots through deep runtime telemetry:

1. **Protocol-Level Signals:** Checking for Chromium DevTools Protocol (CDP) bindings, `navigator.webdriver`, and execution within isolated VM wrappers.
2. **Hardware Consistency:** Comparing screen depth, WebGL GLenum limits, shader precision formats, and audio oscillation hashes.
3. **Behavioral Telemetry:** Analyzing mouse movement trajectories (linear versus curved acceleration) and uniform keystroke latencies.
4. **Network Fingerprinting:** Checking TLS cipher ordering, HTTP/2 SETTINGS frames, and WebRTC STUN host candidate leaks.

nodetect addresses these vectors systematically:

```
[ Target Web Application ]
         ▲
         │ (Undetected Runtime Context)
┌────────┴───────────────────────────────────────────────────────┐
│                       nodetect Engine                      │
├────────────────────────────────┬───────────────────────────────┤
│ Core Playwright Runtime        │ curl_cffi TLS Impersonator    │
│ • blink automation suppressed  │ • Chrome JA3/JA4 fingerprints │
│ • isolated persistent context  │ • HTTP/2 SETTINGS frame match │
├────────────────────────────────┴───────────────────────────────┤
│ Injected Stealth Subsystems                                    │
│ • Navigator.prototype.webdriver eradication                    │
│ • NavigatorUAData high-entropy client hints                    │
│ • Full WebGL GLenum parameter table & shader precision spoof   │
│ • WebRTC STUN SDP candidate leak shield                        │
│ • WeakSet native Function.prototype.toString protection        │
│ • Error stack trace sanitization                               │
├────────────────────────────────────────────────────────────────┤
│ Behavioral & Persistence Layer                                 │
│ • Cubic Bézier curve mouse trajectory generator                │
│ • Gaussian keystroke latency with punctuation micro-pauses     │
│ • SQLite profile vault & isolated Chromium user data dirs      │
└────────────────────────────────────────────────────────────────┘
```

---

## 2. Installation & Prerequisites

### Requirements
- **Python:** 3.9, 3.10, 3.11, 3.12, 3.13, or 3.14
- **Operating Systems:** Windows 10/11, macOS (Intel & Apple Silicon), Linux (Ubuntu, Debian, Fedora, Arch)

### Setup

```bash
git clone https://github.com/USERNAME/nodetect.git
cd nodetect

# Install Python requirements
pip install -r requirements.txt

# Install Chromium browser binaries
playwright install chromium
```

---

## 3. Python SDK API Reference

### StealthEngine

The entry orchestrator for creating and launching undetected browser environments.

```python
from nodetect import StealthEngine

engine = StealthEngine(manager=None)
```

#### Methods

##### `async launch(profile_id: str, headless: bool = False, proxy: Optional[str] = None, platform_type: str = "windows") -> StealthSession`
Launches an undetected Chromium browser context configured with seed-locked hardware parameters and stealth injections.

- **`profile_id`** *(str)*: Unique identifier for the profile.
- **`headless`** *(bool, default=False)*: Runs headless when `True`, visible window when `False`.
- **`proxy`** *(Optional[str], default=None)*: Proxy server URL in format `http://user:pass@host:port` or `socks5://host:port`.
- **`platform_type`** *(str, default="windows")*: Target operating system emulation (`windows`, `mac`, `linux`).
- **Returns:** An active `StealthSession` instance.

---

### StealthSession & Native Playwright Interop

The `StealthSession` instance wraps the underlying Playwright `BrowserContext` and `Page`. All standard Playwright methods remain 100% accessible directly via `session.page` and `session.context`.

#### Properties
- **`session.page`**: The native Playwright `Page` object.
- **`session.context`**: The native Playwright `BrowserContext` object.
- **`session.record`**: The `ProfileRecord` metadata container.

#### Built-in Stealth Helpers (Available on `session.page`)

##### `await session.page.stealth_click(selector: str)`
Locates the DOM element, generates an organic cubic Bézier path from current coordinates to the element center, glides the cursor with natural ease-in-out deceleration, and dispatches humanized mouse down/up events.

##### `await session.page.stealth_type(selector: str, text: str, wpm: int = 65)`
Clicks the input field and inputs characters using Gaussian-distributed delays with natural micro-pauses at punctuation marks and spaces.

##### `await session.page.stealth_scroll(delta_y: int, steps: int = 10)`
Performs an eased scroll action over multiple intermediate steps.

##### `await session.page.solve_turnstile(timeout_sec: int = 15) -> bool`
Scans the page and shadow roots for Cloudflare Turnstile widgets, calculates checkbox coordinates, glides the cursor to click, and awaits validation. Returns `True` if successfully solved.

##### `await session.page.harvest_turnstile_token(timeout_sec: int = 15) -> Optional[str]`
Executes Turnstile resolution and returns the verified `cf-turnstile-response` token string.

##### `await session.export_to_tls_session() -> TLSSession`
Extracts all authenticated browser cookies, user-agent, and proxy parameters into an active `TLSSession` instance for high-speed requests.

##### `await session.close()`
Persists all session cookies, origin states, and localStorage into the SQLite database, then terminates the browser process cleanly.

---

### TLSSession

High-throughput HTTP client utilizing `curl_cffi` to match authentic desktop Chrome TLS JA3/JA4 handshakes and HTTP/2 protocol frames.

```python
from nodetect import TLSSession

tls = TLSSession(fingerprint=fp, proxy="http://host:port", impersonate="chrome120")
```

#### Methods
- **`get(url: str, **kwargs) -> Response`**: Executes GET request matching Chrome fingerprint.
- **`post(url: str, **kwargs) -> Response`**: Executes POST request.
- **`import_playwright_cookies(cookies: List[Dict[str, Any]])`**: Synchronizes browser cookie state.
- **`export_cookies_dict() -> Dict[str, str]`**: Returns cookies as simple dictionary.
- **`close()`**: Closes connection pools.

---

### TurnstileSolver

Autonomous resolver for Cloudflare Turnstile verification checkboxes.

```python
from nodetect import TurnstileSolver

# Static helper methods
solved = await TurnstileSolver.solve_turnstile_async(page, timeout_sec=20)
token = await TurnstileSolver.harvest_token_async(page, timeout_sec=20)
```

---

### ClearanceHarvester

Automates `cf_clearance` cookie acquisition and high-speed TLS session initialization.

```python
from nodetect import ClearanceHarvester

token, tls_session = await ClearanceHarvester.acquire_clearance(
    url="https://protected-site.com",
    proxy="http://user:pass@gate.proxy.com:8000",
    timeout_sec=35,
    headless=False
)
```

---

### ProfileManager & Fingerprint

Coordinates disk persistence and hardware parameter generation.

```python
from nodetect import ProfileManager, Fingerprint

mgr = ProfileManager()
record = mgr.create_profile(profile_id="node_01", name="Worker 1", proxy=None)
profiles = mgr.list_profiles()
mgr.delete_profile("node_01")
```

---

### Harvester

Imports authentic device dumps generated by `harvest-fp.html`.

```python
from nodetect import Harvester
from pathlib import Path

record = Harvester.import_to_profile(
    profile_id="consumer_laptop",
    json_path=Path("./real-fp.json"),
    proxy="http://user:pass@host:port"
)
```

---

## 4. Complete Automation Workflows

### Workflow A: Standard Undetected Form & Scraping

```python
import asyncio
from nodetect import StealthEngine

async def run():
    engine = StealthEngine()
    session = await engine.launch(profile_id="scraper_node", headless=False)
    page = session.page

    await page.goto("https://duckduckgo.com")
    
    # Humanized interaction
    await page.stealth_type("input[name='q']", "Enterprise Anti-Detect Automation", wpm=75)
    await page.stealth_click("button[type='submit']")

    await page.wait_for_selector(".results")
    content = await page.content()
    print("Page content length:", len(content))

    await session.close()

asyncio.run(run())
```

---

### Workflow B: Native Playwright Feature Integration

Because `session.page` is a standard Playwright `Page`, all native Playwright APIs function normally:

```python
import asyncio
from nodetect import StealthEngine

async def advanced_playwright_flow():
    engine = StealthEngine()
    session = await engine.launch(profile_id="advanced_worker", headless=False)
    page = session.page

    # 1. Block resource-heavy assets
    await page.route("**/*.{png,jpg,jpeg,svg,woff2}", lambda route: route.abort())

    # 2. Intercept responses
    page.on("response", lambda res: print("Status:", res.status, res.url[:50]))

    # 3. Native locator interactions
    await page.goto("https://quotes.toscrape.com/login")
    await page.locator("#username").fill("my_user")
    await page.locator("#password").fill("my_pass")
    await page.locator("input[type='submit']").click()

    # 4. Multi-tab handling
    new_page = await session.context.new_page()
    await new_page.goto("https://quotes.toscrape.com")
    
    # 5. Native full-page screenshot
    await new_page.screenshot(path="quotes.png", full_page=True)

    await session.close()

asyncio.run(advanced_playwright_flow())
```

---

### Workflow C: The Hybrid Browser-to-TLS Handover

Solve initial authentication in an undetected browser, export cookies, and scrape at 1,000 req/s:

```python
import asyncio
from nodetect import StealthEngine

async def hybrid_pipeline():
    engine = StealthEngine()
    session = await engine.launch(profile_id="hybrid_worker", headless=True)
    page = session.page

    # Authenticate or solve challenge
    await page.goto("https://httpbin.org/cookies/set?session_token=abc123xyz&auth=valid")
    
    # Export state to raw TLS engine
    tls = await session.export_to_tls_session()
    await session.close()

    # Fast HTTP requests matching real Chrome TLS JA3/JA4
    for i in range(10):
        resp = tls.get("https://httpbin.org/cookies")
        print(f"Request {i+1} status:", resp.status_code)

    tls.close()

asyncio.run(hybrid_pipeline())
```

---

### Workflow D: Cloudflare Turnstile & Clearance Harvesting

```python
import asyncio
from nodetect import StealthEngine

async def solve_turnstile_demo():
    engine = StealthEngine()
    session = await engine.launch(profile_id="turnstile_worker", headless=False)
    page = session.page

    await page.goto("https://2captcha.com/demo/cloudflare-turnstile")

    # Autonomous resolution
    solved = await page.solve_turnstile(timeout_sec=20)
    print("Turnstile solved status:", solved)

    token = await page.harvest_turnstile_token()
    print("Harvested response token:", token[:40] if token else "None")

    await session.close()

asyncio.run(solve_turnstile_demo())
```

---

## 5. Hardware Fingerprint Harvesting Workflow

nodetect includes `harvest-fp.html` to dump genuine hardware footprints from real consumer devices.

### Step-by-Step Harvesting:
1. Open `harvest-fp.html` in an authentic desktop Google Chrome browser (double-click the HTML file).
2. Click **Harvest**. The tool inspects your real hardware (WebGL GLenums, precision format, AudioContext oscillator sum, Client Hints).
3. Click **Download real-fp.json**.
4. Import the file directly into your nodetect profile store via terminal:

```bash
python -m nodetect.cli profile import my_macbook ./real-fp.json --proxy "http://user:pass@proxy.com:8000"
```

Once imported, any browser launched under `my_macbook` will output the exact hardware signatures, WebGL parameter tables, and audio hashes of that genuine device.

---

## 6. CLI Command Reference

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `nodetect info` | None | Displays banner and architecture status |
| `nodetect profile list` | None | Lists all saved profiles, GPUs, and proxies |
| `nodetect profile create` | `<id> [--name] [--proxy] [--platform]` | Creates a new profile with deterministic specs |
| `nodetect profile import` | `<id> <json_path> [--proxy]` | Imports real fingerprint dump (`harvest-fp.html`) |
| `nodetect profile delete` | `<id>` | Purges a profile and its isolated disk storage |
| `nodetect launch` | `<id> [--url] [--headless]` | Launches interactive browser session |
| `nodetect test` | `[--profile] [--headless]` | Runs internal bot detection audit |
| `nodetect turnstile` | `<url> [--timeout] [--headless]` | Auto-solves Turnstile on target URL |
| `nodetect clearance` | `<url> [--proxy] [--timeout]` | Extracts `cf_clearance` cookie & verifies TLS |

---

## 7. Enterprise Best Practices & Evasion Guidelines

1. **Proxy Consistency:** Always match proxy geolocation with the profile timezone. If using a German residential proxy, ensure the profile timezone is set to `Europe/Berlin` and locale to `de-DE`.
2. **WebRTC Protection:** Never disable WebRTC entirely via Chrome flags (`--disable-webrtc`), as anti-bot scripts treat missing `RTCPeerConnection` as an immediate bot indicator. nodetect's SDP candidate stripper protects your IP while keeping the WebRTC API fully operational.
3. **Session Re-use:** Store session state in SQLite rather than logging in every execution. Repetitive logins from fresh browser instances trigger security challenge escalation.
4. **Keystroke Randomization:** Avoid using `fill()` for sensitive anti-bot form inputs. Always use `stealth_type()` to ensure natural Gaussian typing velocity.

