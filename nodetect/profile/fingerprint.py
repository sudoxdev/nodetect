"""
Deterministic Fingerprint Generator & Harvested Hardware Profile for PhantomVault.
Supports full WebGL GLenum dictionaries, shader precisions, audio context hashes, and Client Hints.
"""
from dataclasses import dataclass, asdict
import hashlib
import json
import random
from typing import Dict, Any, List, Optional

from nodetect.config import WEBGL_PROFILES, SCREEN_RESOLUTIONS, DEFAULT_USER_AGENTS, CLIENT_HINTS_PRESETS


@dataclass
class Fingerprint:
    profile_id: str
    user_agent: str
    platform: str
    viewport_width: int
    viewport_height: int
    screen_width: int
    screen_height: int
    color_depth: int
    device_pixel_ratio: float
    hardware_concurrency: int
    device_memory: int
    languages: List[str]
    webgl_vendor: str
    webgl_renderer: str
    webgl_unmasked_vendor: str
    webgl_unmasked_renderer: str
    canvas_noise_seed: float
    audio_noise_seed: float
    client_hints: Dict[str, Any]
    timezone_id: str = "America/New_York"
    locale: str = "en-US"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    # Advanced Harvested Profiles (from harvest-fp.html)
    webgl_params: Optional[Dict[str, Any]] = None
    shader_precision: Optional[Dict[str, Any]] = None
    webgl_extensions: Optional[List[str]] = None
    audio_hash: Optional[str] = None
    canvas_data_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Fingerprint":
        if "client_hints" not in data:
            data["client_hints"] = CLIENT_HINTS_PRESETS["windows"]
        if "latitude" not in data:
            data["latitude"] = None
        if "longitude" not in data:
            data["longitude"] = None
        if "webgl_params" not in data:
            data["webgl_params"] = None
        if "shader_precision" not in data:
            data["shader_precision"] = None
        if "webgl_extensions" not in data:
            data["webgl_extensions"] = None
        if "audio_hash" not in data:
            data["audio_hash"] = None
        if "canvas_data_url" not in data:
            data["canvas_data_url"] = None
        return cls(**data)

    @classmethod
    def from_harvested_json(cls, profile_id: str, raw_json: Dict[str, Any]) -> "Fingerprint":
        """
        Constructs an ultra-realistic Fingerprint from real browser dump (harvest-fp.html).
        """
        webgl_raw = raw_json.get("webgl", {}) or {}
        screen = raw_json.get("screen", {}) or {}
        ua_data = raw_json.get("uaData", {}) or {}
        audio = raw_json.get("audio", {}) or {}
        canvas = raw_json.get("canvas2d", {}) or {}

        hints = {
            "platform": raw_json.get("platform", "Win32"),
            "brands": ua_data.get("brands", CLIENT_HINTS_PRESETS["windows"]["brands"]),
            "fullVersionList": ua_data.get("highEntropy", {}).get("fullVersionList") if ua_data.get("highEntropy") else CLIENT_HINTS_PRESETS["windows"]["fullVersionList"],
            "architecture": ua_data.get("highEntropy", {}).get("architecture", "x86") if ua_data.get("highEntropy") else "x86",
            "bitness": ua_data.get("highEntropy", {}).get("bitness", "64") if ua_data.get("highEntropy") else "64",
            "model": ua_data.get("highEntropy", {}).get("model", "") if ua_data.get("highEntropy") else "",
            "platformVersion": ua_data.get("highEntropy", {}).get("platformVersion", "15.0.0") if ua_data.get("highEntropy") else "15.0.0",
            "wow64": ua_data.get("highEntropy", {}).get("wow64", False) if ua_data.get("highEntropy") else False
        }

        return cls(
            profile_id=profile_id,
            user_agent=raw_json.get("userAgent", DEFAULT_USER_AGENTS[0]),
            platform=raw_json.get("platform", "Win32"),
            viewport_width=screen.get("w", 1920),
            viewport_height=screen.get("h", 1080),
            screen_width=screen.get("w", 1920),
            screen_height=screen.get("h", 1080),
            color_depth=screen.get("cd", 24),
            device_pixel_ratio=screen.get("dpr", 1.0),
            hardware_concurrency=raw_json.get("hardwareConcurrency", 8),
            device_memory=raw_json.get("deviceMemory", 16),
            languages=raw_json.get("languages", ["en-US", "en"]),
            webgl_vendor=webgl_raw.get("vendor", "Google Inc. (AMD)"),
            webgl_renderer=webgl_raw.get("renderer", "ANGLE (AMD, AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)"),
            webgl_unmasked_vendor=webgl_raw.get("unmaskedVendor", "AMD"),
            webgl_unmasked_renderer=webgl_raw.get("unmaskedRenderer", "AMD Radeon RX 6700 XT"),
            canvas_noise_seed=0.0,
            audio_noise_seed=0.0,
            client_hints=hints,
            timezone_id=raw_json.get("tz", "America/New_York"),
            locale=raw_json.get("language", "en-US"),
            webgl_params=webgl_raw.get("params"),
            shader_precision=webgl_raw.get("precision"),
            webgl_extensions=webgl_raw.get("extensions"),
            audio_hash=audio.get("hash"),
            canvas_data_url=canvas.get("dataURL")
        )

    @classmethod
    def generate(
        cls,
        profile_id: str,
        platform_type: str = "windows",
        timezone: str = "America/New_York",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ) -> "Fingerprint":
        hash_digest = hashlib.sha256(profile_id.encode("utf-8")).hexdigest()
        seed = int(hash_digest[:8], 16)
        rng = random.Random(seed)

        screen = rng.choice(SCREEN_RESOLUTIONS)

        if platform_type == "mac":
            webgl = WEBGL_PROFILES[4]
            ua = DEFAULT_USER_AGENTS[3]
            platform = "MacIntel"
            hints = CLIENT_HINTS_PRESETS["mac"]
        elif platform_type == "linux":
            webgl = rng.choice(WEBGL_PROFILES[:4])
            ua = DEFAULT_USER_AGENTS[4]
            platform = "Linux x86_64"
            hints = CLIENT_HINTS_PRESETS["linux"]
        else:
            webgl = rng.choice(WEBGL_PROFILES[:4])
            ua = rng.choice(DEFAULT_USER_AGENTS[:3])
            platform = "Win32"
            hints = CLIENT_HINTS_PRESETS["windows"]

        cores = rng.choice([4, 6, 8, 12, 16])
        memory = rng.choice([8, 16, 32])

        canvas_seed = (rng.random() - 0.5) * 0.0001
        audio_seed = (rng.random() - 0.5) * 0.0001

        return cls(
            profile_id=profile_id,
            user_agent=ua,
            platform=platform,
            viewport_width=screen["width"],
            viewport_height=screen["height"],
            screen_width=screen["width"],
            screen_height=screen["height"],
            color_depth=screen["color_depth"],
            device_pixel_ratio=screen["pixel_ratio"],
            hardware_concurrency=cores,
            device_memory=memory,
            languages=["en-US", "en"],
            webgl_vendor=webgl["vendor"],
            webgl_renderer=webgl["renderer"],
            webgl_unmasked_vendor=webgl["unmasked_vendor"],
            webgl_unmasked_renderer=webgl["unmasked_renderer"],
            canvas_noise_seed=canvas_seed,
            audio_noise_seed=audio_seed,
            client_hints=hints,
            timezone_id=timezone,
            locale="en-US",
            latitude=latitude,
            longitude=longitude
        )
