"""Agent registry — single entry point for all Gemini-powered agents."""
from __future__ import annotations

from typing import Dict, Optional, Type

from agents.analysis_agent import AnalysisAgent
from agents.base_agent import BaseAgent
from agents.chat_agent import ChatAgent
from agents.coding_agent import CodingAgent
from agents.document_agent import DocumentAgent
from agents.planning_agent import PlanningAgent
from agents.research_agent import ResearchAgent
from agents.task_execution_agent import TaskExecutionAgent
from agents.workflow_agent import WorkflowAgent
from services.gemini_service import GeminiService, get_gemini_service

_AGENT_TYPES: Dict[str, Type[BaseAgent]] = {
  "chat": ChatAgent,
  "planning": PlanningAgent,
  "research": ResearchAgent,
  "coding": CodingAgent,
  "analysis": AnalysisAgent,
  "document": DocumentAgent,
  "workflow": WorkflowAgent,
  "task_execution": TaskExecutionAgent,
}

_instances: Dict[str, BaseAgent] = {}


def get_agent(name: str, gemini: Optional[GeminiService] = None) -> BaseAgent:
  if name not in _AGENT_TYPES:
    raise ValueError(f"Unknown agent: {name}. Available: {list(_AGENT_TYPES)}")
  if name not in _instances:
    _instances[name] = _AGENT_TYPES[name](gemini=gemini or get_gemini_service())
  return _instances[name]


def list_agents() -> Dict[str, str]:
  return {k: _AGENT_TYPES[k].description for k in _AGENT_TYPES}


def reset_agents() -> None:
  _instances.clear()
