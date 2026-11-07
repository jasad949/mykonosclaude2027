"""Contract check. Owner: Jawad.

    python3 scripts/check_contract.py                 # engine on example vs contracts/example_result.json
    python3 scripts/check_contract.py --case FILE     # schema-check a case file, then run the engine on it

Exit codes: 0 PASS, 1 FAIL, 2 engine not merged yet (schema checks still run).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
C = ROOT / "contracts"

REQUIRED_FACTS = [
    "construction_line_balance", "construction_line_rate", "months_late", "contingency_remaining",
    "city_holdback", "holdback_release_condition", "months_until_release", "existing_line_rate",
    "existing_line_available", "foundation_advance_rate", "foundation_deal_cost", "foundation_willing",
    "assignment_consent", "past_sponsorship_excluded",
]
EXPECTED_VERDICTS = {
    "Historical (as documented)": "conditional",
    "What-if: existing line has verified room": "gift_plus_existing_credit",
    "What-if: existing line is full": "conditional",
    "What-if: foundation says yes, city consents, $2,000 deal cost": "gift_plus_foundation_advance",
}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def check_case(case):
    errs = []
    if case.get("contract_version") != "1":
        errs.append("contract_version must be '1'")
    for k in ("case_id", "title", "as_of", "facts"):
        if k not in case:
            errs.append("missing top-level field: " + k)
    facts = case.get("facts", {})
    for name in REQUIRED_FACTS:
        if name not in facts:
            errs.append("missing fact: " + name)
    for name, f in facts.items():
        st = f.get("status")
        if st not in ("sourced", "assumption", "unknown"):
            errs.append("%s: bad status %r" % (name, st))
        if st == "unknown" and f.get("value") is not None:
            errs.append("%s: unknown facts must have value null" % name)
        if st == "sourced":
            src = f.get("source") or {}
            for k in ("doc", "locator", "url", "date"):
                if not src.get(k):
                    errs.append("%s: sourced fact missing source.%s" % (name, k))
    return errs


def pick(result):
    """The fields the UI depends on, in a comparable form."""
    return {
        "is_what_if": result.get("is_what_if"),
        "permanent_need": (result["permanent_need"]["value"], result["permanent_need"]["status"]),
        "temporary_need": result["temporary_need"]["value"],
        "options": [
            (o["id"], [(m["amount"], m["repayable"]) for m in o["money"]], o["permanent_gap_reduction"],
             o["temporary_cash"], o["interest_cost"], o["deal_cost"], o["feasible"])
            for o in result["options"]
        ],
        "advance_savings": result["advance_savings"],
        "verdict": result["recommendation"]["verdict"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", help="case file to schema-check and run")
    args = ap.parse_args()

    case_path = Path(args.case) if args.case else C / "example_case.json"
    case = load(case_path)
    errs = check_case(case)
    print("Schema %s: %s" % (case_path.relative_to(ROOT) if case_path.is_absolute() else case_path,
                             "PASS" if not errs else "FAIL"))
    for e in errs:
        print("  - " + e)

    try:
        from engine.proposal import evaluate
    except ImportError as exc:
        print("Engine: not merged yet (%s). Schema checks only." % exc)
        return 1 if errs else 2

    ok = not errs
    scenarios = load(C / "example_scenarios.json")["scenarios"]
    if args.case:
        for s in scenarios:
            r = evaluate(case, s)
            print("  %-62s verdict=%s" % (s["label"], r["recommendation"]["verdict"]))
    else:
        got = pick(evaluate(case, scenarios[0]))
        want = pick(load(C / "example_result.json"))
        for k in want:
            if got[k] != want[k]:
                ok = False
                print("FAIL %s\n  want %r\n  got  %r" % (k, want[k], got[k]))
        for s in scenarios:
            v = evaluate(case, s)["recommendation"]["verdict"]
            exp = EXPECTED_VERDICTS.get(s["label"])
            if v != exp:
                ok = False
                print("FAIL verdict for %r: want %s, got %s" % (s["label"], exp, v))
    print("Contract:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
