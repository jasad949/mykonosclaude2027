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


if __name__ == "__main__":
    unittest.main()
