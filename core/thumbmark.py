from core.session import SESSION, BASE_URL
from core.headers import UA, SEC_CH_UA


async def post_thumbmark(mysterious_value: str, referer: str) -> None:
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": BASE_URL,
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": referer,
        "sec-ch-ua": SEC_CH_UA,
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": UA,
        "x-mysterious-value": mysterious_value,
    }

    payload = {
        "thumbmark_id": "00000000000000000000000000000000",
        "fingerprint": {
            "system": {"platform": "MacIntel", "hardwareConcurrency": 8},
            "screen": {"colorDepth": 24, "is_touchscreen": False},
        },
    }

    resp = await SESSION.post(
        f"{BASE_URL}/api/thumbmark",
        headers=headers,
        json=payload,
    )
    print(f"  thumbmark POST ({referer}): {resp.status_code}")
