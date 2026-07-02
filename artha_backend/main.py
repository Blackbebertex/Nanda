"""
ARTHA AI – FastAPI Backend (demo-ready)
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import uuid, datetime

# ──────────────────────────────────────────────
# Pydantic Schemas
# ──────────────────────────────────────────────
class SessionStartRequest(BaseModel):
    language: str = "en"

class SessionStartResponse(BaseModel):
    session_id: str
    customer_id: str
    language: str

class MessageRequest(BaseModel):
    session_id: str
    message_text: str

class MessageResponse(BaseModel):
    reply_text: str
    recommendation_ids: List[str] = []

class RecommendationFeedbackRequest(BaseModel):
    feedback: str

class VoiceSynthesisRequest(BaseModel):
    text: str
    language: str = "en"

class VoiceSynthesisResponse(BaseModel):
    audio_url: str
    duration_ms: int
    viseme_cues: List[dict]

# ──────────────────────────────────────────────
# Mock service functions
# ──────────────────────────────────────────────
VALID_TOKENS = {"demo-token": {"customer_id": "cust_001", "name": "Riya Kapoor"}}

def validate_bank_token(token: str) -> Optional[dict]:
    """Synchronous token lookup – swap for real JWT verification in production."""
    return VALID_TOKENS.get(token)

async def handle_message(session_id: str, user_text: str) -> MessageResponse:
    """
    Orchestrates a reply.  Replace with real LLM + RAG + advisory engine.
    """
    lower = user_text.lower()
    recs: List[str] = []

    if any(k in lower for k in ["doing", "summary", "overview"]):
        reply = ("You saved 22% of your income this month — above your usual 18%. "
                 "Your SIPs are on track and your fixed deposit of ₹1.5L is earning 6.1% p.a.")
    elif any(k in lower for k in ["sip", "mutual fund", "investment"]):
        reply = ("Your SIP of ₹5,000/month into the Hybrid Equity Fund is active. "
                 "You've accumulated ₹74,200 so far and are on track for the First Car goal.")
        recs = ["rec_sip_001"]
    elif any(k in lower for k in ["recommend", "suggest", "advice"]):
        reply = ("Your ₹1.5L Fixed Deposit has been dormant for 14 months and earns 6.1%. "
                 "Given your 2-year goal horizon and moderate risk profile, a hybrid fund could target higher returns. "
                 "Want to know why I'm suggesting this?")
        recs = ["rec_fd_realloc_001"]
    elif any(k in lower for k in ["risk", "profile"]):
        reply = ("Your risk profile is Moderate — updated in March 2026 after your salary hike. "
                 "This means you're comfortable with moderate market exposure for 2–3 year horizons.")
    elif any(k in lower for k in ["spend", "expense", "dining", "lunch"]):
        reply = ("Dining-out is up ₹3,200 vs your average this month — mostly weekday lunches. "
                 "It's the 3rd week in a row, but your savings rate is still healthy at 22%.")
    elif any(k in lower for k in ["goal", "car", "vacation", "emergency"]):
        reply = ("First Car goal: 48% funded (₹2.4L of ₹5L) — on track for Jun 2027. "
                 "Europe Vacation goal: only 29% funded with 9 months left — at risk.")
    elif any(k in lower for k in ["rm", "advisor", "human", "priya", "theek", "baat", "confirm"]):
        reply = ("Bilkul! I'll connect you with your RM, Priya Sharma. "
                 "I'll send her a summary of our conversation so she's already up to speed.")
    elif any(k in lower for k in ["hello", "hi", "hey", "namaste"]):
        reply = ("Hello Riya! 👋 I'm Artha, your personal wealth advisor. "
                 "You saved 22% of your income this month. "
                 "Want the quick version or the full breakdown?")
    else:
        reply = ("I can help you with your portfolio, SIPs, spending patterns, goals, "
                 "or recommendations. What would you like to explore?")

    return MessageResponse(reply_text=reply, recommendation_ids=recs)

async def synthesize_voice(text: str, language: str) -> VoiceSynthesisResponse:
    return VoiceSynthesisResponse(
        audio_url="https://example.com/audio.mp3",
        duration_ms=2000,
        viseme_cues=[
            {"atMs": 0,   "shape": "closed"},
            {"atMs": 300, "shape": "open_wide"},
            {"atMs": 700, "shape": "narrow"},
        ]
    )

# ──────────────────────────────────────────────
# App
# ──────────────────────────────────────────────
app = FastAPI(title="ARTHA API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # in production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    token = credentials.credentials if credentials else None
    user_info = validate_bank_token(token) if token else None
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token. Use 'demo-token' for the demo."
        )
    return user_info

# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "service": "ARTHA API Gateway", "time": datetime.datetime.utcnow().isoformat()}

@app.post("/v1/session/start", response_model=SessionStartResponse)
def start_session(req: SessionStartRequest, user=Depends(get_current_user)):
    session_id = "sess_" + str(uuid.uuid4())[:8]
    return SessionStartResponse(
        session_id=session_id,
        customer_id=user["customer_id"],
        language=req.language
    )

@app.post("/v1/conversation/message", response_model=MessageResponse)
async def conversation_message(req: MessageRequest, user=Depends(get_current_user)):
    return await handle_message(req.session_id, req.message_text)

@app.post("/v1/recommendations/{rec_id}/feedback")
def recommendation_feedback(rec_id: str, req: RecommendationFeedbackRequest, user=Depends(get_current_user)):
    # In production: persist to audit log
    print(f"[AUDIT] rec={rec_id} feedback={req.feedback} user={user['customer_id']}")
    return {"status": "recorded", "rec_id": rec_id}

@app.post("/v1/voice/synthesize", response_model=VoiceSynthesisResponse)
async def voice_synthesize(req: VoiceSynthesisRequest, user=Depends(get_current_user)):
    return await synthesize_voice(req.text, req.language)
