import json
import mmh3

from core.session import SESSION
from core.fingerprint import get_fingerprint


def generate_thumbmark():

    fingerprint = get_fingerprint()

    fingerprint_str = json.dumps(
        fingerprint,
        separators=(",", ":")
    )

    thumbmark_hash = mmh3.hash128(
        fingerprint_str,
        signed=False
    )

    return format(thumbmark_hash, "032x"), fingerprint


def send_thumbmark(mysterious_value, referer):

    thumbmark, fingerprint = generate_thumbmark()

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://bo7.online",
        "priority": "u=1, i",
        "referer": referer,
        "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "x-mysterious-value": mysterious_value,
    }

    payload = {
        "thumbmark_id": thumbmark,
        "fingerprint": fingerprint
    }

    response = SESSION.post(
        "https://bo7.online/api/thumbmark",
        headers=headers,
        json=payload
    )

    print(f"response status for {referer}: {response.status_code}")

    return response

def send_mirror_thumbmark(mysterious_value, referer):

    fingerprint = get_fingerprint()

    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://bo7.online",
        "referer": referer,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "x-mysterious-value": mysterious_value,
    }

    payload = {
        "thumbmark_id": "e73b88b7fc7f02b5a5fde12816afde6d",
        "fingerprint": fingerprint
    }

    resp = SESSION.post(
        "https://bo7.online/api/thumbmark",
        headers=headers,
        json=payload
    )

    print("mirror thumbmark status:", resp.status_code)

    return resp

from core.fingerprint import get_fingerprint


def generate_mirror_thumbmark():

    fingerprint = get_fingerprint()

    fingerprint_str = json.dumps(
        fingerprint,
        separators=(",", ":"),
        sort_keys=True
    )

    thumbmark = format(
        mmh3.hash128(fingerprint_str, signed=False),
        "032x"
    )

    return thumbmark, fingerprint

def generate_vault_thumbmark():

    thumbmark = "c241becd64841177480d464f53236101"

    fingerprint = {
        "audio": {
            "sampleHash": 1168.9068228197468,
            "maxChannels": 1,
            "channelCountMode": "max"
        },
        "canvas": {
            "commonPixelsHash": "a2f82ea380fbe5afb2ff17e951074312"
        },
        "fonts": {
            "Arial Black": 531.9140625,
            "Comic Sans MS": 462.4453125,
            "Courier": 432.0703125,
            "Courier New": 432.0703125,
            "Georgia": 475.2421875,
            "Impact": 395.54296875,
            "Noto Sans": 472.03216552734375,
            "Quicksand": 460.5841979980469,
            "Trebuchet MS": 428.90625,
            "Ubuntu": 458.7841796875,
            "Verdana": 486.5625
        },
        "hardware": {
            "videocard": {
                "vendor": "WebKit",
                "renderer": "WebKit WebGL",
                "version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
                "shadingLanguageVersion": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)"
            },
            "architecture": 255,
            "deviceMemory": "8",
            "jsHeapSizeLimit": 4294967296
        },
        "locales": {
            "languages": "en-US",
            "timezone": "Asia/Calcutta"
        },
        "math": {
            "acos": 1.0471975511965979,
            "asin": -9.614302481290016e-17,
            "cos": -4.854249971455313e-16,
            "largeCos": 0.7639704044417283,
            "largeSin": -0.6452512852657808,
            "largeTan": -0.8446024630198843,
            "sin": -1.9461946644816207e-16,
            "tan": 6.980860926542689e-14
        },
        "plugins": {
            "plugins": [
                "PDF Viewer|internal-pdf-viewer|Portable Document Format",
                "Chrome PDF Viewer|internal-pdf-viewer|Portable Document Format",
                "Chromium PDF Viewer|internal-pdf-viewer|Portable Document Format",
                "Microsoft Edge PDF Viewer|internal-pdf-viewer|Portable Document Format",
                "WebKit built-in PDF|internal-pdf-viewer|Portable Document Format"
            ]
        },
        "screen": {
            "is_touchscreen": False,
            "maxTouchPoints": 0,
            "colorDepth": 24,
            "mediaMatches": [
                "prefers-contrast: no-preference",
                "any-hover: hover",
                "any-pointer: fine",
                "pointer: fine",
                "hover: hover",
                "update: fast",
                "prefers-reduced-motion: no-preference",
                "prefers-reduced-transparency: no-preference",
                "scripting: enabled",
                "forced-colors: none"
            ]
        },
        "system": {
            "platform": "Linux x86_64",
            "productSub": "20030107",
            "product": "Gecko",
            "useragent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "hardwareConcurrency": 12,
            "browser": {
                "name": "Chrome",
                "version": "145.0.0.0"
            },
            "mobile": False,
            "applePayVersion": 0,
            "cookieEnabled": True
        },
        "webgl": {
            "commonPixelsHash": "72ec1429cf00d77fb4c381d3950fc0b0"
        }
    }

    return thumbmark, fingerprint