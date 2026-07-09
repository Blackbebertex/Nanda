"""Analysis Agent — wealth analyst and behavioural signal interpretation."""
from __future__ import annotations

from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from agents.wealth_chain.prompt_loader import render_prompt as render_chain_prompt


class AnalysisAgent(BaseAgent):
  name = "analysis"
  description = "Customer financial analysis and risk assessment via Gemini"

  async def run(
    self,
    *,
    step_file: str,
    context: Dict[str, str],
    customer_id: Optional[str] = None,
    user_instruction: str = "Produce Step 1 JSON analysis.",
    step_index: Optional[int] = None,
  ) -> Dict[str, Any]:
    system = render_chain_prompt(step_file, **context)
    from services.gemini_service import GeminiMessage
    return await self.gemini.generate_json(
      system=system,
      messages=[GeminiMessage(role="user", content=user_instruction)],
      temperature=0.1,
      telemetry_path="analysis_step",
      customer_id=customer_id,
    )
