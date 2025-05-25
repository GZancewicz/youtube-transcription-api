import os

def get_proxies():
    proxy_url = os.getenv("PROXY_URL")
    if not proxy_url:
        raise RuntimeError("Missing required environment variable: PROXY_URL")
    return {
        "http": proxy_url,
        "https": proxy_url
    } 