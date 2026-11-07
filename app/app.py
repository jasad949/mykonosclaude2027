"""One-screen funding comparison. Run: bash scripts/run_demo.sh. Owner: Nabheel."""
import copy
import hashlib
import json
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.presentation import (amount, annotated, chip, esc, evidence, fact_status,
                              proposal_html, source_link, statuses, upper_bound, VERDICTS)

HISTORICAL = "Historical (as documented)"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def assumption(value, **extra):
    return {"value": value, "status": "assumption", "note": "User-entered what-if; not independently verified", **extra}


def html(text):
    st.markdown(text, unsafe_allow_html=True)


def metric(label, value, status, note=""):
    html('<div class="metric"><div class="eyebrow">%s</div><div class="value">%s</div><div class="note">%s</div></div>' %
         (esc(label), amount(value, status), esc(note)))


def fact_row(facts, name, label):
    f = facts.get(name, {})
    value = f.get("value")
    if value is None:
        shown = "Unknown"
    elif "rate" in name:
        shown = "{:.2f}%".format(value * 100)
    elif isinstance(value, bool):
        shown = "Yes" if value else "No"
    elif isinstance(value, (int, float)):
        shown = str(value) + " months" if "months" in name else "${:,.0f}".format(value)
    else:
        shown = str(value)
    html('<p><b>%s:</b> %s %s</p>' % (esc(label), esc(shown), chip(fact_status(facts, name))))
    if f.get("source"):
        html('<div class="source">%s</div>' % source_link(f))
    if f.get("as_of"):
        st.caption("Fact as of " + f["as_of"] + (" · not verified current" if f.get("verified_current") is False else ""))
    if f.get("note"):
        # A note can contain historical numbers beyond the primary fact.
        html('<div class="note">%s</div>' % annotated(f["note"], fact_status(facts, name)))


def sidebar(facts, fixture):
    st.sidebar.title("Scenario desk")
    enabled = st.sidebar.toggle("Explore a what-if", disabled=fixture, key="what_if")
    st.sidebar.caption("Every edited value is an ASSUMPTION. Verification here is hypothetical, not proof.")
    disabled = not enabled or fixture
    overrides = {}
    line = st.sidebar.selectbox("Line room verified?", ["As documented", "Yes", "No", "Unknown"], disabled=disabled, key="line_verified")
    room = st.sidebar.number_input("Line room ($) · ASSUMPTION", min_value=0, value=int(facts["existing_line_available"].get("value") or 0), step=10000, disabled=disabled or line in ("As documented", "Unknown"), key="room")
    months = st.sidebar.number_input("Months until release · ASSUMPTION", min_value=0, max_value=120, value=int(facts["months_until_release"].get("value") or 0), disabled=disabled, key="months")
    rate = st.sidebar.number_input("Foundation annual rate (%) · ASSUMPTION", min_value=0.0, max_value=100.0, value=float(facts["foundation_advance_rate"].get("value") or 0) * 100, step=0.25, disabled=disabled, key="rate")
    cost_known = st.sidebar.checkbox("Set deal cost · ASSUMPTION", disabled=disabled, key="cost_known")
    cost = st.sidebar.number_input("Deal cost ($) · ASSUMPTION", min_value=0, value=2000, step=500, disabled=disabled or not cost_known, key="cost")
    willing = st.sidebar.selectbox("Foundation willing? · ASSUMPTION", ["As documented", "Yes", "No", "Unknown"], disabled=disabled, key="willing")
    consent = st.sidebar.selectbox("City consent? · ASSUMPTION", ["As documented", "Yes", "No", "Unknown"], disabled=disabled, key="consent")
    cont_known = st.sidebar.checkbox("Set contingency remaining · ASSUMPTION", disabled=disabled, key="cont_known")
    cont = st.sidebar.number_input("Contingency ($) · ASSUMPTION", min_value=0, value=0, step=5000, disabled=disabled or not cont_known, key="cont")
    if enabled and not fixture:
        if line == "Unknown":
            overrides["existing_line_available"] = {"value": None, "status": "unknown", "verified_current": False}
        elif line != "As documented":
            overrides["existing_line_available"] = assumption(room, verified_current=line == "Yes")
        for key, value in (("months_until_release", months), ("foundation_advance_rate", rate / 100)):
            if value != facts[key].get("value"):
                overrides[key] = assumption(value)
        if cost_known:
            overrides["foundation_deal_cost"] = assumption(cost)
        if cont_known:
            overrides["contingency_remaining"] = assumption(cont)
        for name, choice in (("foundation_willing", willing), ("assignment_consent", consent)):
            if choice == "Unknown":
                overrides[name] = {"value": None, "status": "unknown"}
            elif choice != "As documented":
                overrides[name] = assumption(choice == "Yes")
    return {"label": "What-if: custom inputs" if enabled and not fixture else HISTORICAL, "overrides": overrides}


