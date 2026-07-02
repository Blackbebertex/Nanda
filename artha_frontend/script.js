// ============================================================
// ARTHA AI – Frontend ↔ FastAPI Backend Connector
// ============================================================
const BACKEND_URL = "http://localhost:8000";
const DEMO_TOKEN  = "demo-token";

let sessionId = null;
let isRecording = false;

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
    appendBotMessage(
      "👋 Good morning, Riya! I'm Artha, your personal wealth advisor. You saved **22%** of your income this month — above your usual 18%! Want a quick update or the full breakdown?",
      null
    );
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

  // Convert **bold** markdown
  bubble.innerHTML = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

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
  animateAvatar();
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

// ---- Avatar mouth animation --------------------------------
function animateAvatar() {
  const mouth = document.getElementById("avatar-mouth");
  mouth.classList.add("talking");
  setTimeout(() => mouth.classList.remove("talking"), 2500);
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

    // Build a smarter demo reply if backend returns generic mock
    const replyText = buildSmartReply(text, data.reply_text, lang);
    const rec = data.recommendation_ids?.length ? buildMockRec(text) : null;

    appendBotMessage(replyText, rec);
  } catch (e) {
    hideTyping();
    appendBotMessage("❌ Couldn't reach the backend. Is the FastAPI server running? (`uvicorn main:app --port 8000`)", null);
  }
}

function sendSuggestion(text) {
  document.getElementById("user_input").value = text;
  sendMessage();
}

// ---- Smart demo reply builder ------------------------------
const responses = {
  "how am i doing": "You're doing great this month, Riya! 🎉 You saved **22%** of your income (₹12,760), which is above your 18% average. Your SIPs are on track for the **First Car** goal, and you have ₹38,200 in your savings account.",
  "sip": "Your SIP of **₹5,000/month** into the Hybrid Equity Fund is active and on track. You've accumulated **₹74,200** so far. At this rate, you'll hit the ₹1,20,000 milestone in ~10 months.",
  "recommendation": "Based on your profile, I have one suggestion: your **Fixed Deposit of ₹1.5L** is earning 6.1% and has been untouched for 14 months. A short-horizon hybrid fund could realistically target higher returns given your 2-year goal horizon and moderate risk profile. Want to know why?",
  "risk profile": "Your risk profile was updated to **Moderate** in March 2026 after your salary hike of 18%. This means you're comfortable with some market exposure for potentially higher returns over 2–3 year horizons.",
  "spending": "This month, dining-out spending is up **₹3,200** vs your average — mostly weekday lunches. Not a problem, just flagging it since it's the 3rd week in a row. Your savings rate (22%) is still healthy.",
  "goal": "Your **First Car** goal is 48% funded (₹2,40,000 of ₹5,00,000). You're on track for June 2027 if SIPs continue. Your Europe Vacation goal (March 2026) is at risk — only 29% funded with 9 months to go.",
  "rm": "I'll connect you with your RM, **Priya Sharma**, right away. I'll send her a summary of our conversation and your current portfolio. She'll reach out within 24 hours. 📋",
  "hindi": "Bilkul! Main aapko Hindi mein bata sakti hoon. Aapki savings rate is mahine 22% hai — yeh aapke average se behtar hai. Aapka SIP bhi First Car goal ke liye sahi track pe hai. 🎯",
  "theek": "Bilkul sahi soch hai. Main aapki RM, Priya Sharma, ko ek summary bhej deti hoon — aap unse seedha baat kar sakti hain. 📋",
  "why": "Three reasons for this recommendation: 1) Your FD has been dormant for **14 months**, 2) Your goal horizon is **2 years** — matching a hybrid fund's risk window, 3) Your risk profile moved from conservative to **moderate** in March. None of this is a push to invest more — just to place what you have more efficiently.",
  "default": "I understand, Riya. Based on your current financial data, you're in a healthy position. Your savings rate is above average and your SIPs are active. Is there a specific aspect of your finances you'd like to explore?"
};

function buildSmartReply(userText, backendReply, lang) {
  const lower = userText.toLowerCase();
  if (lang === "hi" || lower.includes("theek") || lower.includes("hindi")) return responses["theek"];
  for (const [key, val] of Object.entries(responses)) {
    if (key !== "default" && lower.includes(key)) return val;
  }
  // If backend returned something useful (not just the echo), use it
  if (backendReply && !backendReply.startsWith("You said:")) return backendReply;
  return responses["default"];
}

function buildMockRec(userText) {
  if (userText.toLowerCase().includes("recommendation") || userText.toLowerCase().includes("suggest")) {
    return {
      reasonCode: "DORMANT_FD_REALLOCATION",
      facts: {
        "Account": "Fixed Deposit – HDFC (acc_fd_882)",
        "Current Rate": "6.1% p.a.",
        "Months Dormant": "14",
        "Matching Goal": "First Car (Jun 2027)",
        "Risk Profile": "Moderate",
      },
    };
  }
  return null;
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
    // Simulate voice after 2 seconds
    setTimeout(() => stopVoice("How am I doing this month?"), 2500);
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
