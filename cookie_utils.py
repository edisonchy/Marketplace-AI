import json

def sanitize_cookies(raw_cookies):
    for cookie in raw_cookies:
        cookie.pop("id", None)
        cookie.pop("storeId", None)
        cookie.pop("hostOnly", None)
        cookie.pop("session", None)
        if cookie.get("sameSite") not in ["Strict", "Lax", "None"]:
            cookie["sameSite"] = "Lax"
    return raw_cookies

def load_cookies(file_path="cookies.json"):
    with open(file_path, "r") as f:
        return json.load(f)