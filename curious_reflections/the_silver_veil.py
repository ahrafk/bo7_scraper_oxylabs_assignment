from core.session import SESSION, BASE_URL
from core.headers import nav_headers


async def solve_silver_veil():
    resp = await SESSION.get(
        f"{BASE_URL}/the_silver_veil",
        headers=nav_headers(referer=f"{BASE_URL}/"),
    )

    print(f"Silver Veil: {resp.status_code}")

    with open("test_results/silver_veil_result.html", "w") as f:
        f.write(resp.text)

    if "Mirror Aligns" in resp.text:
        print("Silver Veil solved ✓")
    else:
        print("Silver Veil failed")
