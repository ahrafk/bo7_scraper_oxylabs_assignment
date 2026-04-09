from curl_cffi import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://bo7.online"

PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")

proxy = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxies = {
    "http": proxy,
    "https": proxy,
}

SESSION = requests.AsyncSession(
    impersonate="chrome",
    proxies=proxies,
)

SESSION.cookies.set("wormhole_token", "galactic-cookie-42", domain="bo7.online")
