from core.session import SESSION, BASE_URL
from core.headers import nav_headers


async def visit_homepage():
    response = await SESSION.get(BASE_URL + "/", headers=nav_headers(fetch_site="none"))
    if response.status_code == 200:
        print("Homepage loaded.")
    else:
        print(f"Homepage returned {response.status_code}")
    return response
