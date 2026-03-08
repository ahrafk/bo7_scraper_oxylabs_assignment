from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import send_thumbmark


def solve_silver_veil():

    homepage_html = get_bo7_homepage()

    mysterious_home = extract_mysterious_value(homepage_html)

    send_thumbmark(
        mysterious_home,
        "https://bo7.online/"
    )

    SESSION.get("https://bo7.online/")

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://bo7.online/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/145.0.0.0 Safari/537.36"
    }

    resp = SESSION.get(
        "https://bo7.online/the_silver_veil",
        headers=headers
    )

    print("silver veil first load:", resp.status_code)

    html = resp.text

    mysterious_page = extract_mysterious_value(html)

    send_thumbmark(
        mysterious_page,
        "https://bo7.online/the_silver_veil"
    )

    resp2 = SESSION.get(
        "https://bo7.online/the_silver_veil",
        headers=headers
    )

    print("silver veil final status:", resp2.status_code)
    with open("test_results/silver_veil_result.html", "w") as f:
        f.write(resp2.text)
        f.close()

    if "veil" in resp2.text.lower():
        print("Silver Veil solved")