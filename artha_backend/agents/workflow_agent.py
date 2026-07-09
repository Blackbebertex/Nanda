"""Workflow Agent — orchestrates the 7-step wealth chain via Gemini agents."""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from agents.analysis_agent import AnalysisAgent
from agents.coding_agent import CodingAgent
from agents.document_agent import DocumentAgent
from agents.planning_agent import PlanningAgent
from agents.wealth_chain.auditor import merge_auditor_result, run_programmatic_checks
from agents.wealth_chain.cache import get_step1_cached, set_step1_cached
from agents.wealth_chain.mock_chain import build_mock_chain, prior_steps_json
from agents.wealth_chain.orchestrator import store_plan
from agents.wealth_chain.schemas import (
  AuditDecision,
  ChainMetadata,
  ChainState,
  Step1Output,
  Step2Output,
  Step3Output,
  Step4Output,
  Step5Output,
  Step6Output,
  Step7Output,
)
from agents.wealth_chain.prompt_loader import render_prompt as render_chain_prompt
from agents.pii_masker import format_customer_facts_masked, mask_snapshot_for_llm, mask_text_for_llm
from agents.base_agent import BaseAgent
from agents.llm_telemetry import record_llm_event
from services.config import get_settings
import json


STEP_FILES = [
  "step1_wealth_analyst.md",
  "step2_goal_architect.md",
  "step3_portfolio_strategist.md",
  "step4_red_team.md",
  "step5_blue_team.md",
  "step6_wealth_avatar.md",
  "step7_master_auditor.md",
]

STEP_MODELS = [Step1Output, Step2Output, Step3Output, Step4Output, Step5Output, Step6Output, Step7Output]
MAX_REVISE_LOOPS = 2


