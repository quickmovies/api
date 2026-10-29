import json
import random
from typing import Any
import requests

OTP_API_URL = "https://www.medplusmart.com/my-profile/getOtp"

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
            'MOBILE_NUMBER': number,
            'tokenId': "EA4A63D8AB7C08A6D80655D8C19A5565",
            'isCordova': "false",
            'isPhonepeSwitch': "false",
            'SESSIONID': "EA4A63D8AB7C08A6D80655D8C19A5565"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-platform': device["platform"],
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.medplusmart.com/login",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "bm_sz=33AA12532225FA2C204C33A55EB9ADDE~YAAQnfQ3F3qtm4GhAQAA92vMhAEXnAELwjaIMWpIZBo73pc5SsYVQA5NvQXOR87O7Jw84B/TX4hJzV28aOZemARXZ3oBV4oxpZrD6rRBBHiBsDj3kvVdH2Ci8CUYkdqzNfTUHIU9vj/35d6w/dWXQKZYmqlhIx9tS4zTjvoq3GyhcI7qPGxuEGl8nMcu434UY3+lZFuBIms7WmzFXo20u3cmQdwlJUkh3B8SM/jY9ZODtuJiIuie7XufLqG0W1UdzrMYQv4hsKYSw2kDrT/BuKX6lGdfjRAu3FSV53tAktwKQZWIdZHb1WAy7YDIJ12FiVmvHT1YBIbttxUjCXDTkVKVF/badKeYYzcf1pmG0Zvi3GXZbhDahJy6aOj8yxaS152qHgr6lJ3p8ZlIyM2Ae/2+89Rf~4343353~3160386; tokenId=EA4A63D8AB7C08A6D80655D8C19A5565; locality=%7B%22combination%22%3A%22Lee%20Pharma%2C%20Bhavani%20Nagar%2C%20Balanagar%2C%20Hyderabad%2C%20Telangana%20500018%2C%20India%22%2C%22pincode%22%3A%22500018%22%2C%22locationLatLong%22%3A%2217.472083%2C78.428701%22%7D; redisCart=true; JSESSIONID=3BEFF658C2D9B400C7E0E0EEDB27B4EF; _abck=08AF8FB814C5D215BCC13300B0D24E23~-1~YAAQnfQ3F1qwm4GhAQAATLTMhBBXk4t7Wv7goUomQQPLJe7Ve9wHn7KjjP0RLVdtXCpOUC5/CQS0MFV23zhqmMnJHF441gswzDmCZSRxgS7VJZHS8djp6+qZUn/IG1VmJLy527MfjdhWaQd4KalbhAIYjW75AadV20+b88yvaMWcP12qqIt2y+nEOlnwmvp0x9an5FC/R2o8LeVnPEAv4uvsE1ESTcqGSWZ1yYpb3UB77zTBfywGI7LIkIuT9cwsUHVYVhy3hTi0lH0BZzkbogFXXU6L9nOMs4aXlohJNrk0p+FaD0eF7GCAQOrMul0Ewpa6ux19Ic4UVD6s1Z5eIv1wEjM1B1OwgnUDyTVzZBRMUCDeGPaICdTYmy2+RUuayVhk79JehyRQ47n6GtrihMU94WWhwprUHSYHdXPlaAV1UBCSk/OFu5kQFF9qbq50pYHSREY05ennzg7xQ3wO+HVJpnmHkhto0zMNsatUq83af6xqCxvVNpQHigKWzc8K62ccpM9Snf6HC/F5y2I7L3EHm7HFURvWxHRBj7jFFL7UfKsE2OBYiWXpM/k2QEZ4ezohxe3QqnHNK9ZzYW8nIrkbE8jiu7vfm3VL2d5wHtgh1r1EvFuwQQu4D07qyn+XoA==~-1~-1~-1~AAQAAAAG%2f%2f%2f%2f%2f%2fzuIZSSM8WkViEO1ldFrZIIl2HQdtbaQAtD2aciqDfc9XRSoewbdFtG%2fofBFADcr%2fJ8+L3xn8ohBn3BTa6IkOQxSK%2f8T2HYHoDe~-1"
        }

        resp = requests.get(
            OTP_API_URL,
            params=params,
            headers=headers,
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
