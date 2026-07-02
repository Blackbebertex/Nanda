# ARTHA AI
**An Avatar-Led Digital Wealth Advisor, Built Into the Bank's Own App**
*Track 01 • Hackathon Submission Blueprint & Complete Build Manual*

## PART A: THE BLUEPRINT

### Section 01 — The Problem, In Context

**Problem Statement:** Wealth management and advisory services remain fragmented and largely inaccessible to a large share of customers. Banks lack a comprehensive, continuously-updated view of a customer's investment behaviour and spending habits, which limits their ability to offer timely, personalised, data-driven guidance.

**Expected Outcome:** An AI-powered, avatar-based Digital Wealth Management application that integrates directly into the bank's existing mobile app, delivering personalised and scalable advisory services through an intuitive conversational interface.

#### Why this matters right now
India's retail investing base has grown extraordinarily fast: demat accounts have crossed roughly 21–22 crore, monthly SIP inflows are running close to ₹30,000 crore, and total mutual fund AUM is approaching ₹80 lakh crore. Nearly four in ten new investors are under 30, and a growing share of this growth is coming from Tier-2 and Tier-3 towns, not just metros.

Yet most of these new investors have no real advisor. They have a trading app that shows them a portfolio, not someone who explains why it matters, whether it still matches their goals, or what their actual spending behaviour says about their financial health. Human wealth advisory is expensive to scale — it depends on relationship managers who can only serve a few hundred clients each. Generic robo-advisory tools, meanwhile, tend to ask the customer to re-enter data the bank already has, and rarely look beyond a single account.

#### The gap ARTHA AI is built to close
* **Fragmentation** — a customer's mutual funds, deposits, loans, insurance, and spending live in different systems; nobody assembles them into one picture.
* **One-size-fits-all advice** — static risk questionnaires from years ago don't reflect a customer's current life stage or behaviour.
* **No habit insight** — spending and saving patterns are rarely connected back to investment recommendations.
* **Trust and access** — first-time investors, especially outside metros, want guidance in their own language, in a format that feels like a conversation, not a dashboard full of jargon.

> "The opportunity isn't 'another investing app.' It's turning the bank's own mobile app — which the customer already trusts and already opens daily — into the place where they get advice, not just account access."

---

### Section 02 — The Solution: ARTHA AI

ARTHA AI (from the Sanskrit *artha*, meaning wealth or purpose) is an avatar-led digital wealth advisor embedded directly inside the bank's mobile app. Customers talk to it the way they'd talk to a knowledgeable relationship manager — by text or voice, in their preferred language — and it responds with a visible, expressive avatar rather than a wall of charts.

#### The one-line pitch
"ARTHA gives every banking customer a personal wealth advisor who already knows their accounts, remembers their goals, and explains money in plain language — built right into the app they already use."

#### How it maps to the brief

| Expected Outcome | How ARTHA AI Delivers It |
| :--- | :--- |
| **AI-powered Digital Wealth Management** | LLM-driven advisory engine that combines portfolio data, financial product knowledge, and customer context into specific, explainable recommendations. |
| **Avatar-based** | A consistent visual + voice persona (2D/3D, multilingual) that customers can see and hear, building familiarity and trust over repeated interactions. |
| **Integrates into bank's mobile app** | Delivered as an embeddable module / SDK rather than a separate app, reusing the bank's existing login, KYC, and core banking session. |
| **Personalised and scalable** | Account Aggregator-powered 360° financial view + behavioural analytics, served by an AI engine that scales to millions of customers without a 1:1 human cost. |
| **Intuitive digital interface** | Conversation-first design: no forms to fill, no jargon by default, plain-language explanations with an option to "show the math." |

#### Three pillars
1. **See everything** — Pull a true 360° view of accounts, investments, liabilities, and spending via consented data sharing.
2. **Understand the person** — Translate raw transaction data into a behavioural and risk profile that updates continuously, not once at onboarding.
3. **Advise like a human, scale like software** — Generate explainable, compliant guidance through a conversational avatar, with a clear handoff to a licensed human advisor when needed.

---

### Section 03 — Who It's For

Designing one avatar that works for everyone is the wrong goal. ARTHA needs to recognise which kind of customer it's talking to and adjust depth, tone, and pacing accordingly.

#### Personas
* **A — Riya, 27, First Jobber**
  New salaried employee, just started SIPs, anxious about market dips, wants reassurance and simple goal tracking (first car, an emergency fund). Prefers chat over voice, mostly in English.
* **B — Suresh, 42, Small Business Owner**
  Irregular income, mixes personal and business spending, under-insured, wants tax-efficient guidance and cash-flow visibility more than stock picks. Comfortable with Hindi/voice.
* **C — Lata, 61, Retiree**
  Has fixed deposits and a pension, worried about outliving savings and about fraud, wants a calm, simple voice-first experience in her regional language, with easy escalation to a real person.

#### Design implication
The avatar's tone, vocabulary, and even the channel it defaults to (chat vs. voice) should adapt per persona. For the hackathon demo, picking one persona to demo deeply (Riya works well — relatable, fast to build for) and briefly describing the other two in the pitch is usually more convincing than building three shallow flows.

#### Non-customer stakeholders
* **Relationship managers** — need a dashboard showing which customers ARTHA has flagged for human follow-up, and why.
* **Compliance/Risk teams** — need an audit trail of every recommendation ARTHA made and the data it was based on.
* **Bank's product/IT team** — need ARTHA to be an embeddable module, not a parallel app they have to separately market.

---

### Section 04 — Core Feature Set

Build features 1–4 for a hackathon-credible MVP. Features 5–8 are what turn it from a demo into a product — mention them on a roadmap slide even if not built.

