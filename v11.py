import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.davaindia.com/login"

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
        # Next.js Server Action payload format
        payload_data = [
            {
                "identifierType": "mobile",
                "phoneNumber": f"+91{number}",
                "email": "",
                "isWeb": True
            },
            {
                "client": "$T",
                "meta": "$undefined",
                "mutationKey": "$undefined"
            }
        ]
        payload = json.dumps(payload_data)

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "text/x-component",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'next-action': "7ffa1ec709884dee456aece1460195b9427792d944",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'next-router-state-tree': "%5B%22%22%2C%7B%22children%22%3A%5B%22(screens)%22%2C%7B%22children%22%3A%5B%22(auth)%22%2C%7B%22children%22%3A%5B%22login%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
            'content-type': "text/plain;charset=UTF-8",
            'origin': "https://www.davaindia.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.davaindia.com/login",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "__Host-authjs.csrf-token=b191a0bdd2ddd2d593385e91a3e36607a07381b03d1be1dde44cce8bfd924f37%7C4e3243082ae8e52ae083dc896a3508aeae1a93b8075e4a0a977638a60f1cde9b; __Secure-authjs.callback-url=https%3A%2F%2Flocalhost%3A3001; WZRK_S_WR9-7Z6-9K7Z=%7B%22p%22%3A5%7D"
        }

        resp = requests.post(
            OTP_API_URL,
            headers=headers,
            data=payload,
            timeout=15,
        )

        result_text = resp.text

        if resp.ok:
            return {
                "success": True,
                "message": f"OTP request sent to +91{number}",
                "status_code": resp.status_code,
                "data": result_text,
            }
        else:
            return {
                "success": False,
                "message": f"HTTP {resp.status_code}",
                "data": result_text,
            }

    except Exception as err:
        return {"success": False, "message": str(err)}

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
