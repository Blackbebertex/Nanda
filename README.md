# ARTHA AI — Digital Wealth Advisor

Avatar-led digital wealth advisor for banks. **All AI is powered exclusively by Google Gemini** through a single shared `GeminiService`.

## Features

- 6 demo customer personas with live portfolio dashboards
- Quick-path chat (Chat Agent → Gemini)
- 7-step audited wealth plan (Workflow Agent → Gemini)
- Research, Analysis, Planning, Document, and Task Execution agents
- SSE streaming chat endpoint
- Session security, plan access control, compliance guardrails

---

## Prerequisites

- Python 3.11+
- Node.js 18+ (frontend static server)
- [Google Gemini API key](https://aistudio.google.com/apikey)

---

## Installation

```bash
git clone <your-repo>
cd IDBI

# Backend
cd artha_backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend (optional for local dev)
cd ../artha_frontend
npm run validate
```

---

## Environment Variables

Copy `.env.example` to `.env` in the project root (or set in your shell):

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
PORT=8000
NODE_ENV=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | **Yes** (for AI) | Google Gemini API key — never commit |
| `GEMINI_MODEL` | No | Default `gemini-2.0-flash` |
| `GEMINI_TIMEOUT_SECONDS` | No | Request timeout (default 60) |
| `GEMINI_MAX_RETRIES` | No | Retry count (default 3) |
| `PORT` | No | Backend port (default 8000) |
| `NODE_ENV` | No | `development` or `production` |
| `ALLOWED_ORIGINS` | No | CORS origins (comma-separated) |
| `WEALTH_CHAIN_ENABLED` | No | Enable deep wealth chain |
| `DATABASE_URL` | No | PostgreSQL for plan persistence |
| `REDIS_URL` | No | Session/cache backend |

**Never commit `.env`.** It is listed in `.gitignore`.

---

## Local Development

### Option A — PowerShell launcher

```powershell
cd D:\IDBI
$env:GEMINI_API_KEY = "your_key_here"
.\run_artha.ps1
```

### Option B — Manual

```bash
# Terminal 1 — API
cd artha_backend
export GEMINI_API_KEY=your_key_here
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd artha_frontend
npm run dev
```

Open **http://localhost:3000**

Demo auth: `Authorization: Bearer demo-token`

---

## Gemini Configuration

All LLM calls flow through `artha_backend/services/gemini_service.py`:

```
Agent → GeminiService.generate() / generate_json() / stream()
         ↓
    Google Gemini REST API (GEMINI_API_KEY)
```

- No Anthropic, OpenAI, or other providers in runtime code
- API key read only from `GEMINI_API_KEY`
- Retries on 429/5xx with exponential backoff
- Errors logged without exposing secrets
- Demo keyword fallback when key is missing (local dev only)

---

## AI Agent Architecture

| Agent | Role | Gemini usage |
|-------|------|--------------|
| **Chat Agent** | Quick conversational replies | `generate()` |
| **Planning Agent** | Goal architecture (chain step 2–3) | `generate_json()` |
| **Research Agent** | Product/fact research | `generate()` |
| **Analysis Agent** | Wealth analyst (chain step 1) | `generate_json()` |
| **Coding Agent** | Structured JSON steps 4–5, 7 | `generate_json()` |
| **Document Agent** | Avatar scripts (chain step 6) | `generate_json()` |
| **Workflow Agent** | Orchestrates 7-step chain | Delegates to agents above |
| **Task Execution Agent** | Recommendation narration | `generate()` |

Registry: `agents/registry.py` — `get_agent("chat")` etc.

Prompts: `agents/prompts/` and `agents/wealth_chain/prompts/`

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health + Gemini status |
| GET | `/v1/ai/status` | AI provider info |
| GET | `/v1/agents` | List all agents |
| GET | `/v1/demo/customers` | Demo persona roster |
| POST | `/v1/session/start` | Start session |
| POST | `/v1/conversation/message` | Chat message |
| POST | `/v1/conversation/message/stream` | SSE streaming chat |
| POST | `/v1/wealth/plan` | Full wealth plan |
| GET | `/docs` | OpenAPI Swagger UI |

---

## Render Deployment

### 1. Push to GitHub

```bash
git add .
git commit -m "Gemini-powered ARTHA AI"
git push origin main
```

### 2. Create Render services

Use the included `render.yaml` (Blueprint) or create manually:

**Web Service — `artha-api`**
- Root Directory: `artha_backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment: `GEMINI_API_KEY` = your key

**Static Site — `artha-frontend`**
- Root Directory: `artha_frontend`
- Build: `npm run build`
- Publish: `.`

### 3. Set environment variables on Render

| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | Your Gemini API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` |
| `NODE_ENV` | `production` |
| `ALLOWED_ORIGINS` | `https://your-frontend.onrender.com` |

### 4. Verify

- `https://your-api.onrender.com/health` → `"gemini_configured": true`
- Open frontend URL → chat works with Gemini responses

---

## Build Commands

```bash
# Backend tests
cd artha_backend && python -m pytest tests/ -v

# Frontend validate
cd artha_frontend && npm run validate

# Docker
docker build -t artha-api .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key artha-api
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `GEMINI_API_KEY is not configured` | Set env var; restart server |
| `403` on chat | Start session first via UI or `POST /v1/session/start` |
| CORS errors on Render | Set `ALLOWED_ORIGINS` to your frontend URL |
| Keyword mock replies | Gemini key missing — set `GEMINI_API_KEY` |
| `429` from Gemini | Rate limit — retries are automatic; reduce request frequency |
| Frontend can't reach API | Check `config.js` `BACKEND_URL` after `npm run build` |

---

## Production Recommendations

1. Replace demo tokens with bank OAuth/JWT
2. Store `GEMINI_API_KEY` in Render secret environment (never in code)
3. Enable `DATABASE_URL` for plan persistence across restarts
4. Set `NODE_ENV=production` and restrict `ALLOWED_ORIGINS`
5. Monitor `/v1/admin/llm-telemetry` (admin token required)
6. Rotate API keys periodically
7. Use Gemini safety settings for regulated financial content

---

## License

Internal / IDBI pilot — see project governance docs in `docs/`.
