import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.wealth_chain import orchestrator
from agents.wealth_chain.schemas import ChainState


class FakeRedis:
    def __init__(self):
        self.data = {}

    def setex(self, key, ttl, value):
        self.data[key] = value
        return True

    def get(self, key):
        return self.data.get(key)


class FakeDbSession:
    def __init__(self):
        self.records = {}
        self.commits = 0
        self.rollbacks = 0
        self.closed = False

    def get(self, model, key):
        return self.records.get(key)

    def add(self, record):
        self.records[record.plan_id] = record

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1

    def close(self):
        self.closed = True


class TestPlanStore(unittest.TestCase):
    def setUp(self):
        orchestrator._PLAN_STORE.clear()
        orchestrator.get_db_session = lambda: None

    def test_memory_round_trip(self):
        state = ChainState(plan_id="plan_memory", raw_steps={"step1": {"foo": "bar"}})
        orchestrator.store_plan(state)
        fetched = orchestrator.get_plan("plan_memory")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.plan_id, "plan_memory")
        self.assertEqual(fetched.raw_steps, {"step1": {"foo": "bar"}})

    def test_database_round_trip(self):
        fake_session = FakeDbSession()
        orchestrator.get_db_session = lambda: fake_session
        state = ChainState(plan_id="plan_db", raw_steps={"step7": {"decision": "approve", "confidence": 90}})
        orchestrator.store_plan(state)
        orchestrator._PLAN_STORE.clear()
        fetched = orchestrator.get_plan("plan_db")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.plan_id, "plan_db")
        self.assertEqual(fetched.raw_steps["step7"]["decision"], "approve")
        self.assertIn("plan_db", fake_session.records)
        self.assertEqual(fake_session.commits, 1)
        self.assertTrue(fake_session.closed)
