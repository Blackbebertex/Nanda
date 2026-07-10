"""Base agent — all agents use Gemini through the shared service."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional

from services.gemini_service import GeminiMessage, GeminiService, get_gemini_service


class BaseAgent(ABC):
  """Abstract base for all ARTHA AI agents."""

  name: str = "base"
  description: str = ""

  def __init__(self, gemini: Optional[GeminiService] = None):
    self.gemini = gemini or get_gemini_service()
    self._memory: List[GeminiMessage] = []

  def clear_memory(self) -> None:
    self._memory.clear()

  def add_to_memory(self, role: str, content: str) -> None:
    self._memory.append(GeminiMessage(role=role, content=content))
    if len(self._memory) > 20:
      self._memory = self._memory[-20:]

  def get_memory(self) -> List[GeminiMessage]:
    return list(self._memory)

  async def call_gemini(
    self,
    user_prompt: str,
    *,
    system: Optional[str] = None,
    json_mode: bool = False,
    temperature: float = 0.2,
    max_output_tokens: int = 2048,
    customer_id: Optional[str] = None,
    use_memory: bool = True,
  ) -> str:
    messages = list(self._memory) if use_memory else []
    messages.append(GeminiMessage(role="user", content=user_prompt))
    if json_mode:
      result = await self.gemini.generate_json(
        system=system,
        messages=messages,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        telemetry_path=f"agent_{self.name}",
        customer_id=customer_id,
      )
      import json
      text = json.dumps(result)
      if use_memory:
        self.add_to_memory("user", user_prompt)
        self.add_to_memory("model", text)
      return text
    response = await self.gemini.generate(
      system=system,
      messages=messages,
      temperature=temperature,
      max_output_tokens=max_output_tokens,
      telemetry_path=f"agent_{self.name}",
      customer_id=customer_id,
    )
    if use_memory:
      self.add_to_memory("user", user_prompt)
      self.add_to_memory("model", response.text)
    return response.text

  async def stream_gemini(
    self,
    user_prompt: str,
    *,
    system: Optional[str] = None,
    temperature: float = 0.2,
    customer_id: Optional[str] = None,
  ) -> AsyncIterator[str]:
    messages = list(self._memory)
    messages.append(GeminiMessage(role="user", content=user_prompt))
    full = ""
    async for chunk in self.gemini.stream(
      system=system,
      messages=messages,
      temperature=temperature,
      telemetry_path=f"agent_{self.name}_stream",
      customer_id=customer_id,
    ):
      full += chunk
      yield chunk
    self.add_to_memory("user", user_prompt)
    self.add_to_memory("model", full)

  @abstractmethod
  async def run(self, **kwargs: Any) -> Any:
    ...
