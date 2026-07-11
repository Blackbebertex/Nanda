#!/usr/bin/env bash
# Ping Render API every 50s to reduce free-tier cold starts during demos.
API_URL="${RENDER_API_URL:-https://artha-api-lsli.onrender.com}"
INTERVAL="${KEEPALIVE_INTERVAL_SECONDS:-50}"
PING_URL="${API_URL%/}/v1/demo/hello"

echo "ARTHA keep-alive -> $PING_URL every ${INTERVAL}s (Ctrl+C to stop)"

while true; do
  if curl -sf --max-time 30 "$PING_URL"; then
    echo ""
    echo "$(date -u +%H:%M:%S) hello ok"
  else
    echo "$(date -u +%H:%M:%S) ping failed"
  fi
  sleep "$INTERVAL"
done
