"""Coding Agent — structured JSON/code generation for chain steps."""
from __future__ import annotations

from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from agents.wealth_chain.prompt_loader import render_prompt as render_chain_prompt


class CodingAgent(BaseAgent):
  name = "coding"
  description = "Structured JSON output generation for multi-step workflows via Gemini"

  async def run(
    self,
    *,
    step_file: str,
    context: Dict[str, str],
    step_index: int,
    customer_id: Optional[str] = None,
    user_instruction: Optional[str] = None,
  ) -> Dict[str, Any]:
    system = render_chain_prompt(step_file, **context)
    from services.gemini_service import GeminiMessage
    instruction = user_instruction or f"Produce Step {step_index} JSON. Return valid JSON only."
    return await self.gemini.generate_json(
      system=system,
      messages=[GeminiMessage(role="user", content=instruction)],
      temperature=0.1,
      telemetry_path=f"coding_step_{step_index}",
      customer_id=customer_id,
    )
