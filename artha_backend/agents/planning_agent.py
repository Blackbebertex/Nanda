"""Planning Agent — goal architecture and wealth plan design."""
from __future__ import annotations

from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from agents.wealth_chain.prompt_loader import render_prompt as render_chain_prompt


class PlanningAgent(BaseAgent):
  name = "planning"
  description = "Goal architecture and financial planning via Gemini"

  async def run(
    self,
    *,
    step_file: str,
    context: Dict[str, str],
    customer_id: Optional[str] = None,
    user_instruction: str = "Produce the required JSON output.",
    step_index: Optional[int] = None,
  ) -> Dict[str, Any]:
    system = render_chain_prompt(step_file, **context)
    from services.gemini_service import GeminiMessage
    return await self.gemini.generate_json(
      system=system,
      messages=[GeminiMessage(role="user", content=user_instruction)],
      temperature=0.1,
      telemetry_path=f"planning_{step_file}",
      customer_id=customer_id,
    )
