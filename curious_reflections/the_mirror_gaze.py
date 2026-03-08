from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import generate_mirror_thumbmark
import time


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

    SESSION.get(
        "https://bo7.online/resources/thumbmark.js",
        headers=headers
    )


def send_thumbmark(mysterious_value, referer, thumbmark, fingerprint):

    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://bo7.online",
        "referer": referer,
        "user-agent": HEADERS["user-agent"],
        "x-mysterious-value": mysterious_value
    }

    payload = {
        "thumbmark_id": thumbmark,
        "fingerprint": fingerprint
    }

    resp = SESSION.post(
        "https://bo7.online/api/thumbmark",
        headers=headers,
        json=payload
    )

    print("thumbmark status:", resp.status_code)

    return resp


def solve_mirrored_gaze():

    thumbmark, fingerprint = generate_mirror_thumbmark()

    homepage_html = get_bo7_homepage()

    mysterious_home = extract_mysterious_value(homepage_html)

    load_thumbmark_script("https://bo7.online/")

    send_thumbmark(
        mysterious_home,
        "https://bo7.online/",
        thumbmark,
        fingerprint
    )

    time.sleep(0.2)

    headers = HEADERS.copy()
    headers["referer"] = "https://bo7.online/"

    resp = SESSION.get(
        "https://bo7.online/the_mirrored_gaze",
        headers=headers
    )

    print("mirrored gaze first load:", resp.status_code)

    html = resp.text

    mysterious_page = extract_mysterious_value(html)

    load_thumbmark_script("https://bo7.online/the_mirrored_gaze")

    send_thumbmark(
        mysterious_page,
        "https://bo7.online/the_mirrored_gaze",
        thumbmark,
        fingerprint
    )

    time.sleep(0.2)

    resp2 = SESSION.get(
        "https://bo7.online/the_mirrored_gaze",
        headers=headers
    )

    print("mirrored gaze final status:", resp2.status_code)
    with open("test_results/mirrored_gaze_result.html", "w") as f:
        f.write(resp2.text)
        f.close()

    if resp2.status_code == 200:
        print("Mirrored Gaze solved ✅")
    else:
        print("Mirrored Gaze failed ❌")