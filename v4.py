import json
import random
import uuid
from typing import Any

import requests

OTP_API_URL = "https://crystal-live01.aakash.ac.in/java/crystalApi/otp"


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
            "mobile_number": number,
            "source": "AD_DEMO_LEAD",
            "referer": (
                "https://aakashdigital.com/bookdemo"
                "?utm_source=Google_Search_Brand"
                "&utm_medium=Aakash_AD_BD"
                "&utm_content=akash%20online"
                "&utm_campaign=GGL_Search_AD_2026_Brand_ROI_New"
                "&gad_source=1"
                "&gad_campaignid=24362608459"
                "&gbraid=0AAAAADm7PT3dxrQkG3Sfhlkc0NUILYerk"
                "&gclid=EAIaIQobChMIheavof3clwMVW6pmAh2iTjA9EAAYASAAEgJj8_D_BwE"
            ),
            "web_request_id": uuid.uuid4().hex,   # fresh every time
        }

        headers = {
            "Host": "crystal-live01.aakash.ac.in",
            "sec-ch-ua-platform": device["platform"],
            "User-Agent": device["userAgent"],
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": device["secChUa"],
            "Content-Type": "application/json",
            "sec-ch-ua-mobile": device["mobile"],
            "Origin": "https://aakashdigital.com",
            "x-requested-with": "mark.via.gp",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://aakashdigital.com/",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Priority": "u=1, i",
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
