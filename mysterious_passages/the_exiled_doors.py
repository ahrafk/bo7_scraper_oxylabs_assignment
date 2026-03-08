from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import generate_vault_thumbmark
import time

BASE = "https://bo7.online"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}


def load_thumbmark_script(referer):

    SESSION.get(
        f"{BASE}/resources/thumbmark.js",
        headers={
            "referer": referer,
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "user-agent": HEADERS["user-agent"]
        }
    )


def send_thumbmark(mysterious, referer, thumbmark, fingerprint):

    resp = SESSION.post(
        f"{BASE}/api/thumbmark",
        headers={
            "content-type": "application/json",
            "origin": BASE,
            "referer": referer,
            "x-mysterious-value": mysterious,
            "user-agent": HEADERS["user-agent"]
        },
        json={
            "thumbmark_id": thumbmark,
            "fingerprint": fingerprint
        }
    )

    print("thumbmark status:", resp.status_code)


def solve_exiled_door():

    thumbmark, fingerprint = generate_vault_thumbmark()

    homepage_html = get_bo7_homepage()
    mysterious_home = extract_mysterious_value(homepage_html)

    load_thumbmark_script(BASE)

    send_thumbmark(
        mysterious_home,
        BASE,
        thumbmark,
        fingerprint
    )

    time.sleep(0.2)

    resp = SESSION.get(
        f"{BASE}/the_exiled_door",
        headers={
            **HEADERS,
            "referer": BASE
        }
    )

    print("exiled door first load:", resp.status_code)

    html = resp.text

    mysterious_door = extract_mysterious_value(html)

    load_thumbmark_script(f"{BASE}/the_exiled_door")

    send_thumbmark(
        mysterious_door,
        f"{BASE}/the_exiled_door",
        thumbmark,
        fingerprint
    )

    time.sleep(0.3)

    resp2 = SESSION.get(
        f"{BASE}/the_exiled_door",
        headers={
            **HEADERS,
            "referer": BASE
        }
    )

    print("exiled door final status:", resp2.status_code)

    if resp2.status_code == 200:
        print("Exiled Door solved ✅")
        with open("test_results/exiled_door_result.html", "w") as f:
            f.write(resp2.text)
            f.close()
    else:
        print("Exiled Door failed ❌")