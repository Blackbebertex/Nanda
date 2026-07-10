"""
Central Google Gemini client — sole LLM integration for all agents.
Reads GEMINI_API_KEY from environment only. Never logs secrets.
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Dict, List, Optional

import httpx

from agents.llm_telemetry import record_llm_event
from services.config import get_settings

logger = logging.getLogger("artha.gemini")

GEMINI_BASE_V1BETA = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_BASE_V1 = "https://generativelanguage.googleapis.com/v1"
MODEL_FALLBACKS = [
  "gemini-2.0-flash",
  "gemini-2.0-flash-lite",
  "gemini-1.5-flash",
  "gemini-1.5-flash-8b",
  "gemini-pro",
]


@dataclass
class GeminiMessage:
  role: str  # "user" | "model"
  content: str


@dataclass
class GeminiResponse:
  text: str
  model: str
  raw: Dict[str, Any] = field(default_factory=dict)
  usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeminiToolSpec:
  name: str
  description: str
  parameters: Dict[str, Any]


class GeminiService:
  """Reusable async Gemini client with retries, streaming, and structured JSON."""

  def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
    settings = get_settings()
    self.api_key = settings.gemini_api_key if api_key is None else api_key
    self.model = model or settings.gemini_model
    self.timeout = settings.gemini_timeout_seconds
    self.max_retries = settings.gemini_max_retries

  @property
  def is_configured(self) -> bool:
    return bool(self.api_key)

  def _headers(self) -> Dict[str, str]:
    return {"Content-Type": "application/json"}

  def _url(self, action: str, model: Optional[str] = None, api_base: str = GEMINI_BASE_V1BETA) -> str:
    m = model or self.model
    return f"{api_base}/models/{m}:{action}?key={self.api_key}"

  def _build_payload(
    self,
    *,
    system: Optional[str],
    messages: List[GeminiMessage],
    temperature: float = 0.2,
    max_output_tokens: int = 2048,
    json_mode: bool = False,
    tools: Optional[List[GeminiToolSpec]] = None,
  ) -> Dict[str, Any]:
    contents = []
    for msg in messages:
      role = "model" if msg.role in ("assistant", "model") else "user"
      contents.append({"role": role, "parts": [{"text": msg.content}]})

    generation_config: Dict[str, Any] = {
      "temperature": temperature,
      "maxOutputTokens": max_output_tokens,
    }
    if json_mode:
      generation_config["responseMimeType"] = "application/json"

    payload: Dict[str, Any] = {"contents": contents, "generationConfig": generation_config}
    if system:
      payload["systemInstruction"] = {"parts": [{"text": system}]}
    if tools:
      payload["tools"] = [{
        "functionDeclarations": [
          {"name": t.name, "description": t.description, "parameters": t.parameters}
          for t in tools
        ]
      }]
    return payload

  def _extract_text(self, data: Dict[str, Any]) -> str:
    candidates = data.get("candidates") or []
    if not candidates:
      raise ValueError(data.get("error", {}).get("message", "No candidates in Gemini response"))
    parts = candidates[0].get("content", {}).get("parts") or []
    texts = [p.get("text", "") for p in parts if "text" in p]
    return "".join(texts).strip()

  def _extract_tool_calls(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates = data.get("candidates") or []
    if not candidates:
      return []
    parts = candidates[0].get("content", {}).get("parts") or []
    calls = []
    for part in parts:
      if "functionCall" in part:
        fc = part["functionCall"]
        calls.append({"name": fc.get("name"), "args": fc.get("args", {})})
    return calls

  def _should_retry(self, status: int) -> bool:
    return status in (429, 500, 502, 503, 504)

  async def generate(
    self,
    *,
    system: Optional[str] = None,
    messages: List[GeminiMessage],
    temperature: float = 0.2,
    max_output_tokens: int = 2048,
    json_mode: bool = False,
    tools: Optional[List[GeminiToolSpec]] = None,
    telemetry_path: str = "gemini",
    customer_id: Optional[str] = None,
  ) -> GeminiResponse:
    if not self.is_configured:
      raise RuntimeError("GEMINI_API_KEY is not configured")

    payload = self._build_payload(
      system=system,
      messages=messages,
      temperature=temperature,
      max_output_tokens=max_output_tokens,
      json_mode=json_mode,
      tools=tools,
    )
    last_error: Optional[str] = None
    models_to_try = [self.model] + [m for m in MODEL_FALLBACKS if m != self.model]
    bases = [GEMINI_BASE_V1BETA, GEMINI_BASE_V1]

    async with httpx.AsyncClient(timeout=self.timeout) as client:
      for model_name in models_to_try:
        for api_base in bases:
          for attempt in range(1, self.max_retries + 1):
            try:
              resp = await client.post(
                self._url("generateContent", model=model_name, api_base=api_base),
                headers=self._headers(),
                json=payload,
              )
              if resp.status_code == 404:
                last_error = f"HTTP 404 model={model_name}"
                break
              if self._should_retry(resp.status_code) and attempt < self.max_retries:
                await asyncio.sleep(min(2 ** attempt, 10))
                continue
              resp.raise_for_status()
              data = resp.json()
              text = self._extract_text(data)
              self.model = model_name
              record_llm_event(
                telemetry_path,
                success=True,
                model=model_name,
                customer_id=customer_id,
              )
              return GeminiResponse(
                text=text,
                model=model_name,
                raw=data,
                usage=data.get("usageMetadata", {}),
              )
            except httpx.HTTPStatusError as e:
              last_error = f"HTTP {e.response.status_code}"
              logger.warning("Gemini HTTP error model=%s attempt=%s: %s", model_name, attempt, last_error)
              if e.response.status_code == 404:
                break
              if not self._should_retry(e.response.status_code) or attempt >= self.max_retries:
                break
              await asyncio.sleep(min(2 ** attempt, 10))
            except Exception as e:
              last_error = str(e)
              logger.warning("Gemini error model=%s attempt=%s: %s", model_name, attempt, last_error)
              if attempt >= self.max_retries:
                break
              await asyncio.sleep(min(2 ** attempt, 10))

    record_llm_event(
      telemetry_path,
      success=False,
      model=self.model,
      error=last_error,
      customer_id=customer_id,
    )
    raise RuntimeError(f"Gemini request failed after {self.max_retries} attempts: {last_error}")

  async def generate_json(
    self,
    *,
    system: Optional[str] = None,
    messages: List[GeminiMessage],
    temperature: float = 0.1,
    max_output_tokens: int = 4096,
    telemetry_path: str = "gemini_json",
    customer_id: Optional[str] = None,
  ) -> Dict[str, Any]:
    response = await self.generate(
      system=system,
      messages=messages,
      temperature=temperature,
      max_output_tokens=max_output_tokens,
      json_mode=True,
      telemetry_path=telemetry_path,
      customer_id=customer_id,
    )
    text = response.text
    if text.startswith("```"):
      text = re.sub(r"^```(?:json)?\s*", "", text)
      text = re.sub(r"\s*```$", "", text)
    return json.loads(text)

  async def stream(
    self,
    *,
    system: Optional[str] = None,
    messages: List[GeminiMessage],
    temperature: float = 0.2,
    max_output_tokens: int = 2048,
    telemetry_path: str = "gemini_stream",
    customer_id: Optional[str] = None,
  ) -> AsyncIterator[str]:
    if not self.is_configured:
      raise RuntimeError("GEMINI_API_KEY is not configured")

    payload = self._build_payload(
      system=system,
      messages=messages,
      temperature=temperature,
      max_output_tokens=max_output_tokens,
    )

    async with httpx.AsyncClient(timeout=self.timeout) as client:
      async with client.stream(
        "POST",
        self._url("streamGenerateContent") + "&alt=sse",
        headers=self._headers(),
        json=payload,
      ) as response:
        response.raise_for_status()
        async for line in response.aiter_lines():
          if not line.startswith("data: "):
            continue
          chunk_raw = line[6:].strip()
          if not chunk_raw or chunk_raw == "[DONE]":
            continue
          try:
            data = json.loads(chunk_raw)
            candidates = data.get("candidates") or []
            if candidates:
              parts = candidates[0].get("content", {}).get("parts") or []
              for part in parts:
                if "text" in part:
                  yield part["text"]
          except json.JSONDecodeError:
            continue

    record_llm_event(
      telemetry_path,
      success=True,
      model=self.model,
      customer_id=customer_id,
    )


# Singleton for dependency injection
_service: Optional[GeminiService] = None


def get_gemini_service() -> GeminiService:
  global _service
  if _service is None:
    _service = GeminiService()
  return _service


def reset_gemini_service() -> None:
  """For tests."""
  global _service
  _service = None
