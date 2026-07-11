# Render Keep-Alive — ARTHA API

Render **free tier** web services sleep after ~**15 minutes** of no traffic. Cold starts can take 30–60 seconds.

This project includes a lightweight demo endpoint and keep-alive loops so the API stays warm during demos.

---

## Demo ping endpoint

```
GET https://your-api.onrender.com/v1/demo/hello
```

Response:

```json
{
  "message": "hello",
  "service": "ARTHA API Gateway",
  "status": "ok",
  "time": "2026-07-10T12:00:00+00:00"
}
```

No auth required (same as `/v1/demo/customers`).

---

## Option 1 — Frontend auto-ping (recommended)

When the app is open (Vercel or Render frontend), the UI pings `/v1/demo/hello` every **50 seconds** automatically. No extra setup.

---

## Option 2 — Local loop (Windows)

```powershell
cd D:\IDBI
$env:RENDER_API_URL = "https://artha-api-lsli.onrender.com"
.\scripts\render_keepalive.ps1
```

Custom interval:

```powershell
.\scripts\render_keepalive.ps1 -ApiUrl "https://artha-api-lsli.onrender.com" -IntervalSeconds 50
```

---

## Option 3 — Local loop (Mac/Linux)

```bash
export RENDER_API_URL=https://artha-api-lsli.onrender.com
bash scripts/render_keepalive.sh
```

---

## Option 4 — GitHub Actions (always-on)

Workflow `.github/workflows/render-keepalive.yml` pings every **10 minutes** when enabled.

1. Repo → **Settings** → **Secrets** → add `RENDER_API_URL` = `https://artha-api-lsli.onrender.com`
2. Workflow runs on schedule automatically after push

---

## Option 5 — External monitor (free)

Use [UptimeRobot](https://uptimerobot.com) or [cron-job.org](https://cron-job.org):

- URL: `https://your-api.onrender.com/v1/demo/hello`
- Interval: **5 minutes**

---

## Notes

| Method | Interval | Needs PC on? |
|--------|----------|--------------|
| Frontend auto-ping | 50s | No (tab open) |
| `render_keepalive.ps1` | 50s | Yes |
| GitHub Actions | 10m | No |
| UptimeRobot | 5m | No |

Render **cron jobs** are not on the free plan — use GitHub Actions or an external pinger instead.

---

## Verify

```powershell
Invoke-RestMethod https://artha-api-lsli.onrender.com/v1/demo/hello
```

Expected: `message : hello`
