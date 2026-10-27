const https = require('https');
const { randomUUID } = require('crypto');

const NUMBER_JSON_URL = 'https://quickmovies.github.io/api/number.json';
const OTP_API_URL = 'https://api.allen-live.in/api/v1/auth/sendOtp?center_id=&source=home-page-login';

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

function sendOtp(number) {
  return new Promise((resolve, reject) => {
    const deviceId = `\( {randomUUID()}- \){randomUUID()}`;

    const payload = JSON.stringify({
      country_code: "91",
      phone_number: String(number),
      persona_type: "STUDENT",
      otp_type: "SHARED_DEFAULT"
    });

    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://allen.in',
        'Referer': 'https://allen.in/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 15)',
        'x-device-id': deviceId,
        'x-client-type': 'mweb',
        'x-referrer': 'https://allen.in/',
        'x-requested-with': 'mark.via.gp',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(OTP_API_URL, options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch {
          resolve({ raw: body });
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

(async () => {
  try {
    console.log('Fetching numbers...');
    const data = await fetchJson(NUMBER_JSON_URL);

    // Handle both formats: [7848753925] or [{ "number": "7848753925" }]
    let numbers = [];
    if (Array.isArray(data)) {
      numbers = data.map(item => {
        if (typeof item === 'object' && item !== null) {
          return item.number || item;
        }
        return item;
      });
    }

    if (numbers.length === 0) {
      console.log('No numbers found');
      return;
    }

    // Take only the first number
    const target = String(numbers[0]).trim();

    if (!/^\d{10}$/.test(target)) {
      console.log('Invalid number:', target);
      return;
    }

    console.log(`Sending OTP to: ${target}`);
    const result = await sendOtp(target);
    console.log('Response:', JSON.stringify(result, null, 2));

  } catch (err) {
    console.error('Error:', err.message);
  }
})();
