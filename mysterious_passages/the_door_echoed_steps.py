from core.session import SESSION, BASE_URL
from core.headers import nav_headers


async def solve_echoed_steps():
    resp = await SESSION.get(
        f"{BASE_URL}/the_door_of_echoed_steps",
        headers=nav_headers(referer=f"{BASE_URL}/"),
    )

    print(f"Echoed Steps: {resp.status_code}")

    with open("test_results/echoed_steps_result.html", "w") as f:
        f.write(resp.text)

    if resp.status_code == 200 and "door slides open" in resp.text.lower():
        print("Echoed Steps solved ✓")
    else:
        print("Echoed Steps failed")
