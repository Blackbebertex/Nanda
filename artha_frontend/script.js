// ============================================================
// ARTHA AI – Frontend ↔ FastAPI Backend Connector
// ============================================================
const BACKEND_URL = "http://localhost:8000";
const DEMO_TOKEN  = "demo-token";

let sessionId = null;
let isRecording = false;
let currentVoiceAudio = null;
let visemeTimeouts = [];

// ---- Utility -----------------------------------------------
function now() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

async function apiPost(path, body) {
  const res = await fetch(`${BACKEND_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${DEMO_TOKEN}`,
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ---- Session -----------------------------------------------
async function startSession() {
  setStatus("Connecting…", false);
  try {
    const data = await apiPost("/v1/session/start", { language: "en" });
    sessionId = data.session_id;
    setStatus("Connected · Session " + sessionId, true);
    
    // Initial welcome message from backend
    appendBotMessage(
      "👋 Good morning, Riya! I'm Artha, your personal wealth advisor. You saved **22%** of your income this month — above your usual 18%! Want a quick update or the full breakdown?",
      null
    );
    // Play voice for the initial welcome
    playVoiceAndAnimate("Good morning, Riya! I'm Artha, your personal wealth advisor. You saved 22% of your income this month — above your usual 18%! Want a quick update or the full breakdown?", "en");
  } catch (e) {
    setStatus("Backend offline – check uvicorn is running on port 8000", false);
    appendBotMessage("⚠️ I couldn't connect to the backend. Please make sure the FastAPI server is running on http://localhost:8000", null);
  }
}

// ---- Status bar --------------------------------------------
function setStatus(text, ok) {
  document.getElementById("status-text").textContent = text;
  const dot = document.getElementById("backend-status");
  dot.className = "status-dot-small " + (ok ? "connected" : "disconnected");
}

// ---- Tab switching -----------------------------------------
function switchTab(name) {
  document.querySelectorAll(".tab-panel").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
  document.getElementById("tab-" + name).classList.add("active");
  document.getElementById("nav-" + name).classList.add("active");
}

// ---- Clear chat --------------------------------------------
function clearChat() {
  // Stop active voice / animations
  if (currentVoiceAudio) {
    currentVoiceAudio.pause();
    currentVoiceAudio = null;
  }
  visemeTimeouts.forEach(clearTimeout);
  visemeTimeouts = [];
  applyMouthShape(document.getElementById("avatar-mouth"), "closed");

  document.getElementById("chat-messages").innerHTML = "";
  document.getElementById("chat-suggestions").style.display = "flex";
  startSession();
}

// ---- Sidebar toggle (mobile) --------------------------------
function toggleSidebar() {
  const sb = document.getElementById("sidebar");
  sb.style.display = sb.style.display === "none" ? "flex" : "none";
}

// ---- Chat rendering ----------------------------------------
function appendBotMessage(text, recommendation) {
  hideSuggestions();
  const row = document.createElement("div");
  row.className = "msg-row bot";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot";
  avatar.textContent = "₳";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble bot";

  // Safely parse **bold** markdown to avoid XSS
  const parts = text.split(/(\*\*.*?\*\*)/g);
  parts.forEach(part => {
    if (part.startsWith("**") && part.endsWith("**") && part.length >= 4) {
      const strong = document.createElement("strong");
      strong.textContent = part.slice(2, -2);
      bubble.appendChild(strong);
    } else if (part.length > 0) {
      bubble.appendChild(document.createTextNode(part));
    }
  });

  const timeEl = document.createElement("div");
  timeEl.className = "msg-time";
  timeEl.textContent = now();
  bubble.appendChild(timeEl);

  if (recommendation) {
    bubble.appendChild(buildRecCard(recommendation));
  }

  row.appendChild(avatar);
  row.appendChild(bubble);
  document.getElementById("chat-messages").appendChild(row);
  scrollChat();
}

function appendUserMessage(text) {
  hideSuggestions();
  const row = document.createElement("div");
  row.className = "msg-row user";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar user";
  avatar.textContent = "R";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble user";
  bubble.textContent = text;

  const timeEl = document.createElement("div");
  timeEl.className = "msg-time";
  timeEl.textContent = now();
  bubble.appendChild(timeEl);

  row.appendChild(avatar);
  row.appendChild(bubble);
  document.getElementById("chat-messages").appendChild(row);
  scrollChat();
}

function showTyping() {
  const row = document.createElement("div");
  row.className = "msg-row bot";
  row.id = "typing-row";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot";
  avatar.textContent = "₳";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble bot typing-indicator";
  bubble.innerHTML = "<div class='dot'></div><div class='dot'></div><div class='dot'></div>";

  row.appendChild(avatar);
  row.appendChild(bubble);
  document.getElementById("chat-messages").appendChild(row);
  scrollChat();
}

function hideTyping() {
  const row = document.getElementById("typing-row");
  if (row) row.remove();
}

function buildRecCard(rec) {
  const card = document.createElement("div");
  card.className = "rec-card";
  card.innerHTML = `
    <div class="rec-card-header">💡 Recommendation · ${rec.reasonCode || "ADVISORY"}</div>
    <div class="rec-facts">
      ${Object.entries(rec.facts || {}).map(([k,v]) => `<div class="rec-fact">${k}: <span>${v}</span></div>`).join("")}
    </div>
    <div class="rec-actions">
      <button class="rec-btn primary" onclick="sendSuggestion('Tell me more about this recommendation')">Tell me more</button>
      <button class="rec-btn" onclick="sendSuggestion('Connect me to my RM')">Talk to RM</button>
      <button class="rec-btn" onclick="this.closest('.rec-card').remove()">Dismiss</button>
    </div>
  `;
  return card;
}

function hideSuggestions() {
  document.getElementById("chat-suggestions").style.display = "none";
}

function scrollChat() {
  const el = document.getElementById("chat-messages");
  el.scrollTop = el.scrollHeight;
}

// ---- Lipsync Avatar Viseme Controller ----------------------
function playVoiceAndAnimate(text, language) {
  // Clear running instances
  if (currentVoiceAudio) {
    try { currentVoiceAudio.pause(); } catch(e){}
    currentVoiceAudio = null;
  }
  visemeTimeouts.forEach(clearTimeout);
  visemeTimeouts = [];
  
  const mouth = document.getElementById("avatar-mouth");
  applyMouthShape(mouth, "closed");
  
  // Call backend voice synthesize API
  apiPost("/v1/voice/synthesize", { text: text, language: language })
    .then(data => {
      // 1. Play the audio channel
      currentVoiceAudio = new Audio(data.audio_url);
      currentVoiceAudio.play().catch(e => console.log("Audio playback blocked/failed:", e));
      
      // 2. Synchronize mouth shapes using server timing cues
      data.viseme_cues.forEach(cue => {
        const timer = setTimeout(() => {
          applyMouthShape(mouth, cue.shape);
        }, cue.atMs);
        visemeTimeouts.push(timer);
      });
    })
    .catch(err => {
      console.warn("Could not load lipsync voice stream:", err);
    });
}

function applyMouthShape(mouth, shape) {
  if (!mouth) return;
  mouth.style.transition = "all 0.1s ease-in-out";
  
  if (shape === "closed") {
    mouth.style.height = "2px";
    mouth.style.borderRadius = "0";
    mouth.style.width = "14px";
    mouth.style.borderBottom = "2px solid rgba(255,255,255,0.6)";
  } else if (shape === "open_wide") {
    mouth.style.height = "10px";
    mouth.style.borderRadius = "50%";
    mouth.style.width = "12px";
    mouth.style.borderBottom = "3px solid var(--accent-light)";
  } else if (shape === "narrow") {
    mouth.style.height = "5px";
    mouth.style.borderRadius = "50%";
    mouth.style.width = "6px";
    mouth.style.borderBottom = "3px solid var(--accent-light)";
  } else if (shape === "open_mild") {
    mouth.style.height = "5px";
    mouth.style.borderRadius = "40%";
    mouth.style.width = "14px";
    mouth.style.borderBottom = "3px solid var(--accent-light)";
  } else if (shape === "wide_smile") {
    mouth.style.height = "3px";
    mouth.style.borderRadius = "0 0 10px 10px";
    mouth.style.width = "16px";
    mouth.style.borderBottom = "3px solid var(--accent-light)";
  }
}

// ---- Send message ------------------------------------------
async function sendMessage() {
  const input = document.getElementById("user_input");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";

  appendUserMessage(text);
  showTyping();

  // Detect language switch for Hindi keywords
  const lang = detectLang(text);
  document.getElementById("lang-chip").textContent = lang === "hi" ? "HI" : "EN";

  try {
    if (!sessionId) await startSession();

    const data = await apiPost("/v1/conversation/message", {
      session_id: sessionId,
      message_text: text,
    });

    hideTyping();

    const replyText = data.reply_text;
    const rec = data.recommendation; // Dynamically parsed from backend recommendation object

    appendBotMessage(replyText, rec);
    
    // Play voice and lipsync anims in sync with reply text
    playVoiceAndAnimate(replyText.replace(/\*\*|👋|📊|🎯|💡|📋|❌|⚠️|💰|🎉/g, ""), lang);
  } catch (e) {
    hideTyping();
    appendBotMessage("❌ Couldn't reach the backend. Is the FastAPI server running? (`uvicorn main:app --port 8000`)", null);
  }
}

function sendSuggestion(text) {
  document.getElementById("user_input").value = text;
  sendMessage();
}

// ---- Language detection ------------------------------------
function detectLang(text) {
  const hindiPattern = /[\u0900-\u097F]|theek|kya|aap|nahi|hai|main|hoon/i;
  return hindiPattern.test(text) ? "hi" : "en";
}

// ---- Voice (mock – shows recording state) ------------------
function toggleVoice() {
  const btn = document.getElementById("mic-btn");
  if (!isRecording) {
    isRecording = true;
    btn.classList.add("recording");
    btn.textContent = "⏹️";
    document.getElementById("user_input").placeholder = "Listening…";
    // Simulate voice transcript after 2 seconds
    setTimeout(() => stopVoice("How am I doing this month?"), 2000);
  } else {
    stopVoice(null);
  }
}

function stopVoice(transcript) {
  isRecording = false;
  const btn = document.getElementById("mic-btn");
  btn.classList.remove("recording");
  btn.textContent = "🎤";
  document.getElementById("user_input").placeholder = "Ask Artha anything about your finances…";
  if (transcript) {
    document.getElementById("user_input").value = transcript;
    sendMessage();
  }
}

// ---- Enter key sends message --------------------------------
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("user_input").addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
  });
  startSession();
});
