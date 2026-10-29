import json
import random
from typing import Any
import requests

OTP_API_URL = "https://10minutesindia.com/otp/send-login"

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
        f"Mozilla/5.0 (Linux; Android {d['android']}; {d['model']} Build/{build}; wv) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_full} "
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
            'phone': number,
            'name': 'User',
            'ref': ''
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'x-csrf-token': "LkoPteI3h9bhVCRD5a4ndvc4mlsa1giyaNisMhOq",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'origin': "https://10minutesindia.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://10minutesindia.com/login",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "XSRF-TOKEN=eyJpdiI6Ing1M0JjWEdDdVlucGM4VDNEUUE4YWc9PSIsInZhbHVlIjoieW1GdHNxYS/RYVFhdTZIaDA3QlVSMWNqMThEMEdEM0NnUS9hYzdVQkRGWTNFK1hBRXFJVVpYZzdSd3l0b0w5MTNyS1VSei9rQTFTY2JPV0xrRXdwYmZhUmhJTlRQeis2SU01bDNReXlpQWhKYWptcGFZNkkxVytscWJlZWN0U0wiLCJtYwciOiI5ZTU2OGU0NTIxMDc5OTU3NmVjNzcwYmM5Y2RhNzFlMTA5YTAzY2FjMDhlM2Q4MTJhY2RjZmYwMDkyMmU0NTBlIiwidGFnIjoiIn0%3D; 10minutesindia-session=eyJpdiI6Im1CdDhBb0FNUTAzL2xwOGJYa1FKWlE9PSIsInZhbHVlIjoiZVkvdFRWVDJmb0V4TjF1YVJqWTU2ejJpWXJFZ0FobktIekdmQkN5a1FzejZjTEl4OElFc1ZUdjNSbGZTdHFtVmdoS3hzb1ByenFnalA2blpzUjRuTlozUWhRc1NNdWIzdG1IajgwRkpvMkhwU2xJbnJyMzVWTHBVcUE1WGtlRHMiLCJtYWMiOiI2MTRmOGI2ZTJhZjlhYzcyYTU1MWUwMTQ4NTY4MDVmOGQyYWNmZmMzYzJmNjEzM2U0N2M2NGE4NDA2YzZkZjFmIiwidGFnIjoiIn0%3D"
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

