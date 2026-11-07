"""Gap-to-Proposal: one screen for a nonprofit finance lead.

Owner: Nabheel (UI). Skeleton wired by Jawad for the first end-to-end run; restyle freely,
but keep: status chips on every number, gifts and repayable money in separate rows,
the WHAT-IF badge, the evidence list, and the disclaimer.
Run: bash scripts/run_demo.sh
"""
import copy
import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine.proposal import evaluate  # noqa: E402

HISTORICAL = "Historical (as documented)"
CHIP = {"sourced": "🟢 sourced", "assumption": "🟡 ASSUMPTION", "unknown": "🔴 unknown"}


def usd(x):
    return "unknown" if x is None else "${:,.0f}".format(x)


def load_cases():
    paths = sorted((ROOT / "data" / "cases").glob("*.json")) + [ROOT / "contracts" / "example_case.json"]
    cases = {}
    for p in paths:
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
            cases["{}  ({})".format(c.get("title", p.stem), p.relative_to(ROOT))] = c
        except (OSError, ValueError):
            continue
    return cases


def md(text):
    """Markdown with literal dollar signs (Streamlit renders $...$ as LaTeX otherwise)."""
    st.markdown(text.replace("$", "\\$"))


def fact_line(facts, name, label, kind=None):
    f = facts.get(name, {})
    src = f.get("source") or {}
    where = " · {}, {}".format(src.get("doc", ""), src.get("locator", "")) if src else ""
    val = f.get("value")
    if val is None:
        shown = "unknown"
    elif kind == "usd":
        shown = usd(val)
    elif kind == "pct":
        shown = "{:.2f}%".format(val * 100)
    elif kind == "months":
        shown = "{} months".format(val)
    else:
        shown = val
    md("**{}**: {} {}{}".format(label, shown, CHIP.get(f.get("status"), ""), where))


st.set_page_config(page_title="Gap-to-Proposal", layout="wide")
st.caption("Prototype. Not financial, legal or lending advice. Public data only; every number shows its source or status.")

cases = load_cases()
case_key = st.sidebar.selectbox("Case", list(cases))
case = cases[case_key]
facts = case["facts"]

st.sidebar.header("What-if inputs")
st.sidebar.caption("Leave on 'as documented' for the historical case.")
overrides = {}

line = st.sidebar.selectbox("Existing line room today", ["as documented (unverified)", "verified: has room", "verified: full"])
if line != "as documented (unverified)":
    room = st.sidebar.number_input("Room on existing line ($)", value=825000 if "room" in line else 0, step=10000)
    overrides["existing_line_available"] = {"value": room, "status": "assumption", "verified_current": True}

months = st.sidebar.number_input("Months until city's final disbursement", value=int(facts["months_until_release"]["value"] or 6), min_value=1, max_value=36)
if months != facts["months_until_release"]["value"]:
    overrides["months_until_release"] = {"value": months, "status": "assumption"}

willing = st.sidebar.selectbox("Foundation willing to advance?", ["unknown", "yes", "no"])
if willing != "unknown":
    overrides["foundation_willing"] = {"value": willing == "yes", "status": "assumption"}

consent = st.sidebar.selectbox("City consents to repayment from its final disbursement (§7.13)?", ["unknown", "yes", "no"])
if consent != "unknown":
    overrides["assignment_consent"] = {"value": consent == "yes", "status": "assumption"}

deal_known = st.sidebar.checkbox("I have a quote for the advance's deal cost")
if deal_known:
    overrides["foundation_deal_cost"] = {"value": st.sidebar.number_input("Deal cost ($)", value=2000, step=500), "status": "assumption"}

cont_known = st.sidebar.checkbox("I know the contingency remaining")
if cont_known:
    overrides["contingency_remaining"] = {"value": st.sidebar.number_input("Contingency remaining ($)", value=0, step=5000), "status": "assumption"}

scenario = {"label": HISTORICAL if not overrides else "What-if: custom inputs", "overrides": overrides}
result = evaluate(copy.deepcopy(case), scenario)

