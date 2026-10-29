import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.caratlane.com/cg/dhevudu"

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
            "query": "mutation SendOtp($mobile:String, $isdCode:String, $otpType:String, $email:String){\n  SendOtp(input:{mobile:$mobile, isdCode:$isdCode, otpType:$otpType, email:$email}){\n          status{\n              message\n              code\n          }\n      }\n  }\n",
            "variables": {
                "mobile": number,
                "isdCode": "91",
                "otpType": "registerOtp"
            }
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': device["platform"],
            'authorization': "07152c8e48070703aa9b36b15fdca083db285dcd1fc27f31ac9c6690a186",
            'sec-ch-ua': device["secChUa"],
            'x-authorization': "07152c8e48070703aa9b36b15fdca083db285dcd1fc27f31ac9c6690a186",
            'x-amzn-trace-id': "uniqid=4grjumvsuecqo-1793236031744",
            'sec-ch-ua-mobile': device["mobile"],
            'setsamesite': "true",
            'ib': "false",
            'uniqid': "4grjumvsuecqo-1793236031744",
            'cs-request': "true",
            'cookieenabled': "true",
            'origin': "https://www.caratlane.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.caratlane.com/login",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "rb_uid=4grjumvsuecqo; selectedLanguage=en; ab_site=old; BP=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InZicm8zaG12c3VlY3F4IiwiZXhwIjoxNzk1ODkwNTk5LCJpYXQiOjE3OTMyMzU5NzMsImF1ZCI6IldlYiIsImlzcyI6IkNhcmF0bGFuZSJ9.qDIQuo18edmiY51-XYgJcSm2OTowhk_0xGgvfsD6CqzkATN9fr-wvgx-lkMeLy9S_QDgecEXv_x1CwPDJCS8ye-zEWqCcezVFHh8Yy6ZU3VmOackdb6xETMX0RzwpJ7Wjm9TjdDSAjkqaer4FS-ijFCB0PVs54MQA2Vi081ugJ4CP-oPGAs_fpLV51K7ybWC0cudWxDDVDn77UFYNTgAhEt2JIkLfpFhVoA743es1we7OuTNt9erHf73z2MCgjVsA6xGVOSwMGsouVeiUYsyMWQ9f4txzck6h2CoDXQJSBtPGSjLhy00tnb5z7m4IJ7mXMTs_3fzog69-t8fl9Mzrg; JCN=07152c8e48070703aa9b36b15fdca083db285dcd1fc27f31ac9c6690a186; vt_bp=true; showHighlightForRecentlyViewedStoreLink=true; locale=en_IN; _fbp=fb.1.1793235986082.386375083286168122; G_ENABLED_IDPS=google; AWSALBTG=MQPmkOU6JMZDq7fCM532YF2ThTz7PjX16Ew0hjJI7t1kVZaRl3W/FWV24R6fwUuOTMF0xFR98pAY8u6FCSm3JcZcZx3P/QB6CeEcXpGLo0Vit72wQNvAjtqhhu+Pm7MyTkd2S0apr0h2HhXKsdxUl4tptQYLO1U1o071yAbuetLBpehN7Ew="
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
