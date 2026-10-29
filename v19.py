import json
import random
from typing import Any
import requests

OTP_API_URL = "https://auth.saya.net.in/api/users/sign-up/or/sign-in"

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
            "phone_number": f"+91{number}",
            "login_by": "phone"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': device["platform"],
            'authorization': "Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJndWVzdF8zNjk2MmRjMC01ZjliLTQwZGUtYTE5Yi04MDY0YTFmM2U4NzYiLCJzaWQiOiI0ZDE1ZjEyNS0yMDVjLTRiODctODZmZi0xYmNlNDE3OTVkNjQiLCJkaWQiOiIzNjk2MmRjMC01ZjliLTQwZGUtYTE5Yi04MDY0YTFmM2U4NzYiLCJpc3MiOiJodHRwczovL2F1dGguc2F5YS5uZXQuaW4iLCJhdWQiOiJhcGkiLCJpYXQiOjE3OTMyMzMxOTYsImp0aSI6IjgyMjhlZDg5LTVlY2MtNDVmZi1iNTU5LTYyYTZkZjZjNTc4ZCIsImV4cCI6MTc5MzIzNDA5Nn0.zVGkhjTWoraoj7b5uU37LQB-PvPU8LSHVlG0YwMqrlhSbLkyFV3qA_KT4TSnQmsobUCHhWkabNVEgxveZo_5WDa9eA9EUsiZL8xwX56Nzjxc4yTVyTbX2uGGjnbBV-hsQZ774a9Mo4dbWWp5Gkl9zziwlvXkARddcdetRk58FK5P1tifPK66_vF6mZpG3xLjs4CjokTjFK06LB02k8X1YjYJg-ZJAcA1cea23scmOSowKmBlymxGsrcifWwMr2OlQ5vrbbVlzcraK_0dJXyM3OLr6nJUqTWYhnuHcXzxUXPJKG5lZDM7GAjsYHa2aTpIvrcd-XzGs0aapIRHjjfNmg",
            'x-device-id': "36962dc0-5f9b-40de-a19b-8064a1f3e876",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'origin': "https://sayacare.in",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "cross-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://sayacare.in/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i"
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
