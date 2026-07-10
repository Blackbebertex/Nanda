import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.gemini_service import GeminiService, GeminiMessage, reset_gemini_service
from services.config import get_settings
from agents.registry import reset_agents, get_agent
from agents.chat_agent import ChatAgent


class TestGeminiService(unittest.TestCase):
  def setUp(self):
    reset_gemini_service()
    reset_agents()
    get_settings.cache_clear()

  def test_not_configured_without_key(self):
    svc = GeminiService(api_key="")
    self.assertFalse(svc.is_configured)

  @patch("services.gemini_service.httpx.AsyncClient")
  def test_generate_success(self, mock_client_cls):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
      "candidates": [{"content": {"parts": [{"text": "Hello from Gemini"}]}}],
      "usageMetadata": {},
    }
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client_cls.return_value = mock_client

    svc = GeminiService(api_key="test-key", model="gemini-2.0-flash")

    import asyncio
    result = asyncio.run(svc.generate(
      messages=[GeminiMessage(role="user", content="Hi")],
      telemetry_path="test",
    ))
    self.assertEqual(result.text, "Hello from Gemini")
    self.assertEqual(result.model, "gemini-2.0-flash")


class TestChatAgent(unittest.TestCase):
  def setUp(self):
    reset_agents()

  def test_fallback_when_no_gemini(self):
    chat = ChatAgent(gemini=GeminiService(api_key=""))
    import asyncio
    reply, rec_ids = asyncio.run(chat.run(
      user_text="how am I doing",
      customer_context={"customerId": "cust_001", "riskProfile": "Moderate", "accounts": [], "goals": []},
      signals={"savings_rate": 0.22, "avg_savings_rate": 0.18},
      recommendation={},
      history=[],
    ))
    self.assertIn("saved", reply.lower())


class TestAgentRegistry(unittest.TestCase):
  def test_all_agents_registered(self):
    from agents.registry import list_agents
    agents = list_agents()
    for name in ("chat", "planning", "research", "coding", "analysis", "document", "workflow", "task_execution"):
      self.assertIn(name, agents)


if __name__ == "__main__":
  unittest.main()
