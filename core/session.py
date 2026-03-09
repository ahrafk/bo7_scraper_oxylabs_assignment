from curl_cffi import requests

BASE_URL = "https://bo7.online/"
proxy_url = (
    f"http://ahrafkhatri7gmailcom-country-de:_S0rqc7c@proxy.mrscraper.com:10000"
)
proxy_url_https = (
    f"http://ahrafkhatri7gmailcom-country-de:_S0rqc7c@proxy.mrscraper.com:10000"
)
proxies = {
    "http": proxy_url,
    "https": proxy_url_https,
}

SESSION = requests.Session(
    impersonate="chrome",
    proxies=proxies
)

r = SESSION.get("https://httpbin.org/ip")

print(r.text)