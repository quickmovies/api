import json
import random
from typing import Any
import requests

OTP_API_URL = "https://mypillo.in/api/auth/send-otp"

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
            "os": "web",
            "utm_campaign": "pillpop"
        }

        headers = {
            'User-Agent': device["userAgent"],
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': device["platform"],
            'sec-ch-ua': device["secChUa"],
            'sec-ch-ua-mobile': device["mobile"],
            'origin': "https://mypillo.in",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://mypillo.in/city/pune",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
            'Cookie': "pillo_utm=%257B%2522utm_source%2522%253A%2522www.google.com%2522%252C%2522utm_medium%2522%253A%2522organic_search%2522%252C%2522utm_campaign%2522%253A%2522organic_search%2522%252C%2522wpsrc%2522%253Anull%252C%2522referer%2522%253A%2522https%253A%252F%252Fwww.google.com%252F%2522%252C%2522timestamp%2522%253A1793229881923%252C%2522expiry%2522%253A1801005881923%257D; access_token=eJwtzt1ugjAYgOErmqlMNBwuZLKP2IJQsPTEzBbtrzTRBOnVLya7gPfJOy6luhRCV7qELsKaaHjAvUlFDluwgfV5ma3GpZwH1gR%2BShFLnAUz6e7kKpI4VxXrVFh5EIgf2j2hBPFvHlEGetaSESdcFvgbc%2FtAjQycqufIyp%2F2kxQtUrSLsmgKkdUtPMA3TnpneP%2FfvGe8UzKHLaYixRGWit42eJk1Z2oGM71ItBEb%2FCLmFq%2FHFe%2BnLrv6zU6bs7z0Ik%2BTET0HEanPp1h%2FdL9H%2B8VlUPXwB91PVjI%3D; refresh_token=eJwtztFOgzAYQOE3WjomW7gkzOFfR6tQoPTGaAu0pQgJRqBPb5b4AOfLaHlssv1JpqMFQejgSAwt856FM4AzDzKsER4d2x2vD81nUIeKBG8BOpqwdJYFzND2GclB3icS9uBFGkHgWHkVgVqM4cdJFs3hg7jYzq2bB9E%2FL8UtxImmBNCu9SvNURm8FLDDmTo3Oiuq%2FecyMTqsEzhmTYeZhp6x%2FyvbVCK5XsNNGr4CIb4702vvu%2FdB85Jfq95L4aQySutdxFU6oW%2BpNbNa%2BLiOOu%2BIUB%2BvnAH%2BsHFUz; chemist-list=jbdAT250XCu2%2F0FHWZx8GHPTdCN1M7SjgW9Wpssgfz4zHGcKfBnxLiVytnlvGSKVZGswvvAozdDU6ed%2F3IgBu%2Bz8l7TIPdYNnkIaHf07UosUmri1cvy5zfOqDMAJD1uc2dmLdmvgiRmgdY7lhW8WOFHuiPQVuzLu5d%2FsB5Kr1AZ9n6Dqyo2VSEkTCld97B8DI3klfsaiMCr%2FsuImVB5qBWPwuNtFAPAKOVSqTVndYMBdmb3onnvpQSAIsI1TRNsuFy1f84x0QP1ZhuPQSEIa%2Fgj2J3l9F8x2MVmd1QSHwjF%2BK4m%2BKIw64PNggDSXjsJgGt1pmV40%2B8OFY3tGjvErH9GFxAYV%2B5A0WLRlXDz8p0KR0qAAdZi6IAzD1mcUNUJ%2FTfi%2ByIBUcAQRl4xYvxaFlQz2mVzYN%2BBVvEGMMbe4CfhiIOcne4ujpaTmWObajQkiD2czlneE9TPR%2Fzu9eHtnB5D%2BG%2B1PyqERX4FZELpB%2BtUNzh67LA%2FiDwRjmGXhk0K1V3OGEEimRXyTCyHwoxKm6Kfjmley7tN0b3pU8c7aaoETfCJ3w0bjKijhgId75b3xoY4b9V0ipEbBIcW63UcnRY3YvJSHSJza%2BpWfcgr98%2FKqIAicPyaQqZzYW5bYiwjd7Qzc%2Fto0cqD4Z5Rys6MC8KuoyZLcy2W7dtguiyvyYmiWTiUe0qTm2itafnTNsojVsrpgRXPXBT943aW2ay8a3lTI6%2FGGtNP0UqgLb61oPfke%2Bw8AtvshPxlTI%2BmqADK9Hy0ixlX7WByHf2giQUCgR02clT4VuW%2F%2BLTFfsbNYN5xBh26yufg%2BA4TKe5AbbWoYqYJ7kgrr67fjWmBenTVWtP79vTvT%2Fxi6KfiJRYVfGeKSyj2b%2FRbtgvesYjlGXJ2J2ZrBhd5C1VZUakfUyvxKD7XNP1lDLdOT8Z5Jp0yRDJEBJKr9YLoCSNhAGJEuCY8654B8PesxJoHgfvQ%2FXCk9zG86lGertLH7e1%2Fqh2H9tviiAHVjWGrY1uFPZGqh5om2hlH1%2BVZGPB%2FBt7YRJZfLk4X0l1z2nMdc6Vaev0SZAKpWccKuGwu6RzZGrhf9ncy454Ritg2PBZ%2BZIClJXL346kZSm7E7NwSYpGAce%2BErBAOajdZwbBwtIjhIUoHSpSKYJUlKu%2B7POyEehANq6M5THK7Q6Xd3MH2OjApYSzU47QIXn7T95CPFuH5xIOOXNKTVOrIiWvP9L7jEWjHr71e8lhC%2BQo7gvRjihOrllq%2BAMA8i8e5DrfDvqsTJ8C2sE24nrDyvlmssk88JVSXelCMSfIo4%2Fzh46Er3%2BHJCAB66Zov5wPyJ9LhIPtdElGOI9lAgnncob2F1i%2BNiS%2BRrP8D4TR%2FHR106dKplbtnMGuvo9ShRKdFwX2ewp3E1bSAN0gH0VQGeotkgaPCV5ciUjBm4PfWYZ2DcnJxzrSgqEC6gXbPr4qsLQ8xwGiOPy%2BfOJczWg5eGAODFWnul22sYZuekAD4UcYdoV%2BukGW3cHAcaP2o%3D; error_slug=no_pharmacy_found_due_to_off_hours; is_quick_saver=false; moduleDateselect=29%2F10%2F2026; user-latitude=18.5211; user-longitude=73.8502; user-address=Pune; user-address-line2=Pune%2C%20Maharashtra; user-city=Pune; user-state=Maharashtra; user-country=India; full-address=Pune%2C%20Maharashtra%2C%20India; zipcode=411004"
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
