"""Chat Agent — quick-path conversational responses via Gemini."""
from __future__ import annotations

import json
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple

from agents.base_agent import BaseAgent
from agents.compliance_guardrails import check_safety
from agents.pii_masker import format_customer_facts_masked, mask_text_for_llm
from agents.rag_knowledge_base import retrieve_facts
from services.prompt_registry import render_prompt


class ChatAgent(BaseAgent):
  name = "chat"
  description = "Conversational wealth advisor for quick customer queries"

  async def run(
    self,
    *,
    user_text: str,
    customer_context: Dict[str, Any],
    signals: Dict[str, Any],
    recommendation: Dict[str, Any],
    history: List[Dict[str, str]],
    language: str = "en",
    customer_id: Optional[str] = None,
  ) -> Tuple[str, List[str]]:
    if not check_safety(user_text):
      return "I'm sorry, I cannot process that request. Let's keep our conversation focused on personal finance.", []

    if not self.gemini.is_configured:
      return await self._fallback(user_text, customer_context, signals, recommendation, language)

    try:
      customer_facts = format_customer_facts_masked(customer_context, signals)
      rag_facts = retrieve_facts(user_text)
      masked_history = "\n".join(
        f"User: {mask_text_for_llm(t.get('user', ''))}\nArtha: {mask_text_for_llm(t.get('bot', ''))}"
        for t in history[-6:]
      )

      system = render_prompt(
        "chat_system",
        CUSTOMER_FACTS=customer_facts,
        PRODUCT_FACTS="\n".join(f"- {f}" for f in rag_facts),
        RECOMMENDATION_ACTION=recommendation.get("action", "None"),
        RECOMMENDATION_CODE=recommendation.get("reasonCode", "None"),
        RECOMMENDATION_FACTS=json.dumps(recommendation.get("facts", {})),
        CONVERSATION_HISTORY=masked_history or "(none)",
      )

      self.clear_memory()
      for turn in history[-4:]:
        self.add_to_memory("user", mask_text_for_llm(turn.get("user", "")))
        self.add_to_memory("model", mask_text_for_llm(turn.get("bot", "")))

      reply = await self.call_gemini(
        mask_text_for_llm(user_text),
        system=system,
        temperature=0.2,
        max_output_tokens=512,
        customer_id=customer_id,
        use_memory=True,
      )

      if not check_safety(reply):
        reply = "I cannot recommend products with guaranteed returns. Let me focus on explaining historical performances and risk parameters."

      rec_ids = [recommendation["recommendation_id"]] if recommendation.get("recommendation_id") else []
      return reply, rec_ids
    except Exception:
      return await self._fallback(user_text, customer_context, signals, recommendation, language)

  async def stream(
    self,
    *,
    user_text: str,
    customer_context: Dict[str, Any],
    signals: Dict[str, Any],
    recommendation: Dict[str, Any],
    history: List[Dict[str, str]],
    customer_id: Optional[str] = None,
  ) -> AsyncIterator[str]:
    if not self.gemini.is_configured:
      reply, _ = await self._fallback(user_text, customer_context, signals, recommendation, "en")
      yield reply
      return

    customer_facts = format_customer_facts_masked(customer_context, signals)
    rag_facts = retrieve_facts(user_text)
    system = render_prompt(
      "chat_system",
      CUSTOMER_FACTS=customer_facts,
      PRODUCT_FACTS="\n".join(f"- {f}" for f in rag_facts),
      RECOMMENDATION_ACTION=recommendation.get("action", "None"),
      RECOMMENDATION_CODE=recommendation.get("reasonCode", "None"),
      RECOMMENDATION_FACTS=json.dumps(recommendation.get("facts", {})),
      CONVERSATION_HISTORY="",
    )
    self.clear_memory()
    async for chunk in self.stream_gemini(
      mask_text_for_llm(user_text),
      system=system,
      customer_id=customer_id,
    ):
      yield chunk

  async def _fallback(
    self,
    user_text: str,
    customer_context: Dict[str, Any],
    signals: Dict[str, Any],
    recommendation: Dict[str, Any],
    language: str,
  ) -> Tuple[str, List[str]]:
    from agents.fallback_responses import keyword_reply
    return keyword_reply(user_text, customer_context, signals, recommendation, language)
