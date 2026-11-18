"""
PhantomVault Configuration, Hardware Fingerprints & Client Hints Presets
"""
from pathlib import Path
from typing import Dict, List, Any
import os

DEFAULT_VAULT_DIR = Path(os.environ.get("NODETECT_DIR", Path.home() / ".nodetect"))
PROFILES_DIR = DEFAULT_VAULT_DIR / "profiles"
DATABASE_PATH = DEFAULT_VAULT_DIR / "vault.db"

WEBGL_PROFILES: List[Dict[str, str]] = [
    {
        "vendor": "Google Inc. (NVIDIA)",
        "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "unmasked_vendor": "NVIDIA Corporation",
        "unmasked_renderer": "NVIDIA GeForce RTX 3070/PCIe/SSE2"
    },
    {
        "vendor": "Google Inc. (NVIDIA)",
        "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 4080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "unmasked_vendor": "NVIDIA Corporation",
        "unmasked_renderer": "NVIDIA GeForce RTX 4080/PCIe/SSE2"
    },
    {
        "vendor": "Google Inc. (AMD)",
        "renderer": "ANGLE (AMD, AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "unmasked_vendor": "AMD",
        "unmasked_renderer": "AMD Radeon RX 6700 XT"
    },
    {
        "vendor": "Google Inc. (Intel)",
        "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "unmasked_vendor": "Intel Inc.",
        "unmasked_renderer": "Intel(R) UHD Graphics 630"
    },
    {
        "vendor": "Apple Inc.",
        "renderer": "Apple GPU",
        "unmasked_vendor": "Apple",
        "unmasked_renderer": "Apple M2 Pro"
    }
]

SCREEN_RESOLUTIONS: List[Dict[str, int]] = [
    {"width": 1920, "height": 1080, "color_depth": 24, "pixel_ratio": 1},
    {"width": 2560, "height": 1440, "color_depth": 24, "pixel_ratio": 1},
    {"width": 1680, "height": 1050, "color_depth": 24, "pixel_ratio": 1},
    {"width": 1536, "height": 864, "color_depth": 24, "pixel_ratio": 1.25},
    {"width": 1440, "height": 900, "color_depth": 24, "pixel_ratio": 2}
]

DEFAULT_USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
]

# Client Hints High Entropy Presets
CLIENT_HINTS_PRESETS: Dict[str, Dict[str, Any]] = {
    "windows": {
        "platform": "Windows",
        "platformVersion": "15.0.0",
        "architecture": "x86",
        "bitness": "64",
        "model": "",
        "wow64": False,
        "brands": [
            {"brand": "Chromium", "version": "128"},
            {"brand": "Not;A=Brand", "version": "24"},
            {"brand": "Google Chrome", "version": "128"}
        ],
        "fullVersionList": [
            {"brand": "Chromium", "version": "128.0.6613.138"},
            {"brand": "Not;A=Brand", "version": "24.0.0.0"},
            {"brand": "Google Chrome", "version": "128.0.6613.138"}
        ]
    },
    "mac": {
        "platform": "macOS",
        "platformVersion": "14.5.0",
        "architecture": "arm",
        "bitness": "64",
        "model": "",
        "wow64": False,
        "brands": [
            {"brand": "Chromium", "version": "129"},
            {"brand": "Not;A=Brand", "version": "24"},
            {"brand": "Google Chrome", "version": "129"}
        ],
        "fullVersionList": [
            {"brand": "Chromium", "version": "129.0.6668.70"},
            {"brand": "Not;A=Brand", "version": "24.0.0.0"},
            {"brand": "Google Chrome", "version": "129.0.6668.70"}
        ]
    },
    "linux": {
        "platform": "Linux",
        "platformVersion": "6.5.0",
        "architecture": "x86",
        "bitness": "64",
        "model": "",
        "wow64": False,
        "brands": [
            {"brand": "Chromium", "version": "128"},
            {"brand": "Not;A=Brand", "version": "24"},
            {"brand": "Google Chrome", "version": "128"}
        ],
        "fullVersionList": [
            {"brand": "Chromium", "version": "128.0.6613.138"},
            {"brand": "Not;A=Brand", "version": "24.0.0.0"},
            {"brand": "Google Chrome", "version": "128.0.6613.138"}
        ]
    }
}

STEALTH_CHROME_ARGS: List[str] = [
    "--disable-blink-features=AutomationControlled",
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-site-isolation-trials",
    "--disable-infobars",
    "--no-default-browser-check",
    "--no-first-run",
    "--disable-popup-blocking",
    "--ignore-certificate-errors",
    "--password-store=basic",
    "--use-mock-keychain",
    "--disable-component-update",
    "--disable-background-networking",
    "--disable-sync",
    "--metrics-recording-only",
    "--disable-default-apps",
    "--disable-hang-monitor",
    "--disable-prompt-on-repost",
    "--disable-client-side-phishing-detection"
]
