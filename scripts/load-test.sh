#!/usr/bin/env bash
# Load generator for the HPA demo.
#
# Usage:
#   ./scripts/load-test.sh [BASE_URL] [DURATION_SECONDS]
#
# Typical cluster run:
#   kubectl port-forward svc/medidesk-backend 8000:80 -n medidesk &
#   ./scripts/load-test.sh http://localhost:8000 120
#
# Then watch: kubectl get hpa -n medidesk -w

BASE_URL="${1:-http://localhost:8000}"
DURATION="${2:-120}"

echo "Load-testing $BASE_URL for ${DURATION}s — watch 'kubectl get hpa'"
END=$((SECONDS + DURATION))
COUNT=0
FAIL=0

while [ $SECONDS -lt $END ]; do
  for path in /api/appointments /api/appointments/stats; do
    if curl -sf -o /dev/null "$BASE_URL$path"; then
      COUNT=$((COUNT + 1))
    else
      FAIL=$((FAIL + 1))
    fi
  done
done

echo "done: $COUNT requests ok, $FAIL failed"
