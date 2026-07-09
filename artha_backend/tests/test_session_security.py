import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.session_store import add_session, validate_session
from agents.wealth_chain.orchestrator import _PLAN_STORE, store_plan
from agents.wealth_chain.schemas import ChainState
from main import require_plan_access
from fastapi import HTTPException


class TestSessionSecurity(unittest.TestCase):
    def setUp(self):
        _PLAN_STORE.clear()

    def test_session_bound_to_customer(self):
        add_session("sess_a", "en", "cust_001")
        self.assertTrue(validate_session("sess_a", "cust_001"))
        self.assertFalse(validate_session("sess_a", "cust_002"))
        self.assertFalse(validate_session("sess_missing", "cust_001"))

    def test_plan_access_denied_cross_customer(self):
        state = ChainState(plan_id="plan_x", raw_steps={"customer_id": "cust_001"})
        store_plan(state)
        plan = _PLAN_STORE["plan_x"]
        with self.assertRaises(HTTPException) as ctx:
            require_plan_access(plan, "cust_002")
        self.assertEqual(ctx.exception.status_code, 403)

    def test_plan_access_allowed_owner(self):
        state = ChainState(plan_id="plan_y", raw_steps={"customer_id": "cust_001"})
        store_plan(state)
        plan = _PLAN_STORE["plan_y"]
        require_plan_access(plan, "cust_001")


if __name__ == "__main__":
    unittest.main()
