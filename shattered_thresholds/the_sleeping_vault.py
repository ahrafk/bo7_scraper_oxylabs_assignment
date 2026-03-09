from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import generate_vault_thumbmark
import time


BASE = "https://bo7.online"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"


def load_thumbmark_script(referer):

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": referer,
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": UA
    }

    SESSION.get(f"{BASE}/resources/thumbmark.js", headers=headers)


def load_vault_resource():

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": f"{BASE}/the_sleeping_vault",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": UA
    }

    SESSION.get(f"{BASE}/resources/open.html", headers=headers)


def send_thumbmark(mysterious, referer, thumbmark, fingerprint):

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": BASE,
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": referer,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": UA,
        "x-mysterious-value": mysterious
    }

    payload = {
        "thumbmark_id": thumbmark,
        "fingerprint": fingerprint
    }

    resp = SESSION.post(
        f"{BASE}/api/thumbmark",
        headers=headers,
        json=payload
    )

    print("thumbmark status:", resp.status_code)


def solve_sleeping_vault():

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

    time.sleep(0.7)

    vault_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": BASE,
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": UA
    }

    resp = SESSION.get(
        f"{BASE}/the_sleeping_vault",
        headers=vault_headers
    )

    print("vault first load:", resp.status_code)

    html = resp.text
    mysterious_vault = extract_mysterious_value(html)

    load_vault_resource()

    load_thumbmark_script(f"{BASE}/the_sleeping_vault")

    time.sleep(0.7)

    send_thumbmark(
        mysterious_vault,
        f"{BASE}/the_sleeping_vault",
        thumbmark,
        fingerprint
    )

    time.sleep(0.7)

    resp2 = SESSION.get(
        f"{BASE}/the_sleeping_vault",
        headers=vault_headers
    )

    print("vault final status:", resp2.status_code)

    open_resp = SESSION.get(
        f"{BASE}/resources/open.html",
        headers={
            "accept": "*/*",
            "referer": f"{BASE}/the_sleeping_vault",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": UA
        }
    )

    if open_resp.status_code == 200 and "The door slides open" in open_resp.text:

        print("Sleeping Vault solved")

        with open("test_results/sleeping_vault_result.html", "w") as f:
            f.write(open_resp.text)

    else:
        print("Sleeping Vault failed")