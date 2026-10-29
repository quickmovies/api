import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.mrmed.in/sign-in"

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
        # Next.js Server Action array payload format: [phone, uuid, email, name]
        payload_data = [
            number,
            "b13c2eb4-196b-4967-b5f4-8d2bfcec9bb3",
            "njann@gmail.com",
            "Test"
        ]
        payload = json.dumps(payload_data)

        params = {
            'mode': "register",
            'action': "request_medicine"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "text/x-component",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'next-action': "3ba6f2cc8fc96ab2dec240b8e305281d8f0d33f9",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'next-router-state-tree': "%5B%22%22%2C%7B%22children%22%3A%5B%22(auth)%22%2C%7B%22children%22%3A%5B%22sign-in%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fsign-in%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
            'content-type': "text/plain;charset=UTF-8",
            'x-deployment-id': "dpl_5YwurTw6vVei2h4S3JWjAj7A6ecq",
            'origin': "https://www.mrmed.in",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.mrmed.in/sign-in?mode=register&action=request_medicine",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i"
        }

        resp = requests.post(
            OTP_API_URL,
            params=params,
            headers=headers,
            data=payload,
            timeout=15,
        )

        result_text = resp.text

        if resp.ok:
            return {
                "success": True,
                "message": f"OTP request sent to {number}",
                "status_code": resp.status_code,
                "data": {"raw": result_text},
            }
        else:
            return {
                "success": False,
                "message": f"HTTP {resp.status_code}",
                "data": {"raw": result_text},
            }

    except Exception as err:
        return {"success": False, "message": str(err)}

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
