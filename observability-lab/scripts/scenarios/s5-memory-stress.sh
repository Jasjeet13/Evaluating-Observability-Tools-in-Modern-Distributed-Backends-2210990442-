#!/bin/bash
# S5 — Memory pressure (Kubernetes + LitmusChaos)
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Apply Litmus memory experiment:"
echo "  kubectl apply -f k8s/namespace.yaml"
echo "  kubectl apply -f chaos/litmus/memory-stress.yaml"
