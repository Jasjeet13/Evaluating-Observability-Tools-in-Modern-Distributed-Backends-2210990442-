#!/bin/bash
# S3 — Network delay (+20 ms on order → payment path in Compose; use chaos/netem on K8s)
set -euo pipefail
cd "$(dirname "$0")/../.."
export FAULT_DELAY_MS=0
export FAULT_NETWORK_DELAY_MS=20
docker compose up --build -d
echo "S3 network delay: FAULT_NETWORK_DELAY_MS=20 on order-service"
