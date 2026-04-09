from curl_cffi import requests as cffi_requests
from dotenv import load_dotenv
import os

from core.session import BASE_URL
from core.headers import nav_headers, fetch_headers

load_dotenv()

PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
_proxy = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
_proxies = {"http": _proxy, "https": _proxy}

PUZZLE_URL = f"{BASE_URL}/the_exiled_door"

FRESH_SESSION = cffi_requests.AsyncSession(impersonate="chrome", proxies=_proxies)


async def solve_exiled_door():
    page = await FRESH_SESSION.get(
        PUZZLE_URL,
        headers=nav_headers(fetch_site="none"),
    )
    print(f"Exiled Door page: {page.status_code}")

    open_resp = await FRESH_SESSION.get(
        f"{BASE_URL}/resources/open.html",
        headers=fetch_headers(referer=PUZZLE_URL),
    )
    print(f"Exiled Door open.html: {open_resp.status_code}")

    with open("test_results/exiled_door_result.html", "w") as f:
        f.write(open_resp.text)

    if open_resp.status_code == 200 and "door slides open" in open_resp.text.lower():
        print("Exiled Door solved ✓")
    else:
        print(f"Exiled Door failed — {open_resp.text[:120].strip()}")
