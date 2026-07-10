import os
import sys

tests_dir = r'd:\IDBI\artha_backend\tests'
os.makedirs(tests_dir, exist_ok=True)

test_code = '''
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.consent_service import check_consent
from services.customer_snapshot import get_snapshot
from services.behaviour_engine import compute_signals
from services.advisory_engine import get_recommendation
from agents.compliance_guardrails import check_safety

class TestArthaServices(unittest.TestCase):
    def test_consent(self):
        self.assertTrue(check_consent(123))

    def test_snapshot(self):
        snap = get_snapshot(123)
        self.assertEqual(snap["savings"], 50000)
        self.assertEqual(snap["debts"], 1000)

    def test_behaviour_engine(self):
        signals = compute_signals([])
        self.assertEqual(signals["savings_rate"], 0.22)

    def test_advisory_engine(self):
        rec = get_recommendation({})
        self.assertEqual(rec["action"], "increase_emergency_fund")

    def test_compliance_guardrails(self):
        self.assertTrue(check_safety("Here is a safe response."))

if __name__ == '__main__':
    unittest.main()
'''

with open(os.path.join(tests_dir, 'test_services.py'), 'w', encoding='utf-8') as f:
    f.write(test_code)

print('Phase 3 Tests created.')
