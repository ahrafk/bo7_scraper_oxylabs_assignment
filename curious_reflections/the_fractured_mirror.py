from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import send_thumbmark
import time


def solve_fractured_mirror():

    homepage_html = get_bo7_homepage()

    mysterious = extract_mysterious_value(homepage_html)

    thumb = send_thumbmark(
        mysterious,
        "https://bo7.online/"
    )

    print("thumbmark status:", thumb.status_code)

    time.sleep(0.3)

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i",
        "referer": "https://bo7.online/",
        "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    }

    resp = SESSION.get(
        "https://bo7.online/the_fractured_mirror",
        headers=headers
    )

    print("mirror page status:", resp.status_code)
    with open("test_results/fractured_mirror_result.html", "w") as f:
        f.write(resp.text)
        f.close()

    html = resp.text

    if "Mirror Aligns" in html:
        print("Fractured mirror solved")