from core.session import SESSION, BASE_URL
from core.headers import nav_headers, fetch_headers

PUZZLE_URL = f"{BASE_URL}/the_mirrored_gaze"
HOME_URL = f"{BASE_URL}/"


async def solve_mirrored_gaze():
    page = await SESSION.get(PUZZLE_URL, headers=nav_headers(referer=HOME_URL))
    print(f"Mirrored Gaze page: {page.status_code}")

    open_resp = await SESSION.get(
        f"{BASE_URL}/resources/open.html",
        headers=fetch_headers(referer=PUZZLE_URL),
    )
    print(f"Mirrored Gaze open.html: {open_resp.status_code}")

    with open("test_results/mirrored_gaze_result.html", "w") as f:
        f.write(open_resp.text)

    if open_resp.status_code == 200 and "door slides open" in open_resp.text.lower():
        print("Mirrored Gaze solved ✓")
    else:
        print(f"Mirrored Gaze failed — {open_resp.text[:120].strip()}")