| # | Feature | Description |
| :--- | :--- | :--- |
| 1 | **Avatar Conversation** | Text + voice chat with a persistent visual avatar; multilingual (English, Hindi, +1 regional language for demo impact). |
| 2 | **360° Financial View** | Aggregates accounts, investments, and liabilities across institutions via consented data sharing, not just this bank's own data. |
| 3 | **Dynamic Risk Profiling** | Risk and goal profile that updates from actual behaviour over time, not a one-time onboarding quiz. |
| 4 | **Explainable Recommendations** | Specific, reasoned suggestions with a visible "why" behind each one. |
| 5 | **Spending Insight & Nudges** | Pattern detection on spending categories, with gentle, non-judgemental nudges rather than alarms. |
| 6 | **Proactive Alerts** | Goal drift, market-linked events, policy/SIP renewal reminders — delivered conversationally, not as raw push notifications. |
| 7 | **Human Handoff** | One-tap escalation to a licensed relationship manager or investment adviser for regulated or high-stakes decisions. |
| 8 | **Avatar Personalisation** | Customer can choose avatar appearance, voice, and language — small touch, large effect on adoption and trust. |

#### MVP cut line for the hackathon
| Build for demo | Mock or simplify | Mention only (roadmap) |
| :--- | :--- | :--- |
| Avatar chat (1), one persona's 360° view (2), 3–4 canned-but-data-driven recommendations (4) | Risk profiling (3) using a short quiz; spending insight (5) on pre-loaded sample dataset | Proactive alerts (6), human handoff (7), avatar personalisation (8) |

---

### Section 05 — System Architecture

Five layers, each replaceable independently — important for a hackathon, where you'll mock the bottom layers and build the top ones for real.

**Layer 1 — Bank Mobile App (Existing)**
Avatar UI module (chat + voice) embedded in current app shell. Reuses existing login & session.

**Layer 2 — API Gateway & Auth**
Token validation, rate limiting, routes requests to orchestration services.

**Layer 3 — Orchestration Microservices**
*   **Conversation Orchestrator** — Manages dialogue state
*   **Advisory & Risk Engine** — Scoring + recommendations
*   **Avatar & Voice Service** — TTS / STT / rendering
*   **Notification Service** — Alerts & nudges

**Layer 4 — AI / ML Core**
LLM + RAG for conversation, behavioural analytics models, recommendation / portfolio scoring models, guardrails & compliance filters.

**Layer 5 — Data & Integration**
Core banking APIs, Account Aggregator (consent-based external data), Customer 360 store, Vector DB for product knowledge, Audit log.

*Why this layering matters for a hackathon:* You can fully mock Layer 5 with a sample dataset, build a thin but real Layer 3 and 4, and the judges will still see an end-to-end, architecturally sound system — not a single hard-coded chatbot script.

---

### Section 06 — How ARTHA "Thinks": The AI Engine

Four cooperating sub-systems, not one monolithic model.

#### 1. Conversational layer (LLM + RAG)
A large language model handles natural dialogue, but it should never "freelance" financial facts. Ground every factual claim in a retrieval step over: the customer's actual account data, the bank's product catalogue (fund names, interest rates, fees), and regulatory disclosure text. This is a classic Retrieval-Augmented Generation (RAG) pattern: retrieve the relevant facts first, then let the LLM phrase the response in plain language.

#### 2. Behavioural analytics layer
A separate, simpler pipeline (not the LLM) computes structured signals from transaction data — spending-category breakdowns, savings rate trend, income regularity, anomaly/fraud flags. These signals become inputs to the advisory layer; they are not invented by the chatbot in real time.

#### 3. Advisory / recommendation layer
A rules engine (hard regulatory and risk constraints) combined with a scoring model (which products fit this risk band, goal horizon, and liquidity need) produces a short, ranked list of recommendations. Each recommendation carries a machine-readable "reason code" so the avatar can always answer "why are you suggesting this?" with a real, traceable answer — not a hallucinated justification.

#### 4. Avatar / presentation layer
Text-to-speech and speech-to-text convert between the dialogue layer and the visual avatar; for video/3D avatars, viseme or lip-sync data drives mouth movement in time with audio. Keep this layer swappable — for a hackathon, a 2D animated avatar with synced audio is far more reliable to demo live than a 3D render pipeline.

#### Guardrails that should never be skipped
*   Every recommendation is logged with the data and reasoning behind it — this audit trail is what compliance teams will ask for first.
*   The avatar should explicitly flag when something needs a licensed human advisor, rather than ever implying it alone is sufficient for a regulated decision.
*   If the model is uncertain or the data is incomplete, ARTHA should say so plainly instead of generating a confident-sounding guess.

---

### Section 07 — Avatar & Conversation Design

#### Persona brief
*   **Name:** Artha
*   **Traits:** calm, precise, warm but never sugar-coating risk
*   **Voice:** speaks like a trusted senior colleague, not a salesperson
*   **Never does:** use fear to push a product, bury a "why" behind jargon, or pretend certainty it doesn't have.

#### Tone guidelines
*   **Lead with the customer's situation, not the product:** "Your rent is taking up 41% of your income this month" before "consider this fund."
*   **Quantify, don't alarm:** prefer concrete numbers over emotionally loaded words like "dangerous" or "risky behaviour."
*   **Always offer the "why" and the "what if I don't" in one or two sentences, then stop** — avoid long lectures.
*   **Default to the customer's preferred language** and switch fluidly if they code-switch mid-conversation (very common in Indian English-Hindi usage).

