"""Centralized prompt template management."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Dict


PROMPTS_DIR = os.path.join(
  os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
  "agents",
  "prompts",
)


@lru_cache(maxsize=64)
def load_prompt(name: str) -> str:
  path = os.path.join(PROMPTS_DIR, f"{name}.md")
  if not os.path.exists(path):
    raise FileNotFoundError(f"Prompt template not found: {name}")
  with open(path, "r", encoding="utf-8") as f:
    return f.read()


def render_prompt(name: str, **kwargs: str) -> str:
  template = load_prompt(name)
  for key, value in kwargs.items():
    template = template.replace(f"{{{{{key}}}}}", str(value))
  return template


def list_prompts() -> Dict[str, str]:
  if not os.path.isdir(PROMPTS_DIR):
    return {}
  return {
    f[:-3]: os.path.join(PROMPTS_DIR, f)
    for f in os.listdir(PROMPTS_DIR)
    if f.endswith(".md")
  }
