from core.session import SESSION, BASE_URL
from core.headers import nav_headers, fetch_headers

PUZZLE_URL = f"{BASE_URL}/the_fractured_mirror"
HOME_URL = f"{BASE_URL}/"


async def solve_fractured_mirror():
    page = await SESSION.get(PUZZLE_URL, headers=nav_headers(referer=HOME_URL))
    print(f"Fractured Mirror page: {page.status_code}")

    open_resp = await SESSION.get(
        f"{BASE_URL}/resources/open.html",
        headers=fetch_headers(referer=PUZZLE_URL),
    )
    print(f"Fractured Mirror open.html: {open_resp.status_code}")

    with open("test_results/fractured_mirror_result.html", "w") as f:
        f.write(open_resp.text)

    if open_resp.status_code == 200 and "door slides open" in open_resp.text.lower():
        print("Fractured Mirror solved ✓")
    else:
        print(f"Fractured Mirror failed — {open_resp.text[:120].strip()}")
