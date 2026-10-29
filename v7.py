import json
import random
import uuid
from typing import Any
from urllib.parse import unquote

import requests

OTP_API_URL = "https://www.pantaloons.com/api/abfrl"


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

    # ===== Values taken from your successful capture =====
    device_id = "ca32bedf-30f2-482b-8f57-390971758b9a"
    device_token = "cf1a35a06ab15d01bc245672505c436b.1793202522"
    session_id = "cf1a35a06ab15d01bc245672505c436b"
    body_hash = "609013b78050ae2da4a1eafba6bab6ab"

    # JWT from registerData cookie
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlblBheWxvYWQiOnsiZGV2aWNlSWQiOiJjYTMyYmVkZi0zMGYyLTQ4MmItOGY1Ny0zOTA5NzE3NThiOWEifSwiaWF0IjoxNzkzMjAyNTIyfQ.NyTTwVPDEZckg6NGhYWBV8ij-VPOMmh7ylJI2GDFXS0"

    try:
        payload = {
            "method": "POST",
            "data": {
                "brand": "pantaloons",
                "validateHash": False,
                "utmSource": "gp",
                "version": 3.4,
                "geoLocation": {"latitude": 343},
                "deviceType": "mobile",
                "fcmToken": "111",
                "mobile": number,
                "mode": "verify",
                "cartId": 0,
                "customerId": 0,
                "sliderSource": "-1",
                "cartOperation": "add",
                "deviceId": device_id,
                "deviceToken": device_token,
                "sessionId": session_id,
                "hash": body_hash,
            },
            "storeKey": "FETCH_SEND_OTP",
            "pathWithQuery": "/common/sendOTP",
            "baseType": "API",
        }

        headers = {
            "User-Agent": device["userAgent"],
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": device["platform"],
            "sec-ch-ua": device["secChUa"],
            "sec-ch-ua-mobile": device["mobile"],
            "origin": "https://www.pantaloons.com",
            "x-requested-with": "mark.via.gp",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.pantaloons.com/",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i",
            # ===== This was missing =====
            "Authorization": f"Bearer {jwt_token}",
        }

        cookies = {
            "registerDevice": device_id,
            "registerData": json.dumps({
                "deviceToken": device_token,
                "token": jwt_token,
                "hash": "fd5f1d78efbe5ae6e8d34c42d64b7d00.f55f42165628e2ad4364f712c0cfe3ec"
            }),
        }

        resp = requests.post(
            OTP_API_URL,
            headers=headers,
            json=payload,
            cookies=cookies,
            timeout=20,
        )

        try:
            result_data = resp.json()
        except Exception:
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
