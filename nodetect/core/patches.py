"""
Deep JS Runtime Evasions, Client Hints Mockup, WebRTC Shield, and CDP Neutralizers.
"""
import json
from nodetect.profile.fingerprint import Fingerprint


def build_stealth_script(fp: Fingerprint) -> str:
    """
    Compiles enterprise-grade evasion script for Playwright page contexts.
    """
    fp_json = json.dumps(fp.to_dict())

    return f"""
(() => {{
    'use strict';
    const FP = {fp_json};

    // --- 0. Native Function ToString Obfuscation ---
    const nativeFnMap = new WeakSet();
    const origToString = Function.prototype.toString;
    Function.prototype.toString = function() {{
        if (nativeFnMap.has(this)) {{
            return 'function ' + (this.name || '') + '() {{ [native code] }}';
        }}
        return origToString.apply(this, arguments);
    }};
    nativeFnMap.add(Function.prototype.toString);

    function markNative(fn) {{
        nativeFnMap.add(fn);
        return fn;
    }}

    // --- 1. Eradicate navigator.webdriver ---
    try {{
        delete Navigator.prototype.webdriver;
    }} catch (e) {{}}
    try {{
        delete navigator.webdriver;
    }} catch (e) {{}}

    // --- 2. Hardware and Platform Identity ---
    try {{
        Object.defineProperty(Navigator.prototype, 'hardwareConcurrency', {{
            get: markNative(function() {{ return FP.hardware_concurrency; }}),
            configurable: true
        }});
        Object.defineProperty(Navigator.prototype, 'deviceMemory', {{
            get: markNative(function() {{ return FP.device_memory; }}),
            configurable: true
        }});
        Object.defineProperty(Navigator.prototype, 'platform', {{
            get: markNative(function() {{ return FP.platform; }}),
            configurable: true
        }});
        Object.defineProperty(Navigator.prototype, 'languages', {{
            get: markNative(function() {{ return FP.languages; }}),
            configurable: true
        }});
    }} catch (e) {{}}

    // --- 3. Full NavigatorUAData & Client Hints Simulation ---
    try {{
        if (FP.client_hints) {{
            const hints = FP.client_hints;
            class NavigatorUAData {{
                constructor() {{
                    this.brands = hints.brands || [];
                    this.mobile = false;
                    this.platform = hints.platform || "Windows";
                }}
                getHighEntropyValues(requestedHints) {{
                    return new Promise((resolve) => {{
                        const result = {{
                            architecture: hints.architecture || "x86",
                            bitness: hints.bitness || "64",
                            brands: hints.brands || [],
                            fullVersionList: hints.fullVersionList || hints.brands || [],
                            mobile: false,
                            model: hints.model || "",
                            platform: hints.platform || "Windows",
                            platformVersion: hints.platformVersion || "15.0.0",
                            wow64: hints.wow64 || false
                        }};
                        resolve(result);
                    }});
                }}
                toJSON() {{
                    return {{
                        brands: this.brands,
                        mobile: this.mobile,
                        platform: this.platform
                    }};
                }}
            }}
            markNative(NavigatorUAData.prototype.getHighEntropyValues);
            markNative(NavigatorUAData.prototype.toJSON);

            const uaDataInstance = new NavigatorUAData();
            Object.defineProperty(Navigator.prototype, 'userAgentData', {{
                get: markNative(function() {{ return uaDataInstance; }}),
                configurable: true,
                enumerable: true
            }});
        }}
    }} catch (e) {{}}

    // --- 4. Authentic window.chrome Object ---
    try {{
        if (!window.chrome) {{
            window.chrome = {{}};
        }}
        if (!window.chrome.runtime) {{
            window.chrome.runtime = {{
                OnInstalledReason: {{ CHROME_UPDATE: "chrome_update", INSTALL: "install", SHARED_MODULE_UPDATE: "shared_module_update", UPDATE: "update" }},
                PlatformArch: {{ ARM: "arm", ARM64: "arm64", MIPS: "mips", MIPS64: "mips64", X86_32: "x86-32", X86_64: "x86-64" }},
                PlatformNaclArch: {{ ARM: "arm", MIPS: "mips", MIPS64: "mips64", X86_32: "x86-32", X86_64: "x86-64" }},
                PlatformOs: {{ ANDROID: "android", CROS: "cros", LINUX: "linux", MAC: "mac", OPENBSD: "openbsd", WIN: "win" }},
                RequestUpdateCheckStatus: {{ NO_UPDATE: "no_update", THROTTLED: "throttled", UPDATE_AVAILABLE: "update_available" }},
                connect: markNative(function() {{ return {{ disconnect: function() {{}}, onDisconnect: {{ addListener: function() {{}} }}, onMessage: {{ addListener: function() {{}} }}, postMessage: function() {{}} }}; }}),
                sendMessage: markNative(function() {{}})
            }};
        }}
        if (!window.chrome.csi) {{
            window.chrome.csi = markNative(function() {{ return {{ startE: Date.now(), onloadT: Date.now() + 10, pageT: 15, tran: 15 }}; }});
        }}
        if (!window.chrome.loadTimes) {{
            window.chrome.loadTimes = markNative(function() {{
                return {{
                    requestTime: Date.now() / 1000,
                    startLoadTime: Date.now() / 1000,
                    commitLoadTime: Date.now() / 1000 + 0.05,
                    finishDocumentLoadTime: Date.now() / 1000 + 0.1,
                    firstPaintTime: Date.now() / 1000 + 0.08,
                    firstPaintAfterLoadTime: 0,
                    navigationType: "Other",
                    wasFetchedViaSpdy: true,
                    wasNpnNegotiated: true,
                    npnNegotiatedProtocol: "h2",
                    wasAlternateProtocolAvailable: false,
                    connectionInfo: "h2"
                }};
            }});
        }}
    }} catch (e) {{}}

    // --- 5. WebGL Deep Hardware Parameter & Shader Precision Spoofing ---
    const patchWebGL = (target) => {{
        if (!target) return;
        const origGetParameter = target.prototype.getParameter;
        target.prototype.getParameter = markNative(function(param) {{
            if (param === 37445) return FP.webgl_unmasked_vendor;   // UNMASKED_VENDOR_WEBGL
            if (param === 37446) return FP.webgl_unmasked_renderer; // UNMASKED_RENDERER_WEBGL
            if (param === 7936) return FP.webgl_vendor;             // VENDOR
            if (param === 7937) return FP.webgl_renderer;           // RENDERER

            // If a deep harvested parameter map is supplied, return exact hardware value
            if (FP.webgl_params && FP.webgl_params[param] !== undefined) {{
                const val = FP.webgl_params[param];
                if (Array.isArray(val)) {{
                    return new Float32Array(val);
                }}
                return val;
            }}
            return origGetParameter.apply(this, arguments);
        }});

        // Shader precision format spoofing
        if (FP.shader_precision) {{
            const origGetShaderPrecisionFormat = target.prototype.getShaderPrecisionFormat;
            target.prototype.getShaderPrecisionFormat = markNative(function(shaderType, precisionType) {{
                // Map numeric types
                const stageMap = {{ 35633: "VERTEX_SHADER", 35632: "FRAGMENT_SHADER" }};
                const typeMap = {{ 36336: "LOW_FLOAT", 36337: "MEDIUM_FLOAT", 36338: "HIGH_FLOAT", 36339: "LOW_INT", 36340: "MEDIUM_INT", 36341: "HIGH_INT" }};
                const key = (stageMap[shaderType] || shaderType) + "." + (typeMap[precisionType] || precisionType);
                if (FP.shader_precision[key]) {{
                    const prec = FP.shader_precision[key];
                    return {{
                        rangeMin: prec.rangeMin,
                        rangeMax: prec.rangeMax,
                        precision: prec.precision
                    }};
                }}
                return origGetShaderPrecisionFormat.apply(this, arguments);
            }});
        }}

        // Extensions spoofing
        if (FP.webgl_extensions && FP.webgl_extensions.length > 0) {{
            target.prototype.getSupportedExtensions = markNative(function() {{
                return FP.webgl_extensions;
            }});
        }}
    }};
    try {{
        patchWebGL(window.WebGLRenderingContext);
        patchWebGL(window.WebGL2RenderingContext);
    }} catch (e) {{}}

    // --- 6. Canvas Fingerprint Noise Perturbation ---
    try {{
        const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = markNative(function() {{
            const ctx = this.getContext('2d');
            if (ctx && this.width > 0 && this.height > 0) {{
                try {{
                    const imgData = ctx.getImageData(0, 0, Math.min(this.width, 16), Math.min(this.height, 16));
                    for (let i = 0; i < imgData.data.length; i += 4) {{
                        imgData.data[i] = Math.min(255, Math.max(0, imgData.data[i] + Math.round(FP.canvas_noise_seed * 10000) % 2));
                    }}
                    ctx.putImageData(imgData, 0, 0);
                }} catch (e) {{}}
            }}
            return origToDataURL.apply(this, arguments);
        }});
    }} catch (e) {{}}

    // --- 7. AudioContext Frequency Jitter ---
    try {{
        if (window.AudioBuffer) {{
            const origGetChannelData = AudioBuffer.prototype.getChannelData;
            AudioBuffer.prototype.getChannelData = markNative(function() {{
                const data = origGetChannelData.apply(this, arguments);
                for (let i = 0; i < data.length; i += 100) {{
                    data[i] += FP.audio_noise_seed;
                }}
                return data;
            }});
        }}
    }} catch (e) {{}}

    // --- 8. Authentic PluginArray and Plugin Prototypes ---
    try {{
        if (window.PluginArray && window.Plugin) {{
            const pluginData = [
                {{ name: "PDF Viewer", filename: "internal-pdf-viewer", description: "Portable Document Format" }},
                {{ name: "Chrome PDF Viewer", filename: "internal-pdf-viewer", description: "Portable Document Format" }},
                {{ name: "Chromium PDF Viewer", filename: "internal-pdf-viewer", description: "Portable Document Format" }}
            ];
            const fakePlugins = Object.create(PluginArray.prototype);
            const pluginList = [];

            pluginData.forEach((p, idx) => {{
                const plugin = Object.create(Plugin.prototype);
                Object.defineProperties(plugin, {{
                    name: {{ value: p.name, enumerable: true }},
                    filename: {{ value: p.filename, enumerable: true }},
                    description: {{ value: p.description, enumerable: true }},
                    length: {{ value: 1, enumerable: true }}
                }});
                try {{ plugin[Symbol.toStringTag] = 'Plugin'; }} catch (e) {{}}
                fakePlugins[idx] = plugin;
                fakePlugins[p.name] = plugin;
                pluginList.push(plugin);
            }});

            Object.defineProperties(fakePlugins, {{
                length: {{ value: pluginList.length, enumerable: true }},
                item: {{ value: markNative((i) => pluginList[i] || null), enumerable: false }},
                namedItem: {{ value: markNative((n) => pluginList.find(p => p.name === n) || null), enumerable: false }},
                refresh: {{ value: markNative(() => {{}}), enumerable: false }}
            }});

            try {{ fakePlugins[Symbol.toStringTag] = 'PluginArray'; }} catch (e) {{}}

            Object.defineProperty(Navigator.prototype, 'plugins', {{
                get: markNative(function() {{ return fakePlugins; }}),
                configurable: true,
                enumerable: true
            }});
        }}
    }} catch (e) {{}}

    // --- 9. WebRTC Real IP Leak Shield ---
    try {{
        if (window.RTCPeerConnection) {{
            const origCreateOffer = RTCPeerConnection.prototype.createOffer;
            const rtcRegex = new RegExp("a=candidate:.*typ host.*", "g");
            RTCPeerConnection.prototype.createOffer = markNative(function() {{
                return origCreateOffer.apply(this, arguments).then(offer => {{
                    if (offer && offer.sdp) {{
                        offer.sdp = offer.sdp.replace(rtcRegex, '');
                    }}
                    return offer;
                }});
            }});
        }}
    }} catch (e) {{}}

    // --- 10. Error Stack Sanitization (CDP / Playwright Trace Scrub) ---
    try {{
        const origPrepareStackTrace = Error.prepareStackTrace;
        Error.prepareStackTrace = markNative(function(err, stack) {{
            if (typeof origPrepareStackTrace === 'function') {{
                return origPrepareStackTrace(err, stack);
            }}
            return stack;
        }});

        const origStackDescriptor = Object.getOwnPropertyDescriptor(Error.prototype, 'stack');
        if (origStackDescriptor && origStackDescriptor.get) {{
            Object.defineProperty(Error.prototype, 'stack', {{
                get: markNative(function() {{
                    const rawStack = origStackDescriptor.get.apply(this);
                    if (typeof rawStack === 'string') {{
                        const nl = String.fromCharCode(10);
                        return rawStack
                            .split(nl)
                            .filter(line => !line.includes('__playwright') && !line.includes('__pw'))
                            .join(nl);
                    }}
                    return rawStack;
                }})
            }});
        }}
    }} catch (e) {{}}

    // --- 11. Iframe Stealth Propagation ---
    try {{
        const iframeProto = HTMLIFrameElement.prototype;
        const origContentWindow = Object.getOwnPropertyDescriptor(iframeProto, 'contentWindow')?.get;
        if (origContentWindow) {{
            Object.defineProperty(iframeProto, 'contentWindow', {{
                get: markNative(function() {{
                    const win = origContentWindow.apply(this);
                    try {{
                        if (win && win.Navigator && win.Navigator.prototype) {{
                            delete win.Navigator.prototype.webdriver;
                        }}
                    }} catch (crossOriginErr) {{
                        // Cross-origin iframe: browser SOP prevents cross-window property access
                    }}
                    return win;
                }})
            }});
        }}
    }} catch (e) {{}}

    // --- 12. CDC & Automation Signature Scrubbing ---
    try {{
        const cdcPattern = new RegExp("^(cdc_|__playwright|__pw)", "i");
        for (const prop in window) {{
            if (cdcPattern.test(prop)) delete window[prop];
        }}
        for (const prop in document) {{
            if (cdcPattern.test(prop)) delete document[prop];
        }}
    }} catch (e) {{}}

    // --- 13. Network Connection API ---
    try {{
        if (!navigator.connection) {{
            const fakeConnection = {{
                downlink: 10,
                effectiveType: "4g",
                rtt: 50,
                saveData: false,
                onchange: null
            }};
            Object.defineProperty(Navigator.prototype, 'connection', {{
                get: markNative(function() {{ return fakeConnection; }}),
                configurable: true,
                enumerable: true
            }});
        }}
    }} catch (e) {{}}

    // --- 14. Outer Window Geometry Realism (Akamai / DataDome Frame Fix) ---
    try {{
        const isMac = FP.platform && FP.platform.includes('Mac');
        const frameHeight = isMac ? 78 : 88;
        const frameWidth = isMac ? 0 : 16;
        Object.defineProperty(window, 'outerWidth', {{
            get: markNative(function() {{ return (window.innerWidth || FP.viewport_width) + frameWidth; }}),
            configurable: true
        }});
        Object.defineProperty(window, 'outerHeight', {{
            get: markNative(function() {{ return (window.innerHeight || FP.viewport_height) + frameHeight; }}),
            configurable: true
        }});
    }} catch (e) {{}}

    // --- 15. SpeechSynthesis Voices Engine ---
    try {{
        if (window.speechSynthesis) {{
            const isMac = FP.platform && FP.platform.includes('Mac');
            const fakeVoices = isMac ? [
                {{ name: "Samantha", lang: "en-US", default: true, localService: true, voiceURI: "Samantha" }},
                {{ name: "Alex", lang: "en-US", default: false, localService: true, voiceURI: "Alex" }}
            ] : [
                {{ name: "Microsoft David - English (United States)", lang: "en-US", default: true, localService: true, voiceURI: "Microsoft David - English (United States)" }},
                {{ name: "Microsoft Zira - English (United States)", lang: "en-US", default: false, localService: true, voiceURI: "Microsoft Zira - English (United States)" }}
            ];
            window.speechSynthesis.getVoices = markNative(function() {{
                return fakeVoices;
            }});
        }}
    }} catch (e) {{}}

    // --- 16. Document Visibility & Focus Lock (Anti-Throttling) ---
    try {{
        Object.defineProperty(document, 'hidden', {{
            get: markNative(function() {{ return false; }}),
            configurable: true
        }});
        Object.defineProperty(document, 'visibilityState', {{
            get: markNative(function() {{ return 'visible'; }}),
            configurable: true
        }});
        document.hasFocus = markNative(function() {{
            return true;
        }});
    }} catch (e) {{}}

    // --- 17. CSS Media Queries (Hover & Fine Pointer Desktop Emulation) ---
    try {{
        const origMatchMedia = window.matchMedia;
        window.matchMedia = markNative(function(query) {{
            const res = origMatchMedia.apply(this, arguments);
            if (query && (query.includes('hover: hover') || query.includes('pointer: fine') || query.includes('pointer:fine'))) {{
                return Object.assign({{}}, res, {{ matches: true }});
            }}
            return res;
        }});
    }} catch (e) {{}}

    // --- 18. Battery Status API Simulation ---
    try {{
        if (navigator.getBattery) {{
            const fakeBattery = {{
                charging: false,
                chargingTime: Infinity,
                dischargingTime: 14400,
                level: 0.84,
                onchargingchange: null,
                onchargingtimechange: null,
                ondischargingtimechange: null,
                onlevelchange: null
            }};
            navigator.getBattery = markNative(function() {{
                return Promise.resolve(fakeBattery);
            }});
        }}
    }} catch (e) {{}}

}})();
"""
