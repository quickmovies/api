import json
import random
from typing import Any
import requests

OTP_API_URL = "https://apisap.fabindia.com/occ/v2/fabindiab2c/otp/generate"

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
        params = {
            'lang': "en",
            'curr': "INR"
        }

        payload = {
            "mobileDailCode": "+91",
            "mobileNumber": number,
            "isLogin": False,
            "isSignUp": False
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': device["platform"],
            'authorization': "bearer upaiAYPQZNDpFbGToCWYb72xqCM",
            'viewport-width': "360",
            'device-memory': "8",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-dpr': "3",
            'x-anonymous-consents': "%5B%5D",
            'sec-ch-ua-mobile': device["mobile"],
            'sec-ch-viewport-width': "360",
            'downlink': "9.5",
            'ect': "4g",
            'sec-ch-device-memory': "8",
            'dpr': "3",
            'rtt': "0",
            'origin': "https://www.fabindia.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.fabindia.com/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i"
        }

        resp = requests.post(
            OTP_API_URL,
            params=params,
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

