import json
import random
from typing import Any
import requests

OTP_API_URL = "https://prod.digihaat.in/clientApis/v2/auth/sendOTP"

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
            "appHash": "yt1CWihGAiQ",
            "mobile": number
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'devicename': device["userAgent"],
            'deviceidentity': "d30e7585-8675-43eb-b843-0f6bc27d4597",
            'sec-ch-ua-platform': device["platform"],
            'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZDMwZTc1ODUtODY3NS00M2ViLWI4NDMtMGY2YmMyN2Q0NTk3X183NTk1MjdkMS0xYjY4LTRmYTEtYTVhNC0wY2ZkODcwMmIyZWUiLCJpc0d1ZXN0Ijp0cnVlLCJ0b2tlblR5cGUiOiJhY2Nlc3MiLCJqdGkiOiI5ZTkwMjVjNC05ZTc2LTQxNWMtOWFiZi0wNWZjMmNiN2NmYjQiLCJsYW5ndWFnZSI6ImVuIiwiZ3Vlc3RJZCI6ImQzMGU3NTg1LTg2NzUtNDNlYi1iODQzLTBmNmJjMjdkNDU5N19fNzU5NTI3ZDEtMWI2OC00ZmExLWE1YTQtMGNmZDg3MDJiMmVlIiwiaWF0IjoxNzkzMjQ0MTYwLCJleHAiOjE3OTM4NDg5NjB9.aAodr0PlNZ1kftS03hHxVWvm99eeK4kSpLGel5H4Tm7h6nv2bWF6SLSriT8SDYRIUqMz54qP9UaOWV1LdGog9RWNRlVeaDsNGCzrigE8f_EvdJ2zmLr1-5ihjHGYTHTLQ2eCG-D9HfGxrxnTiVw4Vn5Dgl7VLOfE8-G5idCvjvYdnJ7vaNu_lPh02NxlqWOnf_TZiz4sipBazcKY8UG1KoBda_mo7wKRYOoMCQrZAMm46byyks5TjCMfKWIOZaDMpSfzwzcVPFMf73VFtLAWBuL1CfcxaNhzim5kAVW1E359cWOieAsY_SvebidwkEoQGahC_9FuNxcqdvrBQVAeCg",
            'devicemanufacturer': "Google Inc.",
            'osversion': "Linux aarch64",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'appversion': "2.0.11",
            'web': "true",
            'platform': "web",
            'devicemodel': device["userAgent"],
            'origin': "https://www.digihaat.in",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.digihaat.in/",
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
