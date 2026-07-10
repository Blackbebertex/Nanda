"""Quick-path orchestrator — delegates to ChatAgent (Gemini)."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from agents.registry import get_agent


async def generate_response_async(
  user_text: str,
  customer_context: Dict[str, Any],
  signals: Dict[str, Any],
  recommendation: Dict[str, Any],
  history: List[Dict[str, str]],
  language: str = "en",
) -> Tuple[str, List[str]]:
  chat = get_agent("chat")
  return await chat.run(
    user_text=user_text,
    customer_context=customer_context,
    signals=signals,
    recommendation=recommendation,
    history=history,
    language=language,
    customer_id=customer_context.get("customerId"),
  )


def generate_response(intent):
  return "Here is your wealth guidance."
