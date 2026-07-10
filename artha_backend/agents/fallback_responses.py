"""Keyword fallback when GEMINI_API_KEY is not set (demo mode only)."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from agents.llm_telemetry import record_llm_event


def _sip_details(snapshot: Dict[str, Any]):
  for acc in snapshot.get("accounts", []):
    if acc.get("type") == "MF_SIP":
      return acc.get("sipAmount", 0), acc.get("fundName", "Mutual Fund")
  return 0, "Mutual Fund"


def _primary_goal_name(snapshot: Dict[str, Any]) -> str:
  goals = snapshot.get("goals") or []
  return goals[0].get("name", "your goal") if goals else "your goal"


def keyword_reply(
  user_text: str,
  customer_context: Dict[str, Any],
  signals: Dict[str, Any],
  recommendation: Dict[str, Any],
  language: str = "en",
) -> Tuple[str, List[str]]:
  lower = user_text.lower()
  is_hindi = language == "hi" or re.search(r"\b(theek|kya|aap|nahi|hai|main|hoon|hindi)\b", lower)
  rec_ids = [recommendation["recommendation_id"]] if recommendation.get("recommendation_id") else []
  rate_pct = round(signals.get("savings_rate", 0.22) * 100, 1)
  avg_pct = round(signals.get("avg_savings_rate", 0.18) * 100, 1)
  sip_amount, fund_name = _sip_details(customer_context)
  goal_name = _primary_goal_name(customer_context)
  risk = customer_context.get("riskProfile", "Moderate")
  customer_id = customer_context.get("customerId")

  if is_hindi:
    comparison = "behtar" if rate_pct >= avg_pct else "kam"
    reply = f"Bilkul! Aapki savings rate is mahine {rate_pct}% hai — yeh aapke average {avg_pct}% se {comparison} hai."
    if sip_amount:
      reply += f" Aapka ₹{int(sip_amount):,}/month SIP {goal_name} ke liye active hai."
  elif re.search(r"\b(doing|summary|overview|status)\b", lower):
    comparison = "above" if rate_pct >= avg_pct else "below"
    reply = f"You saved **{rate_pct}%** of your income this month! This is {comparison} your usual {avg_pct}%."
  elif re.search(r"\b(sip|mutual fund|investment)\b", lower):
    reply = (
      f"Your SIP of **₹{int(sip_amount):,}/month** into {fund_name} is active."
      if sip_amount else "No active SIP found on your profile."
    )
  elif re.search(r"\b(recommend|suggest|advice)", lower):
    if recommendation.get("reasonCode") == "DORMANT_FD_REALLOCATION":
      reply = f"Based on your {risk.lower()} risk profile, your **Fixed Deposit** could be reviewed for better goal alignment."
    elif recommendation.get("reasonCode") == "INSUFFICIENT_EMERGENCY_FUND":
      reply = "Your emergency fund looks short of the 3-month buffer. Want to build it up gradually?"
    else:
      reply = f"Based on your {risk.lower()} risk profile, I have a tailored suggestion from our rules engine."
  else:
    reply = f"Hello! You saved **{rate_pct}%** of your income this month. What would you like to explore?"

  record_llm_event("chat_fallback", success=False, model="keyword_mock", customer_id=customer_id)
  return reply, rec_ids
