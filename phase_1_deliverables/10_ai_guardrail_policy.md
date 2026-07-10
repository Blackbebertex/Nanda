# AI Guardrail Policy & Execution Strategy

This document outlines the security, safety, and compliance guardrails active within the ARTHA AI conversational engine to enforce SEBI compliance and protect user data under the DPDP Act 2023.

## 1. Input Shield (Adversarial Prompt & Jailbreak Defense)
All incoming user messages pass through a text parser checking for known malicious patterns before the LLM orchestration layer is invoked.
- **Detections:**
  - Instructions override phrases (e.g. `ignore all previous instructions`, `override rules`).
  - System prompt extraction requests (e.g. `reveal system prompt`, `system settings`).
  - Jailbreak indicators (e.g. `jailbreak`).
- **Mitigation:** If flagged, execution is aborted, and a standardized fallback response is returned: *"I'm sorry, I cannot process that request. Let's keep our conversation focused on personal finance."*

## 2. Output Shield (SEBI Compliance Enforcement)
All generated language outputs are parsed for prohibited regulatory assertions prior to rendering in the client.
- **Detections:**
  - Claims of guaranteed capital safety or returns (e.g. `guarantee`, `guaranteed profit`, `assured returns`, `zero risk`).
- **Mitigation:** If flagged, the output is blocked and replaced by a compliant template: *"I cannot recommend products with guaranteed returns. Let me focus on explaining historical performances and risk parameters."*

## 3. PII Masking Policy (Data Privacy)
- User identifiers, account numbers, and exact contact details are masked within conversation histories prior to sending payloads to public LLM endpoints, replacing them with generic tags (e.g., `[Account_A]`).
