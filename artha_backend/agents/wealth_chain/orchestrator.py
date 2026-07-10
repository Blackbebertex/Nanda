"""Plan persistence and wealth chain entry point (Gemini WorkflowAgent)."""
import hashlib
import json
from typing import Dict, Optional, Tuple

from agents.wealth_chain.schemas import ChainMetadata, ChainState
from services.database import get_db_session
from services.db_models import AuditChainRecord

_PLAN_STORE: Dict[str, ChainState] = {}


def _plan_payload(state: ChainState) -> Tuple[dict, str]:
  payload = state.model_dump(mode="json")
  payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
  return payload, payload_hash


def _close_session(session) -> None:
  if session is None:
    return
  try:
    session.close()
  except Exception:
    pass


def store_plan(state: ChainState) -> None:
  _PLAN_STORE[state.plan_id] = state
  if len(_PLAN_STORE) > 500:
    oldest = next(iter(_PLAN_STORE))
    _PLAN_STORE.pop(oldest, None)

  session = get_db_session()
  if not session:
    return

  try:
    payload, payload_hash = _plan_payload(state)
    record = session.get(AuditChainRecord, state.plan_id)
    if record is None:
      record = AuditChainRecord(
        plan_id=state.plan_id,
        customer_id=state.raw_steps.get("customer_id", "unknown"),
        chain_json=payload,
        confidence=state.step7.confidence if state.step7 else None,
        decision=state.step7.decision.value if state.step7 else None,
        integrity_hash=payload_hash,
      )
      session.add(record)
    else:
      record.customer_id = state.raw_steps.get("customer_id", record.customer_id)
      record.chain_json = payload
      record.confidence = state.step7.confidence if state.step7 else None
      record.decision = state.step7.decision.value if state.step7 else None
      record.integrity_hash = payload_hash
    session.commit()
  except Exception:
    try:
      session.rollback()
    except Exception:
      pass
  finally:
    _close_session(session)


def get_plan(plan_id: str) -> Optional[ChainState]:
  session = get_db_session()
  if session:
    try:
      record = session.get(AuditChainRecord, plan_id)
      if record and record.chain_json:
        return ChainState.model_validate(record.chain_json)
    except Exception:
      pass
    finally:
      _close_session(session)
  return _PLAN_STORE.get(plan_id)


async def run_wealth_chain(snapshot, signals, recommendation, product_catalog, user_text, customer_id):
  from agents.registry import get_agent
  workflow = get_agent("workflow")
  return await workflow.run(
    snapshot=snapshot,
    signals=signals,
    recommendation=recommendation,
    product_catalog=product_catalog,
    user_text=user_text,
    customer_id=customer_id,
  )