#### Sample exchange — weekly check-in
**Artha:** Good evening, Riya. Quick update: your SIPs are on track, but I noticed dining-out spending is up about ₹3,200 versus your usual month. Want me to show you where it's going?
**Riya:** Yeah go ahead
**Artha:** Most of it's weekday lunches near your office. Not a problem at all — just flagging it because it's the third week in a row. If it's intentional, no action needed from me.

#### Multilingual & voice notes
For the demo, pick two languages (e.g. English + Hindi) and show a clean code-switch mid-conversation — this single moment is often the most memorable part of a wealth-AI demo for Indian judges, since it directly signals inclusion for Tier-2/3 customers. Keep sentences short for the TTS voice; long, clause-heavy sentences sound noticeably more robotic than short ones, regardless of which TTS engine you use.

---

### Section 08 — Data, Privacy & Compliance

This section is the single biggest differentiator for a banking-track hackathon judge — most student teams skip it entirely.

#### The Account Aggregator (AA) framework
RBI's Account Aggregator framework is exactly the regulatory mechanism this problem statement implicitly needs. It lets a customer consent to share financial data between regulated entities through a licensed NBFC-Account Aggregator that never reads the data itself — it only routes it, encrypted, between a Financial Information Provider (FIP, e.g. a bank or mutual fund RTA) and a Financial Information User (FIU, which is what ARTHA AI would register as). Every share is governed by a signed "consent artefact" specifying exactly what data, for how long, and for what purpose.

The ecosystem has scaled rapidly: well over a billion accounts are technically enabled for sharing, though only a few hundred million customers have actually linked an account so far — meaning there's still a large unconverted opportunity. Established NBFC-AAs you can integrate with (most offer sandbox access) include Finvu, OneMoney, CAMSFinServ, Setu AA, Anumati, and NADL. RBI recently recognised Sahamati as the ecosystem's self-regulatory body.

> *FIP = data holder (bank, AMC, insurer) · FIU = data consumer (ARTHA AI) · AA = consent-based, data-blind router*

#### Where "advice" becomes regulated
SEBI draws a line between general financial guidance/education and personalised investment "advice" given for a fee, which requires Investment Adviser registration. A practical, demo-safe positioning: ARTHA gives *personalised information and guidance* and explicitly routes any decision that constitutes *regulated advice* to a licensed human adviser or to mutual fund distribution flows the bank is already authorised for. Say this clearly in your pitch — it shows the judges you understand the regulatory boundary rather than having missed it.

#### Other compliance touchpoints
| Area | What it requires of ARTHA AI |
| :--- | :--- |
| **RBI digital lending / data norms** | Data localisation for sensitive financial data, encrypted storage, and clear consent logs for any data fetched. |
| **DPDP Act, 2023** | Purpose limitation, data minimisation, and a user-facing way to view and revoke what's been collected — not just AA-sourced data, but everything ARTHA stores. |
| **KYC / customer authentication** | Reuse the bank's existing KYC and session — never re-collect identity data inside the avatar flow. |
| **Model governance** | Every AI-generated recommendation logged with its inputs and reasoning for after-the-fact audit and dispute resolution. |

---

### Section 09 — Recommended Tech Stack

Optimised for "buildable in a hackathon, credible as a production direction."

| Layer | Hackathon-Speed Choice | Production-Grade Direction |
| :--- | :--- | :--- |
| **Mobile UI module** | React Native or Flutter screen embedded in a demo shell app | Native SDK/module shipped into the bank's existing app codebase |
| **Backend services** | Node.js (Express/NestJS) or Python (FastAPI) microservices | Same, containerised on Kubernetes behind an API gateway (Kong/Apigee) |
| **Conversational AI** | Claude or another LLM API with a RAG layer over a small product/FAQ knowledge base | Same pattern, with fine-tuned guardrail classifiers and a compliance review queue |
| **Vector store (for RAG)** | pgvector on Postgres, or a lightweight in-memory store for the demo | Managed vector DB (e.g. Pinecone/Weaviate) with refresh pipelines |
| **Avatar rendering** | 2D animated avatar (Lottie/Rive) driven by TTS audio timing | 3D or video-based avatar via a dedicated avatar API, with viseme-level lip-sync |
| **Speech (STT/TTS)** | Open-source Whisper for STT; cloud neural TTS with Indian-language voices | Same, with per-language voice tuning and latency optimisation for real-time feel |
| **External financial data** | Mocked AA responses (sample JSON payloads modelled on the real AA data schema) | Live integration with a licensed NBFC-AA (e.g. Setu AA, Finvu) sandbox, then production |
| **Database** | PostgreSQL for structured data, Redis for session/conversation state | Same, plus an event stream (Kafka) for behavioural analytics pipelines |
| **Security** | Standard HTTPS, JWT auth for the demo | Secrets vault, field-level encryption for PII, WAF, full audit logging |

