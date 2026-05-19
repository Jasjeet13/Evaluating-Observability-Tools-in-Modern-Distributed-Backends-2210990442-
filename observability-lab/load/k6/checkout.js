import http from 'k6/http';
import { check, sleep } from 'k6';

// S0/S1 load sweep: adjust VUS and duration to match paper (500-2000 req/s needs scaling)
export const options = {
  scenarios: {
    checkout: {
      executor: 'constant-arrival-rate',
      rate: 50,
      timeUnit: '1s',
      duration: '2m',
      preAllocatedVUs: 20,
      maxVUs: 100,
    },
  },
};

const BASE = __ENV.GATEWAY_URL || 'http://localhost:8080';

export default function () {
  const res = http.post(`${BASE}/api/checkout`, null, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, { 'status is 2xx': (r) => r.status >= 200 && r.status < 300 });
  sleep(0.01);
}
