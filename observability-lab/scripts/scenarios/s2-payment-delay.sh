#!/bin/bash
# S2 — Payment service +300ms delay (middleware sleep)
set -euo pipefail
cd "$(dirname "$0")/../.."
export FAULT_DELAY_MS=300
docker compose up --build -d
echo "S2 payment delay active (FAULT_DELAY_MS=300). Run k6 against gateway."
