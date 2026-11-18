"""
Unit tests for PhantomVault core functionality.
"""
import pytest
from pathlib import Path
import tempfile
import json
import sys

# Ensure nodetect package is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nodetect.profile.fingerprint import Fingerprint
from nodetect.profile.manager import ProfileManager
from nodetect.core.patches import build_stealth_script
from nodetect.core.humanizer import generate_bezier_trajectory
from nodetect.core.solver import TurnstileSolver


def test_fingerprint_determinism():
    """Ensure that the same profile ID always generates identical hardware specs."""
    fp1 = Fingerprint.generate(profile_id="alpha_node", platform_type="windows")
    fp2 = Fingerprint.generate(profile_id="alpha_node", platform_type="windows")

    assert fp1.user_agent == fp2.user_agent
    assert fp1.webgl_unmasked_renderer == fp2.webgl_unmasked_renderer
    assert fp1.viewport_width == fp2.viewport_width
    assert fp1.canvas_noise_seed == fp2.canvas_noise_seed
    assert fp1.audio_noise_seed == fp2.audio_noise_seed
    assert fp1.client_hints["platform"] == "Windows"
    assert fp1.client_hints["architecture"] == "x86"


def test_profile_manager_persistence():
    """Verify SQLite profile storage, lookup, and deletion."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test_vault.db"

        mgr = ProfileManager(db_path=db_path)
        record = mgr.create_profile(
            profile_id="test_acc_01",
            name="Test Account",
            proxy="http://127.0.0.1:8080",
            platform_type="windows"
        )

        assert record.profile_id == "test_acc_01"
        assert record.proxy == "http://127.0.0.1:8080"

        loaded = mgr.get_profile("test_acc_01")
        assert loaded is not None
        assert loaded.name == "Test Account"
        assert loaded.fingerprint.hardware_concurrency > 0

        # Save session state
        mgr.save_session_state("test_acc_01", {"cookies": [{"name": "sid", "value": "xyz"}]})
        reloaded = mgr.get_profile("test_acc_01")
        assert reloaded.storage_state is not None
        assert reloaded.storage_state["cookies"][0]["value"] == "xyz"

        # List
        all_profiles = mgr.list_profiles()
        assert len(all_profiles) == 1

        # Delete
        mgr.delete_profile("test_acc_01")
        assert mgr.get_profile("test_acc_01") is None


def test_stealth_script_advanced_features():
    """Ensure advanced evasions (Client Hints, WebRTC, Error stack) compile into script."""
    fp = Fingerprint.generate("advanced_test_fp", platform_type="windows")
    js = build_stealth_script(fp)

    assert "delete Navigator.prototype.webdriver" in js
    assert "NavigatorUAData" in js
    assert "getHighEntropyValues" in js
    assert "RTCPeerConnection" in js
    assert "a=candidate:.*typ host" in js
    assert "nativeFnMap" in js
    assert "Error.prepareStackTrace" in js


def test_bezier_curve_generation():
    """Ensure trajectory generates the expected number of smooth points."""
    start = (100.0, 100.0)
    target = (500.0, 400.0)
    points = generate_bezier_trajectory(start, target, num_points=30)

    assert len(points) == 30
    assert points[0] == start
    assert points[-1] == target


def test_harvester_import():
    """Verify that raw harvested JSON from harvest-fp.html imports cleanly."""
    from nodetect.profile.harvester import Harvester
    sample_dump = {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0",
        "platform": "Win32",
        "hardwareConcurrency": 16,
        "deviceMemory": 32,
        "languages": ["en-US", "en"],
        "tz": "America/Chicago",
        "screen": {"w": 2560, "h": 1440, "cd": 24, "dpr": 1.25},
        "webgl": {
            "vendor": "Google Inc. (NVIDIA)",
            "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 4090 Direct3D11)",
            "unmaskedVendor": "NVIDIA Corporation",
            "unmaskedRenderer": "NVIDIA GeForce RTX 4090",
            "params": {"3379": 16384, "3408": 16},
            "precision": {"VERTEX_SHADER.HIGH_FLOAT": {"rangeMin": 127, "rangeMax": 127, "precision": 23}}
        },
        "uaData": {
            "brands": [{"brand": "Google Chrome", "version": "128"}],
            "highEntropy": {"architecture": "x86", "bitness": "64", "platformVersion": "15.0.0"}
        }
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        json_file = Path(tmp_dir) / "dump.json"
        with open(json_file, "w") as f:
            json.dump(sample_dump, f)

        db_path = Path(tmp_dir) / "vault.db"
        mgr = ProfileManager(db_path=db_path)
        record = Harvester.import_to_profile(
            profile_id="harvester_node_01",
            json_path=json_file,
            manager=mgr
        )

        assert record.profile_id == "harvester_node_01"
        assert record.fingerprint.webgl_unmasked_renderer == "NVIDIA GeForce RTX 4090"
        assert record.fingerprint.webgl_params["3379"] == 16384
        assert record.fingerprint.viewport_width == 2560


def test_proxy_pool_rotation():
    """Verify proxy pool round-robin, failure tracking, and recovery."""
    from nodetect.core.proxy_pool import ProxyPool
    pool = ProxyPool(["http://1.1.1.1:8080", "http://2.2.2.2:8080"])
    assert len(pool) == 2
    
    p1 = pool.get_next()
    p2 = pool.get_next()
    p3 = pool.get_next()
    assert p1 == "http://1.1.1.1:8080"
    assert p2 == "http://2.2.2.2:8080"
    assert p3 == "http://1.1.1.1:8080"

    # Test failure marking
    pool.mark_failed("http://1.1.1.1:8080")
    pool.mark_failed("http://1.1.1.1:8080")
    pool.mark_failed("http://1.1.1.1:8080")
    # Now only p2 should be chosen
    assert pool.get_next() == "http://2.2.2.2:8080"


def test_cookie_vault_export_import():
    """Verify EditThisCookie JSON and Netscape cookie formatting."""
    from nodetect.core.cookies import CookieVault
    sample_cookies = [
        {"name": "cf_clearance", "value": "test_clearance_123", "domain": ".example.com", "path": "/", "secure": True, "expires": 1780000000}
    ]

    with tempfile.TemporaryDirectory() as tmp_dir:
        json_file = Path(tmp_dir) / "cookies.json"
        netscape_file = Path(tmp_dir) / "cookies.txt"

        # Test JSON
        CookieVault.export_json(sample_cookies, json_file)
        imported = CookieVault.import_json(json_file)
        assert imported[0]["name"] == "cf_clearance"
        assert imported[0]["value"] == "test_clearance_123"

        # Test Netscape
        CookieVault.export_netscape(sample_cookies, netscape_file)
        content = netscape_file.read_text(encoding="utf-8")
        assert ".example.com" in content
        assert "test_clearance_123" in content


def test_user_agent_feed():
    """Verify modern desktop user agent generation."""
    from nodetect.core.ua_feed import UserAgentFeed
    win_ua = UserAgentFeed.get_random_desktop("windows")
    mac_ua = UserAgentFeed.get_random_desktop("mac")
    
    assert "Windows NT" in win_ua
    assert "Macintosh" in mac_ua
    assert "Chrome/" in win_ua
