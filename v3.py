import json
from typing import Any
import requests

OTP_API_URL = "https://phans.in/api/auth/requestOTP"  # or original endpoint if active

def main() -> dict[str, Any]:
    # ===== Load number from target.py =====
    try:
        from target import NUMBER
        number = str(NUMBER).strip()
    except Exception as e:
        return {"success": False, "message": f"Failed to load NUMBER from target.py → {e}"}

    if not (number.isdigit() and len(number) == 10):
        return {"success": False, "message": f"Invalid number in target.py: {number}"}

    url = "https://pharmeasy.in/api/auth/requestOTP"

    payload = {
        "contactNumber": number
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 15; Infinix X6871 Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.8059.43 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Android WebView\";v=\"155\", \"Chromium\";v=\"155\", \"Not(A:Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://pharmeasy.in",
        'x-requested-with': "mark.via.gp",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://pharmeasy.in/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
        'Cookie': "XdI=-d-DMjt_e6enyjd2s1Ogt; X-Feature-Flags=%7B%22isBestOfferEnabled%22%3Atrue%7D; X-Default-City=1; X-Pincode=400086; XPESD=%7B%22session_id%22%3A%22s_w_-d-DMjt_e6enyjd2s1Ogt_1793222522000%22%2C%22session_id_flag%22%3A%22fingerprint%22%2C%22referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22session_start_time%22%3A%222026-10-28T21%3A22%3A02.549Z%22%7D; XPESS_v2=s_w_-d-DMjt_e6enyjd2s1Ogt_1793222522000"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        try:
            result_data = response.json()
        except json.JSONDecodeError:
            result_data = {"raw": response.text}

        return {
            "success": response.ok,
            "status_code": response.status_code,
            "data": result_data
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
