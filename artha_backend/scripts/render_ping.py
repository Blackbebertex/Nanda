"""One-shot ping for Render keep-alive (cron / CI / manual)."""
import os
import sys

import httpx

raw = os.environ.get("KEEPALIVE_URL") or os.environ.get("RENDER_API_URL") or ""
if not raw:
    print("KEEPALIVE_URL not set", file=sys.stderr)
    sys.exit(1)

base = raw if raw.startswith("http") else f"https://{raw}"
url = base.rstrip("/") + "/v1/demo/hello"

resp = httpx.get(url, timeout=30)
print(resp.status_code, resp.text)
resp.raise_for_status()