badge = "🟠 WHAT-IF" if result.get("is_what_if") else "📅 HISTORICAL as of " + case.get("as_of", "")
st.title(case.get("title", "Case"))
st.subheader(badge)

left, mid, right = st.columns([1, 1.4, 1.1])

with left:
    md("### Needs")
    pn, tn = result["permanent_need"], result["temporary_need"]
    st.metric("Permanent fundraising need", usd(pn["value"]) + (" (upper bound)" if pn.get("upper_bound") else ""))
    st.caption(CHIP.get(pn["status"], "") + " · " + pn.get("note", pn.get("formula", "")))
    st.metric("Temporary cash need (repaid)", usd(tn["value"]))
    st.caption(CHIP.get(tn["status"], "") + " · repaid from: " + tn.get("repaid_from", "unknown"))
    md("#### Evidence behind these")
    for name, label, kind in [("construction_line_balance", "Construction line drawn", "usd"), ("construction_line_rate", "Construction line rate", "pct"),
                        ("months_late", "Months behind budget", "months"), ("contingency_remaining", "Contingency remaining", "usd"),
                        ("city_holdback", "City final disbursement", "usd"), ("holdback_release_condition", "Release condition", None),
                        ("past_sponsorship_excluded", "Past sponsorship (excluded from new money)", "usd")]:
        fact_line(facts, name, label, kind)

with mid:
    md("### Funding options")
    cols = st.columns(2)
    for col, opt in zip(cols, result["options"]):
        with col:
            md("**{}**".format(opt["label"]))
            md("Feasible: **{}**".format(opt["feasible"]))
            for m in opt["money"]:
                kind = "repayable" if m["repayable"] else "gift (not repaid)"
                extra = " · repaid from " + m["repaid_from"] if m.get("repaid_from") else ""
                md("- {}: **{}** ({}){}".format(m["provider"], usd(m["amount"]), kind, extra))
            md("Interest cost: {}".format(usd(opt["interest_cost"])))
            md("Deal cost: {}".format(usd(opt["deal_cost"])))
            for b in opt.get("blockers", []):
                md("🔴 " + b)
    s = result["advance_savings"]
    md("#### What the advance saves")
    md("Gross interest saved: **{}** · deal cost: **{}** · net: **{}** · worth it only if deal cost < **{}**".format(
        usd(s["gross"]), usd(s["deal_cost"]), usd(s["net"]), usd(s["break_even_deal_cost"])))

with right:
    rec = result["recommendation"]
    md("### Recommendation")
    md("**Verdict: {}**".format(rec["verdict"]))
    md(rec["text"])
    if rec.get("conditions"):
        md("Conditions:")
        for c in rec["conditions"]:
            md("- " + c)
    md("### Evidence still needed")
    for e in result.get("evidence_needed", []):
        md("🔴 " + (e if isinstance(e, str) else e.get("item", str(e))))
    if st.button("Draft proposal"):
        gift = result["options"][0]["money"][0]["amount"]
        lines = [
            "DRAFT FUNDING PROPOSAL (prototype; not sent)",
            "Project: " + case.get("title", ""),
            "Scenario: " + result["scenario"],
            "",
            "1. Gift request (permanent, not repaid): {}{}".format(usd(gift), " (upper bound)" if pn.get("upper_bound") else ""),
            "2. Timing gap (repaid from the city's final disbursement): {}".format(usd(tn["value"])),
            "   Option A: existing credit line, interest {}".format(usd(result["options"][0]["interest_cost"])),
            "   Option B: foundation advance, interest {}, deal cost {}".format(usd(result["options"][1]["interest_cost"]), usd(s["deal_cost"])),
            "",
            "Recommendation: " + rec["text"],
            "Evidence still needed: " + "; ".join(e if isinstance(e, str) else str(e) for e in result.get("evidence_needed", [])),
            "Gifts and repayable principal are listed separately and never summed.",
        ]
        st.code("\n".join(lines), language=None)
