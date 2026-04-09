from core.session import SESSION, BASE_URL
from core.headers import nav_headers, resource_headers, fetch_headers

GATE_URL = f"{BASE_URL}/the_verity_gate"


async def solve_verity_gate():
    page = await SESSION.get(GATE_URL, headers=nav_headers(referer=f"{BASE_URL}/"))
    print(f"Verity Gate page: {page.status_code}")

    await SESSION.get(
        f"{BASE_URL}/resources/the_verity_gate.js?v=1",
        headers=resource_headers(referer=GATE_URL),
    )

    open_resp = await SESSION.get(
        f"{BASE_URL}/resources/open.html",
        headers=fetch_headers(referer=GATE_URL),
    )
    print(f"Verity Gate open.html: {open_resp.status_code}")

    with open("test_results/verity_gate_result.html", "w") as f:
        f.write(open_resp.text)

    if open_resp.status_code == 200 and "door slides open" in open_resp.text.lower():
        print("Verity Gate solved ✓")
    else:
        print("Verity Gate failed")