def main():
    st.set_page_config(page_title="Washington Avenue · Funding desk", page_icon="🏠", layout="wide")
    html('''<style>
    .block-container{padding:2.2rem 2rem 1rem;max-width:1700px} h1{font-size:1.9rem!important;padding-bottom:.3rem} h3{font-size:1.05rem!important} p{font-size:.88rem;line-height:1.45;margin-bottom:.5rem}
    .chip{display:inline-block;border:1px solid;border-radius:4px;padding:1px 5px;font:600 10px/1.6 sans-serif;vertical-align:middle;white-space:nowrap}
    .sourced{color:#14604c;background:#e7f3ed}.assumption{color:#7c5100;background:#fff2d5}.unknown{color:#a32432;background:#fff0f0}
    .metric{border:1px solid #cbdad6;border-left:4px solid #1f7160;border-radius:8px;padding:13px;margin-bottom:12px}
    .eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:.07em;font-weight:600}.value{font-size:27px;font-weight:650;margin:5px 0}.note,.source{font-size:11px;line-height:1.45;opacity:.85}.source{margin-bottom:7px}.source a{color:#247463}
    .mode{display:inline-block;border:1px solid #c9a455;border-radius:5px;padding:4px 10px;font-size:12px;font-weight:650;margin-bottom:12px}
    .money{border-bottom:1px solid #dce3e1;padding:8px 0}.money strong{font-size:18px}.money .chip{font-size:9px}.bad{color:#b32936;font-size:12px}.evidence{color:#b32936;padding-left:17px;font-size:12px;line-height:1.5}.verdict{background:#f2f6f3;color:#193c33;border-radius:8px;padding:12px;margin-bottom:10px;font-weight:600}
    [data-testid="stSidebar"] .block-container{padding-top:1rem} [data-testid="stSidebar"] label p{font-size:12px} [data-testid="stVerticalBlock"]{gap:.65rem}
    </style>''')
    fixture = st.sidebar.checkbox("Contract fixture preview", help="Static saved example result; no evaluation. Older fixture, not the current case.", key="fixture")
    path = ROOT / ("contracts/example_case.json" if fixture else "data/cases/washington.json")
    try:
        case = load_json(path)
    except (OSError, ValueError) as exc:
        st.error("Case could not be loaded. Restore the checked-in Washington case before demoing.")
        st.caption(str(exc))
        st.stop()
    scenario = sidebar(case["facts"], fixture)
    facts = copy.deepcopy(case["facts"])
    facts.update(scenario["overrides"])
    if fixture:
        result = load_json(ROOT / "contracts/example_result.json")
    else:
        from engine.proposal import evaluate
        result = evaluate(case, scenario)
    st.session_state["evaluated_result"] = result
    st.session_state["evaluated_scenario"] = scenario
    snapshot = hashlib.sha256(json.dumps([case, scenario, result], sort_keys=True).encode()).hexdigest()
    if st.session_state.get("proposal_snapshot") != snapshot:
        st.session_state.pop("proposal_html", None)
    st.caption("MYKONOS · FUNDING DESK")
    st.title("Habitat OC · Washington Avenue")
    html('<p>%s %s</p>' % (esc(case["title"]), chip("sourced")))
    mode = "CONTRACT FIXTURE · saved example, not the current case" if fixture else "WHAT-IF · assumptions, not commitments" if result["is_what_if"] else "Historical (as of %s)" % case["as_of"]
    html('<div class="mode">%s</div>' % esc(mode))
    st.caption("Prototype, not financial or legal advice. Consult qualified finance and legal professionals before acting.")
    left, middle, right = st.columns([1, 1.7, 1.15], gap="medium")
    p, t, savings = result["permanent_need"], result["temporary_need"], result["advance_savings"]
    states = statuses(result, facts)
    with left:
        st.subheader("The two needs")
        metric("Permanent · gift", p["value"], p["status"], "Upper bound · contingency unknown" if upper_bound(result) else "Modeled delay carry after contingency")
        html('<div class="source">%s</div>' % source_link(facts["construction_line_balance"], "Audited loan balance"))
        metric("Temporary · repaid", t["value"], t["status"], "Repaid from the city's final disbursement")
        html('<div class="source">%s</div>' % source_link(facts["city_holdback"], "City holdback"))
        html('<p class="note">Separate needs, never one fundraising total. Permanent need models delay interest, not the full project budget.</p>')
        with st.expander("Inputs, sources & dates"):
            for name, label in [("construction_line_balance", "Construction loan drawn"), ("construction_line_rate", "Annual construction rate"), ("months_late", "Delay"), ("contingency_remaining", "Contingency"), ("city_holdback", "Holdback"), ("holdback_release_condition", "Release conditions"), ("existing_line_available", "Existing line room"), ("existing_line_rate", "Existing rate"), ("months_until_release", "Time to release"), ("foundation_advance_rate", "Foundation rate"), ("foundation_deal_cost", "Deal cost"), ("past_sponsorship_excluded", "Past gift — excluded from new money")]:
                fact_row(facts, name, label)
            for name in ("construction_line_maturity", "scheduled_construction_completion", "scheduled_move_in", "building_permit_issued"):
                if name in facts:
                    fact_row(facts, name, name.replace("_", " ").capitalize())
    with middle:
        st.subheader("Compare the funding")
        cols = st.columns(2, gap="small")
        for i, (col, opt) in enumerate(zip(cols, result["options"])):
            with col:
                st.markdown("**%s · %s**" % ("A" if i == 0 else "B", "Existing credit" if i == 0 else "Foundation advance"))
                html('<p>Feasible: <b>%s</b>%s</p>' % (esc(opt["feasible"].upper()), " · in this what-if" if result["is_what_if"] else ""))
                for money in opt["money"]:
                    repay = money["repayable"]
                    html('<div class="money"><div class="eyebrow">%s</div><strong>%s</strong><div class="note">%s%s</div></div>' % (
                        "REPAYABLE PRINCIPAL" if repay else "GIFT · NOT REPAID", amount(money["amount"], t["status"] if repay else p["status"]),
                        esc(money["provider"].split(" (")[0]), " · upper bound" if not repay and upper_bound(result) else ""))
                rate_name = "existing_line_rate" if i == 0 else "foundation_advance_rate"
                rate = facts[rate_name].get("value")
                html('<p>Annual rate: %s %s</p>' % ("Unknown" if rate is None else "{:.2f}%".format(rate * 100), chip(fact_status(facts, rate_name))))
                html('<p>Interest: %s</p><p>Deal cost: %s</p>' % (amount(opt["interest_cost"], states["a" if i == 0 else "b"]), amount(opt["deal_cost"], "assumption" if i == 0 else states["cost"])))
                html('<p class="note">Principal repaid from city final disbursement. Interest is an additional cost.</p>')
                for blocker in opt.get("blockers", []):
                    html('<div class="bad">• %s</div>' % annotated(blocker))
        st.markdown("**Advance savings after costs**")
        html('<p>Gross %s − deal cost %s</p>' % (amount(savings["gross"], states["gross"]), amount(savings["deal_cost"], states["cost"])))
        metric("Net savings · B versus A", savings["net"], states["net"], "Savings are not another gift or a funding commitment")
        html('<p class="note">Break-even deal cost: %s. Existing-credit deal cost is an assumed baseline.</p>' % amount(savings["break_even_deal_cost"], states["gross"]))
    with right:
        st.subheader("Next decision")
        rec = result["recommendation"]
        html('<div class="verdict">%s</div>' % esc(VERDICTS.get(rec["verdict"], "Review required")))
        if result["is_what_if"]:
            st.caption("This recommendation depends on user assumptions; no offer or approval is verified.")
        if rec["verdict"] == "conditional":
            st.write("Keep the gift request separate. Confirm bridge availability, written terms and repayment permission before selecting an option.")
        elif rec["verdict"] == "no_bridge":
            st.write("Neither modeled bridge is available. Find another temporary funding source; retain the separate gift request.")
        else:
            st.write("Use the indicated structure only after the evidence below is confirmed. Gifts do not repay principal; city disbursement does.")
        with st.expander("Recommendation rationale"):
            html('<p>%s</p>' % annotated(rec["text"]))
            for condition in rec.get("conditions", []):
                html('<p>%s</p>' % annotated(condition))
        st.markdown("**Evidence still needed**")
        html('<ul class="evidence">%s</ul>' % "".join('<li>%s</li>' % esc(e) for e in evidence(result, facts)))
        if st.button("Draft proposal", type="primary", use_container_width=True):
            st.session_state["proposal_html"] = proposal_html(case, scenario, result, facts)
            st.session_state["proposal_snapshot"] = snapshot
        st.caption("One-page draft · generated locally · not sent")
    if "proposal_html" in st.session_state:
        st.divider()
        st.subheader("Draft funding proposal")
        st.download_button("Download printable proposal", st.session_state["proposal_html"], file_name="washington-funding-proposal.html", mime="text/html")
        components.html(st.session_state["proposal_html"], height=850, scrolling=True)


if __name__ == "__main__":
    main()
