import json
import random
from typing import Any

import requests

OTP_API_URL = "https://www.netmeds.com/api/service/application/user/authentication/v1.0/login/otp"


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
            "mobile": number,
            "country_code": "91",
        }

        headers = {
            "Host": "www.netmeds.com",
            "sec-ch-ua-platform": device["platform"],
            "authorization": "Bearer NjVmNTYyYzE1MDRhNTlhNjdmNTI5YWQ0Ol9VLW9oSTRJeQ==",
            "x-location-detail": json.dumps({
                "country_iso_code": "IN",
                "country": "INDIA",
                "pincode": "110001",
                "city": "Delhi",
                "state": "Delhi"
            }),
            "sec-ch-ua": device["secChUa"],
            "sec-ch-ua-mobile": device["mobile"],
            "x-fp-signature": "v1.1:37b0632d189db5579fdf91da1680aa6aa8ecfa0faadc2d885e59a535000dadcb",
            "x-fp-date": "20261028T150444Z",
            "x-fp-sdk-version": "1.10.5-6",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "x-currency-code": "INR",
            "User-Agent": device["userAgent"],
            "Origin": "https://www.netmeds.com",
            "x-requested-with": "mark.via.gp",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Priority": "u=1, i",
        }

        cookies = {
            "_nmsAttr": "NMP-Search-Diagnostic-ADW",
            "_nmsSource": "NMP-Search-Diagnostic-ADW",
            "_nmsMedium": "CPC",
            "_nmsCampaign": "NMP-Search-Diagnostic-DIAADW",
            "_nmstracking": "NMP-Search-Diagnostic-ADW",
            "app_location_details": json.dumps({
                "country": "INDIA",
                "country_iso_code": "IN",
                "pincode": "110001",
                "city": "Delhi",
                "state": "Delhi"
            }),
            "anonymous_id": "b6e7be0dab9d4780b9808698a9dd50f9",
            "old_browser_anonymous_id": "b6e7be0dab9d4780b9808698a9dd50f9",
            "WZRK_S_865-77W-496Z": '{"p":3}',
        }

        resp = requests.post(
            OTP_API_URL,
            headers=headers,
            json=payload,
            cookies=cookies,
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
