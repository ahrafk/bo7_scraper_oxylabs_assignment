from curl_cffi import requests

BASE_URL = "https://bo7.online/"
# PROXY = "http://91.65.94.20:80"

SESSION = requests.Session(
    impersonate="chrome",
    # proxies={
    #     "http": PROXY,
    #     "https": PROXY
    # }
)

# r = SESSION.get("https://httpbin.org/ip")

# print(r.text)