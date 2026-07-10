"""Document Agent — avatar scripts and customer-facing summaries."""
from __future__ import annotations

from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from agents.wealth_chain.prompt_loader import render_prompt as render_chain_prompt


class DocumentAgent(BaseAgent):
  name = "document"
  description = "Customer-facing narrative and avatar script generation via Gemini"

  async def run(
    self,
    *,
    step_file: str,
    context: Dict[str, str],
    customer_id: Optional[str] = None,
    user_instruction: str = "Produce Step 6 avatar script JSON.",
    step_index: Optional[int] = None,
  ) -> Dict[str, Any]:
    system = render_chain_prompt(step_file, **context)
    from services.gemini_service import GeminiMessage
    return await self.gemini.generate_json(
      system=system,
      messages=[GeminiMessage(role="user", content=user_instruction)],
      temperature=0.3,
      telemetry_path="document_avatar",
      customer_id=customer_id,
    )