*A note on build effort:* The single highest-leverage thing to get right in limited time is the conversation + recommendation loop on a realistic-looking dataset. Judges remember a smooth, sensible conversation far more than they remember architectural slides — build the demo path deep, and keep everything else (especially the avatar's visual fidelity) as simple as it can be while still looking intentional.

---

### Section 10 — Build Roadmap

#### Hackathon timeline (adapt to your actual hour count)
| Time | Action | Detail |
| :--- | :--- | :--- |
| **Hr 0–2** | **Lock the demo story.** | Pick one persona (Riya), write the exact 6–8 turn conversation you want to show, and build a small but realistic mock dataset (accounts, transactions, SIPs). |
| **Hr 2–8** | **Backend skeleton.** | Stand up the conversation API, connect it to the LLM with a simple RAG layer over the mock dataset, and get a basic recommendation rule working end-to-end (even if just 2–3 rules). |
| **Hr 8–16** | **Avatar + voice.** | Wire up TTS for spoken responses and a simple animated avatar synced to audio. Add STT for voice input if time allows; text-only input is an acceptable fallback. |
| **Hr 16–24** | **Advisory depth + UI polish.** | Add the "why" behind each recommendation, the spending-insight nudge, and clean up the mobile screen to look embedded rather than standalone. |
| **Hr 24–30** | **Multilingual moment + edge cases.** | Add the Hindi (or regional language) code-switch demo, and test what happens when the model doesn't know something — make sure it degrades gracefully. |
| **Hr 30–36** | **Rehearse the pitch.** | Run the exact demo script three times, time it, and prepare answers for "is this SEBI-registered advice?" and "how is this different from existing robo-advisors?" |

#### Beyond the hackathon — path to a real pilot
| Phase | Duration | Focus |
| :--- | :--- | :--- |
| **MVP hardening** | ~3 months | Replace mocks with a real AA sandbox integration, add compliance audit logging, security review. |
| **Single-branch pilot** | ~6 months | Live with a limited, opted-in customer group; human-in-the-loop review of every AI recommendation before launch. |
| **Scale-up** | ~12 months | Multi-language rollout, RM dashboard, formal SEBI/compliance sign-off, full production data pipeline. |

---

### Section 11 — Demo Script

A rehearsed, six-turn flow that shows discovery, personalised data, an explainable recommendation, and a language switch — all in under two minutes.

**Riya (opens app, taps Artha):** Hey Artha, how am I doing this month?
**Artha:** Hi Riya! Overall, good — you saved 22% of your income this month, slightly above your usual 18%. Want the quick version or the full breakdown?
**Riya:** Quick version
**Artha:** Your SIPs are on track for your "First Car in 2 Years" goal. One thing worth a look: your fixed deposit of ₹1.5L is earning 6.1%, while your goal horizon and risk profile suggest a hybrid fund could realistically target higher returns with similar safety. Want to see why I'm suggesting that?
**Riya:** Yeah, why?
**Artha:** Three reasons: your goal is 2 years out, you haven't touched this FD in 14 months, and your risk profile moved from "conservative" to "moderate" after your salary hike in March. None of this is a push to invest more — just to place what you already have more efficiently.
**Riya (switches to Hindi):** Theek hai, par main isko apni RM se bhi confirm karna chahti hoon
**Artha:** Bilkul sahi soch hai. Main aapki RM, Priya Sharma, ko ek summary bhej deti hoon — aap unse seedha baat kar sakti hain.

#### What this script proves to judges, on purpose
1.  **Real personalisation** (specific numbers, dates, and a named goal) — not a generic chatbot script.
2.  **Explainability** is a first-class feature, not an afterthought.
3.  The **human-advisor handoff** is built in, not bolted on after a compliance objection.
4.  A natural, mid-conversation **language switch** — the single most memorable inclusion signal you can show live.

---

### Section 12 — Why Judges Will Remember This

#### Differentiation, stated plainly
*   **Real data, not a generic robo-advisor demo** — grounded in the Account Aggregator framework, which is actual live Indian banking infrastructure, not a hypothetical.
*   **Bank-native, not a new app to download** — embedded inside the mobile app the customer already trusts, which is exactly what the brief asks for.
*   **Compliance-aware by design** — the team clearly understands where AI guidance ends and licensed advice begins, instead of glossing over it.
*   **Inclusion angle backed by real numbers** — multilingual, voice-first design directly targets the Tier-2/3 growth wave that is already reshaping Indian retail investing.

#### Risks worth naming before a judge asks about them
| Risk | Mitigation |
| :--- | :--- |
| **AI gives wrong or overconfident advice** | Grounding via RAG on real data, explicit "I'm not certain" fallback, human handoff for high-stakes decisions. |
| **Misclassified as unregistered investment advice** | Position as "guidance and information," route regulated decisions to a licensed adviser/distributor flow. |
| **Data privacy / consent misuse** | Strict adherence to AA consent artefacts; no data use beyond the stated purpose and duration. |
| **Avatar feels gimmicky rather than useful** | Keep the avatar secondary to substance — specific, correct numbers matter far more than visual polish. |
| **Low trust/adoption among older or first-time users** | Voice-first, regional-language option; always-available human escalation path. |

#### Metrics that matter, post-launch
Weekly active conversations · SIP starts / top-ups influenced · Recommendation acceptance rate · Human escalation rate · Customer trust score (NPS) · AUM growth per active user

---

### Section 13 — Pitch Deck Cheat Sheet

Nine slides. Spend most of your stage time on the live demo, not the slides.

| # | Slide | What goes on it |
| :--- | :--- | :--- |
| 1 | **Title** | ARTHA AI, one-line pitch, team name, Track 01 badge. |
| 2 | **The Problem** | Fragmented advisory + scale of India's new retail investor wave (use the numbers from Section 1). |
| 3 | **The Solution** | One sentence + the three-pillar framing from Section 2. |
| 4 | **Live Demo** | Run the Section 11 script live. This is the slide that wins or loses the room. |
| 5 | **Architecture** | The five-layer diagram from Section 5 — shows engineering seriousness fast. |
| 6 | **Why It's Trustworthy** | Account Aggregator + explainability + human handoff, in three short bullets. |
| 7 | **Why It's Different** | Bank-native, not another app; compliance-aware by design. |
| 8 | **Roadmap** | The three-phase path from Section 10 — shows this isn't a one-off demo. |
| 9 | **Ask / Close** | What you need to pilot this for real (data access, a design partner branch, etc.) and the one-line pitch again. |

#### Closing line that tends to land well
> "We didn't build another investing app. We built the advisor your bank's mobile app was missing — one that already knows you."

#### Quick glossary
AA = Account Aggregator · FIP = Financial Information Provider · FIU = Financial Information User · RAG = Retrieval-Augmented Generation · SIP = Systematic Investment Plan · TTS/STT = Text-to-Speech / Speech-to-Text · DPDP Act = Digital Personal Data Protection Act, 2023 · KYC = Know Your Customer.

---
---

## PART B: THE BUILD GUIDE

> [!NOTE]
> **Implementation Status:** The Phase 2 MVP Backend and Frontend systems have been fully implemented, integrated, and verified via the expanded test suite in [test_services.py](file:///d:/IDBI/artha_backend/tests/test_services.py) on July 2, 2026. All mock-heavy facades have been upgraded to dynamic, asynchronous services (advisory engine, behavior engine, RAG knowledge retrieval, safety guardrails, and viseme voice generator).

Everything in Part A told you what to build and why. This part tells you exactly how — in the order you'll actually do it.

### Section 14 — Environment & Repo Setup

Before a single feature gets built, get the skeleton right. A clean monorepo layout means every later section in this guide has an obvious place to live — no refactoring detours mid-build.

#### Day-zero checklist
- [x] Node.js 20 LTS and Python 3.11+ installed, plus pnpm (or yarn) and a Python venv tool
- [x] PostgreSQL 15+ and Redis running locally (or via Docker Compose — recommended, see below)
- [x] An Anthropic API key (or your chosen LLM provider) and a cloud TTS/STT key stored in a secrets manager, never committed
- [x] Git repo initialised with a `.gitignore` covering `node_modules`, `.env`, `__pycache__`, and build output
- [x] A shared design-tokens file (colours, spacing, type scale) so the mobile UI and any web demo screen stay visually consistent

#### Recommended monorepo layout
```text
artha-ai/
├── apps/
│   ├── mobile/                 # React Native screen, embeddable module
│   └── demo-shell/             # Thin host app for hackathon demo only
├── services/
│   ├── gateway/                # API gateway + auth
│   ├── orchestrator/           # Conversation orchestrator
│   ├── advisory-engine/        # Rules + scoring
│   ├── ai-core/                # LLM + RAG wrapper
│   └── avatar-voice/           # TTS/STT + avatar driver
├── packages/
│   ├── shared-types/           # TypeScript types shared across services
│   └── design-tokens/          # Colours, spacing, fonts
├── data/
│   ├── seed/                   # Mock AA-style JSON payloads
│   └── migrations/             # SQL migration files
├── infra/
│   └── docker-compose.yml      # Postgres, Redis, and all services
└── docs/
    └── api-contracts.md        # Single source of truth for request/response shapes
```

#### One command to bring the whole stack up
A single `docker-compose.yml` at the root is worth the half-day it takes to set up — it's the difference between "works on my machine" and a demo laptop that boots cleanly five minutes before judging.

```yaml
# infra/docker-compose.yml (essentials)
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: artha
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7
    ports: ["6379:6379"]

  gateway:
    build: ./services/gateway
    ports: ["4000:4000"]
    depends_on: [postgres, redis]

  orchestrator:
    build: ./services/orchestrator
    depends_on: [postgres, redis, gateway]

volumes:
  pgdata:
```

> **Avoid this mistake:** teams that build each microservice in isolation often discover, the night before demo day, that two services disagree on a field name (`accountId` vs `account_id`). Fix this on day zero by writing `docs/api-contracts.md` first and treating it as the one file every teammate checks before changing a payload shape.

---

### Section 15 — Designing the Mock Data Layer

The single highest-leverage engineering decision in this whole build: model your mock data exactly like real Account Aggregator payloads. It costs nothing extra now and means the eventual swap to a live AA sandbox is a data-source change, not a rewrite.

#### Core entities you need
| Entity | Key fields | Why it matters to the demo |
| :--- | :--- | :--- |
| **Customer** | `customerId`, `name`, `language`, `riskProfile`, `onboardedAt` | Drives persona-specific tone and language defaults |
| **Account** | `accountId`, `fipId`, `type` (SAVINGS/FD/MF/LOAN), `balance`, `linkedAt` | Powers the 360° view claim — needs multiple FIPs, not just one bank |
| **Transaction** | `txnId`, `accountId`, `amount`, `category`, `narration`, `date` | Feeds the behavioural analytics layer |
| **SIP / Goal** | `goalId`, `name`, `targetAmount`, `targetDate`, `linkedSipAmount` | Gives recommendations something concrete to reference |
| **ConsentArtefact** | `consentId`, `scope`, `purpose`, `expiresAt` | Lets you demo the AA consent story even with mock data |

#### Sample seed record
```json
{
  "customerId": "cust_riya_001",
  "accounts": [
    {
      "accountId": "acc_fd_882",
      "fipId": "HDFC-FIP",
      "type": "FD",
      "balance": 150000,
      "interestRate": 6.1,
      "openedAt": "2025-04-12",
      "lastTouchedAt": "2025-04-12"
    },
    {
      "accountId": "acc_mf_119",
      "fipId": "ZERODHA-FIP",
      "type": "MF_SIP",
      "fundName": "Hybrid Equity Fund",
      "sipAmount": 5000,
      "linkedGoalId": "goal_car_2027"
    }
  ],
  "goals": [
    { "goalId": "goal_car_2027", "name": "First Car", "targetDate": "2027-06-01" }
  ],
  "consent": {
    "consentId": "consent_001",
    "scope": ["BALANCE", "TRANSACTIONS", "SUMMARY"],
    "purpose": "Personalised wealth advisory",
    "expiresAt": "2026-12-31"
  }
}
```

#### Build three to five realistic months of transactions, not random noise
A small Python or Node script that generates transactions with believable category clustering (rent on the 1st, salary credit on the last working day, weekday lunch spends, an occasional irregular expense) will make the spending-insight feature feel real instead of obviously synthetic. Spend an hour here — it pays off every time you run the demo.

1.  **Write a generator script** — One function per category (rent, groceries, dining, salary) that emits transactions with realistic timing and small randomised variance — not a single flat amount repeated every month.
2.  **Seed Postgres directly from JSON fixtures** — Keep raw fixtures in `data/seed/*.json` and a `seed.ts` or `seed.py` script that loads them — never hand-type rows into the database during a demo rehearsal.
3.  **Add one deliberate anomaly** — A spending spike, a goal at risk, an FD nearing maturity — something for the AI engine to actually notice and explain. A flat, uneventful dataset produces a boring demo no matter how good the prompt is.

---

### Section 16 — Building the Backend Skeleton

This is the spine everything else attaches to: a gateway for auth, an orchestrator that holds conversation state, and a contract every other service agrees on.

#### The API contract — lock this before writing service code
| Endpoint | Method | Purpose |
| :--- | :--- | :--- |
| `/v1/session/start` | POST | Exchanges the bank app's existing auth token for an ARTHA session; returns customer context summary |
| `/v1/conversation/message` | POST | Sends one user turn (text or transcribed voice), returns the avatar's reply + any recommendation payload |
| `/v1/conversation/history` | GET | Returns prior turns for the session, used to rehydrate the chat UI on reopen |
| `/v1/recommendations/:id/feedback` | POST | Logs accept / dismiss / "talk to RM" on a recommendation — this is your audit trail |
| `/v1/voice/synthesize` | POST | Text in, audio stream out (used by the avatar service) |

#### Conversation orchestrator — the core loop
Keep this service deliberately simple: it does not call the LLM provider directly. It assembles context, calls the AI core service, and persists the turn. This separation means you can swap LLM providers later by touching one service only.

```typescript
// services/orchestrator/src/handleMessage.ts
export async function handleMessage(sessionId: string, userText: string) {
  const session = await getSession(sessionId);
  const customerContext = await getCustomerContext(session.customerId);
  const history = await getRecentTurns(sessionId, 8);

  // 1. behavioural signals are computed separately, never invented by the LLM
  const signals = await behaviouralEngine.getSignals(session.customerId);

  // 2. advisory engine returns ranked, reason-coded recommendations
  const recs = await advisoryEngine.getRecommendations(session.customerId, signals);

  // 3. AI core turns all of that into a natural-language reply
  const reply = await aiCore.generateReply({
    userText, customerContext, signals, recs, history, language: session.language
  });

  await persistTurn(sessionId, userText, reply);
  return reply;
}
```

#### Why this ordering matters
*   **Behavioural signals and recommendations are computed by deterministic code before the LLM is called** — the model phrases facts, it doesn't generate them. This is the single most important architectural decision for both demo reliability and compliance credibility.
*   **Conversation history is capped** (8 turns above) to keep latency predictable; summarise older turns into a short context string rather than sending unbounded history to the LLM.
*   **Every recommendation returned carries a `reasonCode`** and the specific data points behind it, so "why are you suggesting this?" always has a real, traceable answer.

#### Session & auth
Reuse the bank's existing session rather than building a parallel login. In production this is an OAuth token exchange; for the hackathon demo, a signed JWT minted by your demo-shell app with the customer ID embedded is a reasonable, honest stand-in — say so explicitly in your pitch rather than implying it's the real bank integration.

---

### Section 17 — Wiring Up the AI Engine

Three pieces working together: a small rules-plus-scoring engine for recommendations, a thin RAG layer for grounding, and a tightly-written system prompt that keeps the LLM in its lane.

#### Step 1 — behavioural signals (plain code, not the LLM)
```python
# services/advisory-engine/signals.py
def compute_signals(transactions, accounts):
    savings_rate = (income(transactions) - spend(transactions)) / income(transactions)
    dormant_funds = [a for a in accounts
                     if a.type == "FD" and months_since(a.lastTouchedAt) > 12]
    category_deltas = compare_to_trailing_avg(transactions, months=3)
    return {
        "savingsRate": savings_rate,
        "dormantFunds": dormant_funds,
        "categoryDeltas": category_deltas,
    }
```

#### Step 2 — reason-coded recommendation rules
Each rule is a small, readable function that either fires or doesn't — resist the temptation to let the LLM "decide" whether to recommend something. The rule decides; the LLM explains.

```python
# services/advisory-engine/rules.py
def rule_dormant_fd_to_hybrid(signals, goals, risk_profile):
    for fd in signals["dormantFunds"]:
        matching_goal = find_goal_within_years(goals, years=3)
        if matching_goal and risk_profile in ("moderate", "growth"):
            return {
                "reasonCode": "DORMANT_FD_REALLOCATION",
                "facts": {
                    "account": fd.accountId, "rate": fd.interestRate,
                    "monthsDormant": months_since(fd.lastTouchedAt),
                    "goal": matching_goal.name,
                },
            }
    return None
```

#### Step 3 — RAG layer for grounded conversation
Keep the knowledge base small and specific for the demo: the bank's product catalogue (fund names, rates, fees), a short FAQ, and relevant regulatory disclosure lines. pgvector on the same Postgres instance is enough — don't add a separate vector database for a hackathon timeline.

```python
# services/ai-core/retrieve.py
def retrieve_context(query, customer_facts, top_k=4):
    query_embedding = embed(query)
    product_chunks = vector_search(query_embedding, table="product_kb", k=top_k)
    return {
        "productFacts": product_chunks,
        "customerFacts": customer_facts,   # structured, not retrieved
    }
```

#### Step 4 — the system prompt that keeps Artha in character and grounded
```text
You are Artha, a wealth advisory voice inside a bank's mobile app.

RULES YOU MUST FOLLOW:
- Only state numbers that appear in CUSTOMER_FACTS or PRODUCT_FACTS below.
  Never estimate, round dramatically, or invent a figure.
- If asked something you cannot answer from the provided facts, say so
  plainly and offer to connect a human advisor. Never guess.
- You give guidance and information, not regulated investment advice.
  For decisions that need a licensed adviser, say so and offer the
  human handoff.
- Keep responses to 2-3 short sentences unless the user asks for detail.
- Mirror the user's language; switch fluidly if they code-switch.
- Tone: calm, precise, warm. Never use fear to push a product.

CUSTOMER_FACTS: {{customerContext}}
RELEVANT_RECOMMENDATION: {{recommendation}}
PRODUCT_FACTS: {{productFacts}}
CONVERSATION_HISTORY: {{history}}
```

> **Test this explicitly:** ask the demo build a question with no good answer in your mock dataset (e.g. a fund that doesn't exist). If it ever invents a confident-sounding number instead of saying "I don't have that information," tighten the prompt and lower the temperature before moving on — this is the failure mode judges probe for first.

---

### Section 18 — Building the Avatar & Voice Layer

The avatar is the layer judges remember emotionally — but it should be the simplest, most reliable piece of engineering in the stack. A 2D animated avatar with well-timed audio reads as more "finished" live than an ambitious 3D pipeline that stutters under demo Wi-Fi.

#### The flow, end to end
1.  **Text reply arrives from the orchestrator** — The avatar service receives the final reply text plus the target language code.
2.  **Send to neural TTS** — Use a cloud TTS engine with good Indian-language voices; request word/phoneme timing data alongside the audio if the engine supports it.
3.  **Drive the avatar from timing data, not guesswork** — Map amplitude or phoneme timestamps onto a small set of pre-built mouth-shape frames (Lottie or Rive supports this well) so lip movement looks intentional rather than randomly bobbing.
4.  **Stream audio + animation cues to the mobile client together** — Send a single payload with the audio URL and a timed cue array, so the client UI doesn't need to do its own lip-sync math.

#### Minimal avatar service response shape
```json
{
  "audioUrl": "https://.../reply_8841.mp3",
  "durationMs": 4200,
  "visemeCues": [
    { "atMs": 0,    "shape": "closed" },
    { "atMs": 180,  "shape": "open_wide" },
    { "atMs": 420,  "shape": "narrow" }
  ],
  "language": "hi-IN"
}
```

#### Multilingual code-switch — the moment that lands best live
Detect the input language per turn (most STT engines return a confidence-scored language guess; a lightweight language-ID model on the text transcript is a reliable fallback) and pass that language code straight through to both the LLM prompt and the TTS voice selection. Don't make the user manually switch a language toggle — the demo is far more impressive when Artha follows the customer's lead automatically, mid-conversation.

| Need | Hackathon-speed choice | Notes |
| :--- | :--- | :--- |
| **Speech-to-text** | Open-source Whisper (small/medium model) | Runs locally, no per-call cost, good Hindi support |
| **Text-to-speech** | Cloud neural TTS with Indian-language voices | Request phoneme/word timing in the same call where supported |
| **Avatar rendering** | Lottie or Rive 2D animation, mouth-shape state machine | Pre-build 5–6 mouth shapes; map visemes onto the closest shape |
| **Idle/listening states** | A subtle breathing-loop animation and a "listening" pulse | Small detail, large effect on the avatar feeling alive between turns |

> **Rehearse with the real device and real Wi-Fi.** TTS latency over a flaky venue network is the most common live-demo failure point. Pre-generate and cache the audio for your rehearsed demo script lines so the live version always plays instantly, while keeping live synthesis working for any improvised question.

---

### Section 19 — Building the Mobile Screen

The single biggest visual tell of a rushed hackathon project is a chat screen that looks like a generic chatbot template. The fix isn't more features — it's matching the bank's existing visual language closely enough that the screen feels native.

#### Screen structure
```text
apps/mobile/src/screens/ArthaScreen/
├── ArthaScreen.tsx          # top-level screen, owns session state
├── AvatarStage.tsx          # avatar render area + idle/talking states
├── ConversationList.tsx     # scrollable turn history
├── MessageBubble.tsx        # text bubble, mirrors bank's existing chat style
├── RecommendationCard.tsx   # inline card for "why" expansion
├── InputBar.tsx             # text input + mic button + language indicator
└── useArthaSession.ts       # hook: session, send message, voice playback
```

#### Make it look embedded, not standalone
- [x] Reuse the bank's existing colour palette and type scale instead of introducing a new brand identity — pull both from a design-tokens package shared across the monorepo
- [x] Keep the existing app's top navigation bar and back button behaviour; ARTHA should feel like a screen inside the app, not a separate experience that was dropped in
- [x] Match the existing app's loading and error states (skeleton loaders, toast style) rather than inventing new ones just for this screen
- [x] If the bank app has a bottom tab bar, keep it visible — don't take over the full screen unless the rest of the app does too

#### A "why" card that earns trust
When a recommendation includes a `reasonCode`, render an expandable card beneath the avatar's message rather than burying the reasoning in plain text. This single UI pattern is what makes "explainability" visible to a judge glancing at the screen, not just something you say in the pitch.

```tsx
// RecommendationCard.tsx (essentials)
function RecommendationCard({ rec }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <Pressable onPress={() => setExpanded(!expanded)}>
      <Text>Why am I seeing this? {expanded ? '▲' : '▼'}</Text>
      {expanded && (
        <View>
          {rec.facts.map(f => <Text key={f.label}>{f.label}: {f.value}</Text>)}
        </View>
      )}
    </Pressable>
  );
}
```

#### Mic input & the language indicator
Show a small, unobtrusive language chip (e.g. "EN" or "HI") near the input bar that updates automatically as the conversation code-switches. It's a tiny UI element that visibly demonstrates the multilingual feature without needing the presenter to explain it.

---

### Section 20 — Connecting Every Layer End-to-End

Once each service works in isolation, trace one full request through the whole system before building anything else. This is the moment a pile of services becomes a product.

#### The full request lifecycle, traced
1.  **Customer taps the mic and speaks** — Mobile client streams audio to the gateway, which forwards it to the avatar-voice service for STT.
2.  **Transcript reaches the orchestrator** — Gateway validates the session token, then calls `/v1/conversation/message` on the orchestrator with the transcribed text.
3.  **Orchestrator gathers context** — Pulls customer context, behavioural signals, and ranked recommendations from the advisory engine — all before touching the LLM.
4.  **AI core composes the reply** — RAG retrieval grounds the response in product facts; the system prompt constrains tone and factual boundaries; the LLM returns natural-language text.
5.  **Avatar-voice service synthesises speech + visemes** — Text goes to TTS; timing data drives the avatar's mouth shapes; both are packaged into one response payload.
6.  **Mobile client renders and plays** — Text bubble appears, avatar animates in sync with audio, and any recommendation renders as an expandable "why" card.

**Every step gets logged** — Orchestrator writes the turn, the signals used, and the recommendation reason code to the audit log — this is what Section 8's compliance story actually looks like in code.

#### A practical integration test worth writing
Before any UI polish, write one automated test that POSTs a known transcript ("how am I doing this month?") through the orchestrator and asserts the reply contains the expected reason code and references the correct mock account. This single test will save hours of manual re-testing every time someone touches a prompt or a rule.

```typescript
// services/orchestrator/test/e2e.test.ts
test('dormant FD recommendation surfaces with correct reason code', async () => {
  const res = await request(app)
    .post('/v1/conversation/message')
    .send({ sessionId: 'demo_riya', text: 'how am I doing this month?' });

  expect(res.body.recommendations[0].reasonCode)
    .toBe('DORMANT_FD_REALLOCATION');
});
```

---

### Section 21 — Testing & Hardening the Demo

A demo doesn't need to handle every possible input — it needs to never break visibly on stage. These are the failure modes worth testing for on purpose.

#### Edge cases to deliberately trigger before judging
| Scenario | What "graceful" looks like |
| :--- | :--- |
| **Question with no answer in mock data** | Artha says plainly it doesn't have that information and offers the human-advisor handoff — never a confident-sounding guess |
| **Mic input that STT mis-transcribes** | A low-confidence transcript triggers a quick clarifying question rather than the system silently acting on a garbled transcript |
| **Network hiccup mid-TTS** | UI shows the text reply immediately and a small "voice loading" indicator, instead of a frozen screen |
| **User asks for explicit investment advice ("just tell me what to buy")** | Artha reframes as guidance and offers the RM handoff — this is a great moment to rehearse, since judges often ask it directly |
| **Rapid back-to-back messages** | Orchestrator queues turns per session so replies never arrive out of order |

#### Pre-demo QA checklist
- [x] Run the full rehearsed demo script (Section 11) three times back-to-back with no restarts, on the exact device you'll present with
- [x] Time the full run — know exactly how long it takes and where you can trim if a judge interrupts with a question
- [x] Test on the venue's actual Wi-Fi if at all possible, or have a mobile hotspot as a tested fallback
- [x] Pre-warm any cold-start services (serverless functions, model loading) a few minutes before your slot
- [x] Have a short, silent fallback path (pre-recorded screen capture) ready in case live demo truly fails — never let a crash be the last thing judges see
- [x] Confirm the mic permission prompt has already been granted on the demo device before you're on stage

#### Logging that helps you debug live, not just after
During rehearsals, keep a visible (to your team, not the audience) debug overlay showing the last reason code fired and the latency of the last LLM call. It turns "something feels off" into "the RAG retrieval is returning the wrong product chunk" in seconds, which matters a great deal in the anxious minutes before you're called up.

> Decide your fallback story for "is this SEBI-registered advice?" now, not on stage. The answer rehearsed in Section 8 — *guidance and information, with regulated decisions routed to a licensed human* — should come out smoothly and immediately when asked, because it will be asked.

---

### Appendix: File & Folder Quick Reference

| Path | Purpose |
| :--- | :--- |
| `apps/mobile/src/screens/ArthaScreen/` | React Native screen components |
| `services/gateway/` | API gateway + auth |
| `services/orchestrator/` | Conversation state machine |
| `services/advisory-engine/` | Behavioural signals + rules |
| `services/ai-core/` | LLM + RAG wrapper |
| `services/avatar-voice/` | TTS/STT + avatar driver |
| `data/seed/*.json` | Mock AA-style fixtures |
| `infra/docker-compose.yml` | One-command local stack |
| `docs/api-contracts.md` | Source of truth for all payloads |
