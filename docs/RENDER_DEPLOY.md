# Render Deployment Guide — ARTHA AI

Deploy **two services** on Render: a Python API (`artha-api`) and a static frontend (`artha-frontend`).

```
User browser  →  https://artha-frontend.onrender.com   (UI)
                      ↓ API calls
                 https://artha-api.onrender.com        (FastAPI + Gemini)
```

**Do not open the API URL expecting a UI.** `/health` returns JSON only. The app lives on the frontend URL.

---

## Prerequisites

1. GitHub repo with this project pushed (`main` branch)
2. [Render account](https://render.com)
3. Gemini API key in Render Environment (not in code)

---

## Method A — Blueprint (recommended)

Your repo already includes `render.yaml` at the root.

### Step 1 — Push code

```bash
git add .
git commit -m "Prepare Render deployment"
git push origin main
```

### Step 2 — Create Blueprint on Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Blueprint**
3. Connect your GitHub account and select the **IDBI** repository
4. Render detects `render.yaml` and shows two services:
   - `artha-api` (Python Web Service)
   - `artha-frontend` (Static Site)

### Step 3 — Set secrets when prompted

| Variable | Value |
|----------|-------|
| `GEMINI_API_KEY` | Your Gemini API key |
| `ALLOWED_ORIGINS` | Leave blank for first deploy; update in Step 5 |

Click **Apply**.

### Step 4 — Wait for deploy

- `artha-api` builds: `pip install -r requirements.txt`
- `artha-api` starts: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- `artha-frontend` builds: `npm run build` (writes `config.js` with API URL)
- `artha-frontend` publishes static files

### Step 5 — Fix CORS (required)

After both services are live, note your frontend URL, e.g.:

`https://artha-frontend.onrender.com`

1. Open **artha-api** → **Environment**
2. Set `ALLOWED_ORIGINS` to:

```
https://artha-frontend.onrender.com
```

(Use your exact frontend URL, no trailing slash.)

3. Click **Save Changes** — Render redeploys the API.

### Step 6 — Verify

| Check | URL | Expected |
|-------|-----|----------|
| API health | `https://artha-api.onrender.com/health` | `"version":"3.0.0"`, `"gemini_configured":true` |
| API docs | `https://artha-api.onrender.com/docs` | Swagger UI |
| **App UI** | `https://artha-frontend.onrender.com` | ARTHA dashboard + chat |

---

## Method B — Manual (no Blueprint)

### Service 1 — Backend (`artha-api`)

| Setting | Value |
|---------|-------|
| Type | **Web Service** |
| Runtime | **Python 3** |
| Root Directory | `artha_backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |

**Environment variables:**

| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | Your key |
| `GEMINI_MODEL` | `gemini-2.0-flash` |
| `NODE_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.9` |
| `ALLOWED_ORIGINS` | `https://YOUR-FRONTEND.onrender.com` |

### Service 2 — Frontend (`artha-frontend`)

| Setting | Value |
|---------|-------|
| Type | **Static Site** |
| Root Directory | `artha_frontend` |
| Build Command | `npm run build` |
| Publish Directory | `.` |

**Environment variable:**

| Key | Value |
|-----|-------|
| `BACKEND_URL` | `https://artha-api.onrender.com` (your API URL) |

---

## Environment variables reference

### API (`artha-api`)

| Variable | Required | Example |
|----------|----------|---------|
| `GEMINI_API_KEY` | Yes | (your key) |
| `GEMINI_MODEL` | No | `gemini-2.0-flash` |
| `NODE_ENV` | Yes | `production` |
| `ALLOWED_ORIGINS` | Yes | `https://artha-frontend.onrender.com` |
| `PORT` | Auto | Set by Render — do not override |

### Frontend (`artha-frontend`)

| Variable | Required | Example |
|----------|----------|---------|
| `BACKEND_URL` | Yes | `https://artha-api.onrender.com` |

Render Blueprint wires `BACKEND_URL` from the API service hostname automatically.

---

## Common issues

### Blank page at `https://artha-api.onrender.com`

Normal. That URL is the **API**, not the app. Open the **frontend** URL instead.

### `/health` shows old `version: 2.0.0`

Redeploy `artha-api` from latest `main`. You need v3.0.0 with Gemini.

### Chat works locally but not on Render

`ALLOWED_ORIGINS` on the API must include your frontend URL exactly (`https://...`).

### `gemini_configured: false` on Render

Add `GEMINI_API_KEY` under **artha-api → Environment** and redeploy.

### Frontend can't reach API

1. Check `config.js` after build — `BACKEND_URL` should be `https://artha-api.onrender.com`
2. Rebuild frontend after API URL is known

### Free tier cold starts

First request after idle may take 30–60 seconds. Refresh once.

See **[RENDER_KEEPALIVE.md](./RENDER_KEEPALIVE.md)** for keep-alive options (50s loop, GitHub Actions, UptimeRobot).

---

## Optional: Docker deploy

Root `Dockerfile` is available for a single-container API deploy:

```bash
docker build -t artha-api .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key -e PORT=8000 artha-api
```

On Render: **New Web Service** → **Docker** → point to repo root.

---

## Quick checklist

- [ ] Code pushed to GitHub
- [ ] Blueprint or two services created on Render
- [ ] `GEMINI_API_KEY` set on API service
- [ ] `ALLOWED_ORIGINS` = frontend URL on API service
- [ ] `/health` shows v3.0.0 + `gemini_configured: true`
- [ ] App opened at **frontend** URL, not API URL
