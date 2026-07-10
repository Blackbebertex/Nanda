"""Task Execution Agent — recommendation and execution intent narration via Gemini."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from services.prompt_registry import render_prompt


class TaskExecutionAgent(BaseAgent):
  name = "task_execution"
  description = "Executes and explains advisory recommendations via Gemini"

  async def run(
    self,
    *,
    recommendation: Dict[str, Any],
    customer_context: Dict[str, Any],
    action: str = "explain",
    customer_id: Optional[str] = None,
  ) -> str:
    if not self.gemini.is_configured:
      code = recommendation.get("reasonCode", "ADVISORY")
      return f"Recommendation ({code}): {recommendation.get('action', 'review your portfolio')}."

    system = render_prompt("task_execution_system")
    user = json.dumps({
      "action": action,
      "recommendation": recommendation,
      "risk_profile": customer_context.get("riskProfile"),
    }, indent=2)
    return await self.call_gemini(user, system=system, customer_id=customer_id, use_memory=False)
