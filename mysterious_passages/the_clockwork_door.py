from core.session import SESSION, BASE_URL
from core.headers import nav_headers


async def solve_clockwork_door():
    resp = await SESSION.get(
        f"{BASE_URL}/the_clockwork_door",
        headers=nav_headers(referer=f"{BASE_URL}/"),
    )

    print(f"Clockwork Door: {resp.status_code}")

    with open("test_results/clockwork_door_result.html", "w") as f:
        f.write(resp.text)

    if resp.status_code == 200 and "door slides open" in resp.text.lower():
        print("Clockwork Door solved ✓")
    else:
        print("Clockwork Door failed")
