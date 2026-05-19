#!/bin/bash
# S0 — Normal load, no fault
set -euo pipefail
cd "$(dirname "$0")/../.."
export FAULT_DELAY_MS=0
docker compose up --build -d
echo "S0 running. Gateway http://localhost:8080 | Grafana http://localhost:3000 (admin/admin) | Jaeger http://localhost:16686"
echo "Load: k6 run load/k6/checkout.js"
