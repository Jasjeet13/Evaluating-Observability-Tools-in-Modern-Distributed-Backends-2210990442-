#!/bin/bash
# S4 — CPU saturation (Kubernetes + LitmusChaos)
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Apply Litmus CPU experiment:"
echo "  kubectl apply -f k8s/namespace.yaml"
echo "  kubectl apply -f chaos/litmus/cpu-stress.yaml"
echo "For local Docker-only runs, use S1 high load to stress CPU on the host."
