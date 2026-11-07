import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.proposal import evaluate  # noqa: E402

C = ROOT / "contracts"


def load(name):
    with open(C / name, encoding="utf-8") as f:
        return json.load(f)


CASE = load("example_case.json")
SCENARIOS = {s["label"]: s for s in load("example_scenarios.json")["scenarios"]}
HIST = SCENARIOS["Historical (as documented)"]


class TestCoreMath(unittest.TestCase):
    def test_permanent_need_and_interest(self):
        r = evaluate(CASE, HIST)
        self.assertEqual(r["permanent_need"]["value"], 103270)
        a = [o for o in r["options"] if o["id"] == "gift_plus_existing_credit"][0]
        self.assertEqual(a["interest_cost"], 4950)


def opt(r, oid):
    return [o for o in r["options"] if o["id"] == oid][0]


def with_overrides(label, **overrides):
    return {"label": label, "overrides": overrides}


class TestGolden(unittest.TestCase):
    def test_historical_matches_example_result(self):
        r = evaluate(CASE, HIST)
        want = load("example_result.json")
        for k in ("is_what_if", "temporary_need", "advance_savings", "assumptions", "unknowns"):
            self.assertEqual(r[k], want[k], k)
        self.assertEqual(r["permanent_need"]["value"], 103270)
        self.assertEqual(r["permanent_need"]["status"], "assumption")
        self.assertTrue(r["permanent_need"]["upper_bound"])
        self.assertEqual(r["recommendation"]["verdict"], "conditional")
        self.assertEqual(opt(r, "gift_plus_existing_credit")["feasible"], "unknown")
        self.assertEqual(opt(r, "gift_plus_foundation_advance")["feasible"], "unknown")
        self.assertIn("Existing line room today", r["evidence_needed"])
        self.assertIn("Contingency remaining", r["evidence_needed"])

    def test_does_not_mutate_inputs(self):
        before = json.dumps(CASE, sort_keys=True)
        s = SCENARIOS["What-if: foundation says yes, city consents, $2,000 deal cost"]
        s_before = json.dumps(s, sort_keys=True)
        evaluate(CASE, s)
        self.assertEqual(json.dumps(CASE, sort_keys=True), before)
        self.assertEqual(json.dumps(s, sort_keys=True), s_before)


class TestWhatIfs(unittest.TestCase):
    def test_line_has_verified_room(self):
        r = evaluate(CASE, SCENARIOS["What-if: existing line has verified room"])
        self.assertTrue(r["is_what_if"])
        self.assertEqual(opt(r, "gift_plus_existing_credit")["feasible"], "yes")
        self.assertEqual(r["recommendation"]["verdict"], "gift_plus_existing_credit")
        self.assertIn("existing_line_available", r["assumptions"])

    def test_line_is_full(self):
        r = evaluate(CASE, SCENARIOS["What-if: existing line is full"])
        self.assertEqual(opt(r, "gift_plus_existing_credit")["feasible"], "no")
        self.assertEqual(opt(r, "gift_plus_foundation_advance")["feasible"], "unknown")
        self.assertEqual(r["recommendation"]["verdict"], "conditional")

    def test_foundation_yes_with_deal_cost(self):
        r = evaluate(CASE, SCENARIOS["What-if: foundation says yes, city consents, $2,000 deal cost"])
        self.assertEqual(opt(r, "gift_plus_foundation_advance")["feasible"], "yes")
        self.assertEqual(r["advance_savings"], {"gross": 4950, "deal_cost": 2000, "net": 2950,
                                                "break_even_deal_cost": 4950})
        self.assertEqual(r["advance_savings_status"], "assumption")
        self.assertEqual(r["recommendation"]["verdict"], "gift_plus_foundation_advance")

    def test_null_deal_cost_gives_null_net_never_zero(self):
        s = with_overrides("What-if: B confirmed, cost unknown",
                           foundation_willing={"value": True, "status": "assumption"},
                           assignment_consent={"value": True, "status": "assumption"})
        r = evaluate(CASE, s)
        self.assertIsNone(r["advance_savings"]["deal_cost"])
        self.assertIsNone(r["advance_savings"]["net"])
        self.assertEqual(r["advance_savings"]["gross"], 4950)
        self.assertEqual(r["advance_savings_status"], "unknown")
        self.assertNotEqual(r["recommendation"]["verdict"], "gift_plus_foundation_advance")

    def test_deal_cost_above_break_even_keeps_line(self):
        s = with_overrides("What-if: expensive advance",
                           existing_line_available={"value": 825000, "status": "assumption", "verified_current": True},
                           foundation_willing={"value": True, "status": "assumption"},
                           assignment_consent={"value": True, "status": "assumption"},
                           foundation_deal_cost={"value": 6000, "status": "assumption"})
        r = evaluate(CASE, s)
        self.assertEqual(r["advance_savings"]["net"], -1050)
        self.assertEqual(r["recommendation"]["verdict"], "gift_plus_existing_credit")

    def test_both_no_is_no_bridge(self):
        s = with_overrides("What-if: nothing works",
                           existing_line_available={"value": 0, "status": "assumption", "verified_current": True},
                           foundation_willing={"value": False, "status": "assumption"})
        r = evaluate(CASE, s)
        self.assertEqual(opt(r, "gift_plus_foundation_advance")["feasible"], "no")
        self.assertEqual(r["recommendation"]["verdict"], "no_bridge")


class TestStatusAndSeparation(unittest.TestCase):
    def test_known_contingency_removes_upper_bound(self):
        s = with_overrides("What-if: contingency 50k",
                           contingency_remaining={"value": 50000, "status": "assumption"})
        r = evaluate(CASE, s)
        self.assertEqual(r["permanent_need"]["value"], 53270)
        self.assertFalse(r["permanent_need"]["upper_bound"])

    def test_contingency_covers_delay_floors_at_zero(self):
        s = with_overrides("What-if: big contingency",
                           contingency_remaining={"value": 477762, "status": "assumption"})
        self.assertEqual(evaluate(CASE, s)["permanent_need"]["value"], 0)

    def test_unknown_input_gives_null_not_zero(self):
        s = with_overrides("What-if: months unknown",
                           months_until_release={"value": None, "status": "unknown"},
                           months_late={"value": None, "status": "unknown"})
        r = evaluate(CASE, s)
        self.assertIsNone(r["permanent_need"]["value"])
        self.assertEqual(r["permanent_need"]["status"], "unknown")
        self.assertIsNone(opt(r, "gift_plus_existing_credit")["interest_cost"])
        self.assertIsNone(r["advance_savings"]["net"])
        self.assertEqual(r["recommendation"]["verdict"], "conditional")

    def test_gift_and_principal_never_summed(self):
        r = evaluate(CASE, HIST)
        for o in r["options"]:
            gifts = [m for m in o["money"] if not m["repayable"]]
            loans = [m for m in o["money"] if m["repayable"]]
            self.assertEqual(len(gifts), 1)
            self.assertEqual(len(loans), 1)
            self.assertNotIn("total", o)
            self.assertNotIn(103270 + 220000, [m["amount"] for m in o["money"]])


if __name__ == "__main__":
    unittest.main()
