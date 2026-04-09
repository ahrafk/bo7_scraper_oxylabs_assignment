from core.session import SESSION, BASE_URL
from core.headers import nav_headers, fetch_headers

VAULT_URL = f"{BASE_URL}/the_sleeping_vault"


async def solve_sleeping_vault():
    page = await SESSION.get(VAULT_URL, headers=nav_headers(referer=f"{BASE_URL}/"))
    print(f"Sleeping Vault page: {page.status_code}")

    open_resp = await SESSION.get(
        f"{BASE_URL}/resources/open.html",
        headers=fetch_headers(referer=VAULT_URL),
    )
    print(f"Sleeping Vault open.html: {open_resp.status_code}")

    with open("test_results/sleeping_vault_result.html", "w") as f:
        f.write(open_resp.text)

    if open_resp.status_code == 200 and "door slides open" in open_resp.text.lower():
        print("Sleeping Vault solved ✓")
    else:
        print("Sleeping Vault failed")
