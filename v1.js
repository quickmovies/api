const NUMBER_JSON_URL = 'https://quickmovies.github.io/api/number.json';
    const OTP_API_URL = 'https://www.bikewale.com/api/user/login/otp-request/';

    let currentNumber = null;
    let isSending = false;

    function log(msg, type = 'info') {
      const el = document.getElementById('status');
      el.className = 'status ' + type;
      el.textContent = msg;
    }

    function updateLastUpdated() {
      const now = new Date();
      document.getElementById('lastUpdated').textContent =
        'Last checked: ' + now.toLocaleTimeString();
    }

    async function sendOtp(number) {
      if (isSending) return;
      isSending = true;

      log(`Auto-sending OTP to ${number}...`, 'info');

      try {
        const payload = {
          mobileNo: number,
          sourceModule: 14
        };

        const res = await fetch(OTP_API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://www.bikewale.com',
            'Referer': 'https://www.bikewale.com/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; Infinix X6871 Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.8059.43 Mobile Safari/537.36',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua': '"Android WebView";v="155", "Chromium";v="155", "Not(A:Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'x-requested-with': 'mark.via.gp',
            'serverdomain': 'CarWale'
          },
          body: JSON.stringify(payload)
        });

        const text = await res.text();
        let result;
        try {
          result = { status: res.status, data: JSON.parse(text) };
        } catch {
          result = { status: res.status, raw: text };
        }

        if (res.ok) {
          log('OTP Sent Successfully!\n\n' + JSON.stringify(result, null, 2), 'success');
        } else {
          log('Failed (HTTP ' + res.status + ')\n\n' + JSON.stringify(result, null, 2), 'error');
        }

      } catch (err) {
        log('Error: ' + err.message + '\n\n(CORS is the usual reason)', 'error');
      }

      isSending = false;
    }

    async function loadNumber() {
      try {
        const res = await fetch(NUMBER_JSON_URL + '?t=' + Date.now());
        const data = await res.json();

        let numbers = [];
        if (Array.isArray(data)) {
          numbers = data.map(item => {
            if (typeof item === 'object' && item !== null) {
              return item.number ?? item;
            }
            return item;
          });
        }

        if (numbers.length === 0) {
          document.getElementById('displayNumber').textContent = 'No number found';
          currentNumber = null;
          return;
        }

        const target = String(numbers[0]).trim();
        document.getElementById('displayNumber').textContent = target;
        updateLastUpdated();

        // Only auto-send if number is valid and different from last one
        if (/^\d{10}$/.test(target) && target !== currentNumber) {
          currentNumber = target;
          await sendOtp(target);
        }

      } catch (err) {
        document.getElementById('displayNumber').textContent = 'Error loading';
        log('Failed to load number.json', 'error');
        console.error(err);
      }
    }

    // Load + auto-send immediately
    loadNumber();

    // Keep checking every 8 seconds
    setInterval(loadNumber, 8000);
