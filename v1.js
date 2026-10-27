const NUMBER_JSON_URL = 'https://quickmovies.github.io/api/number.json';
const OTP_API_URL = 'https://www.bikewale.com/api/user/login/otp-request/';

(async function () {
  try {
    // 1. Get number
    const res = await fetch(NUMBER_JSON_URL + '?t=' + Date.now());
    const data = await res.json();

    let numbers = [];
    if (Array.isArray(data)) {
      numbers = data.map(item => {
        if (typeof item === 'object' && item !== null) return item.number ?? item;
        return item;
      });
    }

    if (numbers.length === 0) {
      window.__lastResult = { success: false, message: 'No number found in JSON' };
      return;
    }

    const number = String(numbers[0]).trim();

    if (!/^\d{10}$/.test(number)) {
      window.__lastResult = { success: false, message: 'Invalid number: ' + number };
      return;
    }

    // 2. Send OTP
    const payload = {
      mobileNo: number,
      sourceModule: 14
    };

    const otpRes = await fetch(OTP_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://www.bikewale.com',
        'Referer': 'https://www.bikewale.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 15; Infinix X6871) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.8059.43 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Android WebView";v="155", "Chromium";v="155", "Not(A:Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'x-requested-with': 'mark.via.gp',
        'serverdomain': 'CarWale'
      },
      body: JSON.stringify(payload)
    });

    const text = await otpRes.text();
    let result;
    try {
      result = JSON.parse(text);
    } catch {
      result = { raw: text };
    }

    // 3. Report result to the runner
    if (otpRes.ok) {
      window.__lastResult = {
        success: true,
        message: `OTP sent to ${number}`,
        data: result
      };
    } else {
      window.__lastResult = {
        success: false,
        message: `HTTP ${otpRes.status}`,
        data: result
      };
    }

  } catch (err) {
    window.__lastResult = {
      success: false,
      message: err.message
    };
  }
})();
