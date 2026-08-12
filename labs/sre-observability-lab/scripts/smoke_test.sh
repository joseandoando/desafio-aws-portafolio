#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"
PROM_URL="${PROM_URL:-http://localhost:9090}"

retry() {
  local url="$1"
  local attempts="${2:-20}"

  for _ in $(seq 1 "$attempts"); do
    if curl --fail --silent --show-error "$url" >/dev/null; then
      return 0
    fi
    sleep 2
  done

  echo "Timed out waiting for $url" >&2
  return 1
}

echo "Waiting for application..."
retry "$BASE_URL/health"

echo "Checking readiness endpoint..."
curl --fail --silent --show-error "$BASE_URL/ready" | grep -q 'ready'

echo "Checking Prometheus metrics..."
curl --fail --silent --show-error "$BASE_URL/metrics" | grep -q 'demo_http_requests_total'

echo "Generating a controlled 500 response..."
status="$(curl --silent --output /dev/null --write-out '%{http_code}' "$BASE_URL/simulate/error")"
test "$status" = "500"

echo "Generating a slow request..."
curl --fail --silent --show-error "$BASE_URL/simulate/latency" >/dev/null

echo "Checking Prometheus readiness..."
retry "$PROM_URL/-/ready"

echo "SRE lab smoke test passed."
