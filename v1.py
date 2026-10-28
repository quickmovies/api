import json
import random
from typing import Any

import requests

OTP_API_URL = "https://www.bikewale.com/api/user/login/otp-request/"


def get_random_device() -> dict[str, str]:
    devices = [
        {"model": "Infinix X6871", "android": "15", "chrome": "131"},
        {"model": "Samsung Galaxy S24", "android": "15", "chrome": "130"},
        {"model": "Redmi Note 13 Pro", "android": "14", "chrome": "129"},
        {"model": "POCO X6 Pro", "android": "14", "chrome": "131"},
        {"model": "Realme GT 6", "android": "15", "chrome": "130"},
        {"model": "Vivo V30", "android": "14", "chrome": "128"},
        {"model": "OnePlus Nord 4", "android": "15", "chrome": "131"},
        {"model": "Motorola Edge 50", "android": "14", "chrome": "129"},
        {"model": "iQOO Z9", "android": "14", "chrome": "130"},
        {"model": "Nothing Phone 2a", "android": "15", "chrome": "131"},
        {"model": "Samsung Galaxy A55", "android": "14", "chrome": "128"},
        {"model": "Xiaomi 14", "android": "15", "chrome": "130"},
        {"model": "Oppo Reno 12", "android": "14", "chrome": "129"},
        {"model": "Tecno Camon 30", "android": "14", "chrome": "131"},
        {"model": "Infinix Note 40", "android": "14", "chrome": "130"},
    ]

    d = random.choice(devices)
    build = f"AP3A.{240000 + random.randint(0, 8999)}.015.A2"

    ua = (
        f"Mozilla/5.0 (Linux; Android {d['android']}; {d['model']} Build/{build}) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{d['chrome']}.0.0.0 "
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
            "mobileNo": number,
            "sourceModule": 14,
        }

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://www.bikewale.com",
            "Referer": "https://www.bikewale.com/",
            "User-Agent": device["userAgent"],
            "sec-ch-ua": device["secChUa"],
            "sec-ch-ua-platform": device["platform"],
            "sec-ch-ua-mobile": device["mobile"],
            "x-requested-with": "mark.via.gp",
            "serverdomain": "CarWale",
        }

        otp_res = requests.post(
            OTP_API_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        try:
            result_data = otp_res.json()
        except json.JSONDecodeError:
            result_data = {"raw": otp_res.text}

        if otp_res.ok:
            return {
                "success": True,
                "message": f"OTP sent to {number}",
                "data": result_data,
            }
        else:
            return {
                "success": False,
                "message": f"HTTP {otp_res.status_code}",
                "data": result_data,
            }

    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