class WorkflowAgent(BaseAgent):
  name = "workflow"
  description = "7-step audited wealth prompt chain orchestration via Gemini"

  def __init__(self, gemini=None):
    super().__init__(gemini)
    self.analysis = AnalysisAgent(gemini=self.gemini)
    self.planning = PlanningAgent(gemini=self.gemini)
    self.coding = CodingAgent(gemini=self.gemini)
    self.document = DocumentAgent(gemini=self.gemini)

  async def run(
    self,
    *,
    snapshot: Dict[str, Any],
    signals: Dict[str, Any],
    recommendation: Dict[str, Any],
    product_catalog: str,
    user_text: str,
    customer_id: str,
  ) -> Tuple[ChainState, ChainMetadata]:
    return await self._run_chain(
      snapshot, signals, recommendation, product_catalog, user_text, customer_id
    )

  def _build_context(self, snapshot, signals, recommendation, product_catalog, state, user_text):
    masked_snap = mask_snapshot_for_llm(snapshot)
    return {
      "PYTHON_FACTS": format_customer_facts_masked(snapshot, signals),
      "CUSTOMER_SNAPSHOT": json.dumps(masked_snap, indent=2),
      "PRIOR_STEPS_JSON": prior_steps_json(state),
      "BANK_PRODUCT_CATALOG": product_catalog,
      "RULES_ENGINE_RECOMMENDATION": json.dumps(recommendation, indent=2),
      "USER_MESSAGE": mask_text_for_llm(user_text),
      "PROGRAMMATIC_CHECKS": "[]",
    }

  async def _call_step(self, idx, ctx, customer_id, fix_targets):
    if idx not in fix_targets:
      return None
    step_file = STEP_FILES[idx - 1]
    if idx == 1:
      agent = self.analysis
    elif idx in (2, 3):
      agent = self.planning
    elif idx in (4, 5, 7):
      agent = self.coding
    elif idx == 6:
      agent = self.document
    else:
      agent = self.coding
    return await agent.run(
      step_file=step_file,
      context=ctx,
      step_index=idx,
      customer_id=customer_id,
      user_instruction=f"Produce Step {idx} JSON.",
    )

  async def _run_chain(self, snapshot, signals, recommendation, product_catalog, user_text, customer_id):
    settings = get_settings()
    revise_loops = 0
    fix_targets: Optional[List[int]] = None
    state: Optional[ChainState] = None

    while revise_loops <= MAX_REVISE_LOOPS:
      if self.gemini.is_configured:
        state = await self._run_steps_gemini(
          snapshot, signals, recommendation, product_catalog, user_text, customer_id, fix_targets
        )
      else:
        checks, _ = run_programmatic_checks(
          state or ChainState(), snapshot, signals, recommendation, []
        )
        state = build_mock_chain(snapshot, signals, recommendation, user_text, checks)

      if not state.step7:
        checks, prog_conf = run_programmatic_checks(state, snapshot, signals, recommendation, [])
        state.step7 = merge_auditor_result(checks, prog_conf, None)

      decision = state.step7.decision
      if decision in (AuditDecision.APPROVE, AuditDecision.REJECT):
        break
      if decision == AuditDecision.REVISE and state.step7.fix_targets and revise_loops < MAX_REVISE_LOOPS:
        fix_targets = state.step7.fix_targets
        revise_loops += 1
        continue
      break

    state.raw_steps["customer_id"] = customer_id
    store_plan(state)
    meta = ChainMetadata(
      confidence=state.step7.confidence if state.step7 else 0,
      decision=state.step7.decision.value if state.step7 else "reject",
      steps_completed=sum(1 for i in range(1, 8) if getattr(state, f"step{i}", None)),
      plan_id=state.plan_id,
      revise_loops=revise_loops,
      path="deep",
    )
    record_llm_event(
      "wealth_chain_complete",
      success=state.step7.decision != AuditDecision.REJECT if state.step7 else False,
      model=settings.gemini_model if self.gemini.is_configured else "mock_chain",
      customer_id=customer_id,
      extra={"confidence": meta.confidence, "decision": meta.decision},
    )
    return state, meta

  async def _run_steps_gemini(self, snapshot, signals, recommendation, product_catalog, user_text, customer_id, fix_targets):
    state = ChainState(plan_id=f"plan_{uuid.uuid4().hex[:12]}")
    fix_targets = fix_targets or list(range(1, 8))
    ctx = self._build_context(snapshot, signals, recommendation, product_catalog, state, user_text)

    cached = get_step1_cached(customer_id, snapshot)
    if cached and 1 in fix_targets:
      state.step1 = Step1Output(**cached)
    elif 1 in fix_targets:
      data = await self.analysis.run(
        step_file=STEP_FILES[0], context=ctx, customer_id=customer_id
      )
      if data:
        state.step1 = Step1Output(**data)
        set_step1_cached(customer_id, snapshot, state.step1.model_dump())

    for idx in range(2, 7):
      ctx = self._build_context(snapshot, signals, recommendation, product_catalog, state, user_text)
      data = await self._call_step(idx, ctx, customer_id, fix_targets)
      if data:
        model = STEP_MODELS[idx - 1]
        setattr(state, f"step{idx}", model(**data))

    checks, prog_conf = run_programmatic_checks(
      state, snapshot, signals, recommendation,
      [p["product_id"] for p in json.loads(product_catalog)] if product_catalog.startswith("[") else [],
    )
    ctx = self._build_context(snapshot, signals, recommendation, product_catalog, state, user_text)
    ctx["PROGRAMMATIC_CHECKS"] = json.dumps([c.model_dump() for c in checks], indent=2)
    data = await self.coding.run(
      step_file=STEP_FILES[6],
      context=ctx,
      step_index=7,
      customer_id=customer_id,
      user_instruction="Produce Step 7 audit JSON.",
    )
    llm7 = Step7Output(**data) if data else None
    state.step7 = merge_auditor_result(checks, prog_conf, llm7)

    for i in range(1, 8):
      step = getattr(state, f"step{i}", None)
      if step:
        state.raw_steps[f"step{i}"] = step.model_dump()
    return state
