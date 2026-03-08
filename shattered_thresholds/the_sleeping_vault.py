from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import generate_vault_thumbmark
import time


BASE = "https://bo7.online"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}


def load_thumbmark_script(referer):

    headers = {
        "accept": "*/*",
        "referer": referer,
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": HEADERS["user-agent"]
    }

    SESSION.get(f"{BASE}/resources/thumbmark.js", headers=headers)


def load_vault_resource():

    headers = {
        "accept": "*/*",
        "referer": f"{BASE}/the_sleeping_vault",
        "user-agent": HEADERS["user-agent"]
    }

    SESSION.get(f"{BASE}/resources/open.html", headers=headers)


def send_thumbmark(mysterious, referer, thumbmark, fingerprint):

    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": BASE,
        "referer": referer,
        "user-agent": HEADERS["user-agent"],
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

    time.sleep(0.2)


    headers = HEADERS.copy()
    headers["referer"] = BASE

    resp = SESSION.get(
        f"{BASE}/the_sleeping_vault",
        headers=headers
    )

    print("vault first load:", resp.status_code)

    html = resp.text
    mysterious_vault = extract_mysterious_value(html)

    load_vault_resource()


    load_thumbmark_script(f"{BASE}/the_sleeping_vault")

    send_thumbmark(
        mysterious_vault,
        f"{BASE}/the_sleeping_vault",
        thumbmark,
        fingerprint
    )

    time.sleep(0.2)


    resp2 = SESSION.get(
        f"{BASE}/the_sleeping_vault",
        headers=headers
    )

    print("vault final status:", resp2.status_code)

    if resp2.status_code == 200:
        print("Sleeping Vault solved")
        with open("test_results/sleeping_vault_result.html", "w") as f:
            f.write(resp2.text)
            f.close()
    else:
        print("Sleeping Vault failed")