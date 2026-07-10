"""Research Agent — product and market fact retrieval augmented by Gemini."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent
from agents.rag_knowledge_base import retrieve_facts
from services.prompt_registry import render_prompt


class ResearchAgent(BaseAgent):
  name = "research"
  description = "Research banking products and financial facts via Gemini + knowledge base"

  async def run(
    self,
    *,
    query: str,
    customer_id: Optional[str] = None,
  ) -> Dict[str, Any]:
    facts = retrieve_facts(query)
    if not self.gemini.is_configured:
      return {"facts": facts, "summary": " ".join(facts[:3]) if facts else "No facts found."}

    system = render_prompt("research_system")
    user = f"Query: {query}\n\nKnowledge base facts:\n" + "\n".join(f"- {f}" for f in facts)
    text = await self.call_gemini(user, system=system, customer_id=customer_id, use_memory=False)
    return {"facts": facts, "summary": text}
