#!/bin/bash
# S1 — High load stress (increase k6 rate in load/k6/checkout.js or use constant-arrival-rate)
set -euo pipefail
cd "$(dirname "$0")/../.."
export FAULT_DELAY_MS=0
docker compose up --build -d
echo "Run high load: k6 run --env GATEWAY_URL=http://localhost:8080 -e RATE=200 load/k6/checkout.js"
echo "Edit checkout.js rate to 500-2000 req/s for paper-scale tests on larger hardware."
