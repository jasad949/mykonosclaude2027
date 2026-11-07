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
                              proposal_html, source_link, statuses, upper_bound)

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


def foundation_example():
    """A clearly hypothetical, reproducible offer; never mark inputs as sourced."""
    st.session_state.update(what_if=True, line_verified="As documented", room=825000,
                            months=6, rate=0.0, cost_known=True, cost=2000,
                            willing="Yes", consent="Yes", cont_known=False, cont=0)


def sidebar(facts, fixture):
    st.markdown("### Try a funding scenario")
    st.caption("Change the terms. See the borrowing decision update.")
    st.button("Try foundation example", key="foundation_example", on_click=foundation_example, disabled=fixture, use_container_width=True)
    enabled = st.toggle("Explore a what-if", disabled=fixture, key="what_if")
    st.caption("Every edited value is an ASSUMPTION. Verification here is hypothetical, not proof.")
    disabled = not enabled or fixture
    overrides = {}
    with st.expander("Adjust assumptions", expanded=enabled):
        line = st.selectbox("Line room verified?", ["As documented", "Yes", "No", "Unknown"], disabled=disabled, key="line_verified")
        room = st.number_input("Line room ($) · ASSUMPTION", min_value=0, value=int(facts["existing_line_available"].get("value") or 0), step=10000, disabled=disabled or line in ("As documented", "Unknown"), key="room")
        months = st.number_input("Months until release · ASSUMPTION", min_value=0, max_value=120, value=int(facts["months_until_release"].get("value") or 0), disabled=disabled, key="months")
        rate = st.number_input("Foundation annual rate (%) · ASSUMPTION", min_value=0.0, max_value=100.0, value=float(facts["foundation_advance_rate"].get("value") or 0) * 100, step=0.25, disabled=disabled, key="rate")
        cost_known = st.checkbox("Set deal cost · ASSUMPTION", disabled=disabled, key="cost_known")
        cost = st.number_input("Deal cost ($) · ASSUMPTION", min_value=0, value=2000, step=500, disabled=disabled or not cost_known, key="cost")
        willing = st.selectbox("Foundation willing? · ASSUMPTION", ["As documented", "Yes", "No", "Unknown"], disabled=disabled, key="willing")
        consent = st.selectbox("City consent? · ASSUMPTION", ["As documented", "Yes", "No", "Unknown"], disabled=disabled, key="consent")
        cont_known = st.checkbox("Set contingency remaining · ASSUMPTION", disabled=disabled, key="cont_known")
        cont = st.number_input("Contingency ($) · ASSUMPTION", min_value=0, value=0, step=5000, disabled=disabled or not cont_known, key="cont")
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
    st.set_page_config(page_title="Habitat OC · Raise or borrow?", page_icon="🏠", layout="wide")
    html((ROOT / "app/style.css").read_text())
    scenario_panel = st.sidebar.container()
    with st.sidebar.expander("Demo tools"):
        fixture = st.checkbox("Contract fixture preview", help="Older saved example; no engine call.", key="fixture")
    path = ROOT / ("contracts/example_case.json" if fixture else "data/cases/washington.json")
    try:
        case = load_json(path)
    except (OSError, ValueError) as exc:
        st.error("Case could not be loaded. Restore the checked-in Washington case before demoing.")
        st.caption(str(exc))
        st.stop()
    with scenario_panel:
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

    html('<div class="brand">MYKONOS / HABITAT OC FUNDING DESK</div>')
    st.title("What to raise. What to borrow.")
    st.write("For Habitat’s finance lead: plan the gift request, compare borrowing, and draft a funding proposal.")
    html('<div class="case-title">Washington Avenue · Santa Ana · 6 affordable homes %s</div>' % chip("sourced"))
    mode = "CONTRACT FIXTURE · saved example, not the current case" if fixture else "WHAT-IF · assumptions, not commitments" if result["is_what_if"] else "Historical (as of %s)" % case["as_of"]
    html('<div class="mode">%s</div><span class="disclaimer">Prototype, not financial or legal advice.</span>' % esc(mode))

    p, t, savings = result["permanent_need"], result["temporary_need"], result["advance_savings"]
    states = statuses(result, facts)
    verdict = result["recommendation"]["verdict"]
    decision = {
        "conditional": ("Confirm terms first", "Neither option is ready to choose without the missing evidence."),
        "gift_plus_existing_credit": ("A · Existing credit", "Available under these inputs. A cheaper foundation advance has not been established."),
        "gift_plus_foundation_advance": ("B · Foundation advance", "Lower cost under these inputs." if savings["net"] is not None and savings["net"] > 0 else "Available under these inputs; the existing line cannot cover the need."),
        "no_bridge": ("Find another lender", "Neither borrowing option can cover the timing gap under these inputs."),
    }.get(verdict, ("Review needed", "Check the detailed recommendation before acting."))
    raise_col, borrow_col, choose_col = st.columns(3, gap="medium")
    with raise_col:
        metric("How much do we need to raise?", p["value"], p["status"],
               "Gift · not repaid. Covers modeled delay interest.")
        st.caption("Upper bound: contingency unknown. Not the full project gap." if upper_bound(result) else "After available contingency. Not the full project gap.")
        html('<div class="source">%s</div>' % source_link(facts["construction_line_balance"], "Audit basis"))
    with borrow_col:
        metric("How much do we only need to borrow?", t["value"], t["status"],
               "Temporary cash · repaid when the city releases its final payment.")
        st.caption("The city must first confirm the release conditions are met.")
        html('<div class="source">%s</div>' % source_link(facts["city_holdback"], "City holdback"))
    with choose_col:
        html('<div class="metric decision"><div class="eyebrow">Which borrowing option makes sense?</div><div class="decision-title">%s</div><div class="note">%s</div></div>' % (esc(decision[0]), esc(decision[1])))
        st.caption("Conditional on assumptions; no offer or approval verified." if result["is_what_if"] else "Historical evidence is not a current lending commitment.")
        with st.expander("Why this answer?"):
            html('<p>%s</p>' % annotated(result["recommendation"]["text"]))
            for condition in result["recommendation"].get("conditions", []):
                html('<p>%s</p>' % annotated(condition))

    comparison, next_step = st.columns([2.05, 1], gap="large")
    with comparison:
        st.subheader("Compare ways to borrow")
        opts = result["options"]
        feasibility = {"yes": "Available under these inputs", "no": "Not available", "unknown": "Needs confirmation"}
        rows = []
        for label, repay in (("Gift · not repaid", False), ("Borrow · repay principal", True)):
            cells = []
            for opt in opts:
                money = next(m for m in opt["money"] if m["repayable"] == repay)
                cells.append(amount(money["amount"], t["status"] if repay else p["status"]) + '<small>' + esc(money["provider"].split(" (")[0]) + '</small>')
            rows.append((label, cells))
        rates = []
        for name in ("existing_line_rate", "foundation_advance_rate"):
            rate = facts[name].get("value")
            rates.append(("Unknown" if rate is None else "{:.2f}%".format(rate * 100)) + " " + chip(fact_status(facts, name)))
        rows.extend([
            ("Annual interest rate", rates),
            ("Interest until city payment", [amount(opts[0]["interest_cost"], states["a"]), amount(opts[1]["interest_cost"], states["b"])]),
            ("Deal cost", [amount(opts[0]["deal_cost"], "assumption"), amount(opts[1]["deal_cost"], states["cost"])]),
            ("Can we use it?", [esc(feasibility.get(o["feasible"], "Needs confirmation")) for o in opts]),
        ])
        html('<div class="comparison"><table><thead><tr><th scope="col">Funding &amp; cost</th><th scope="col">A · Existing credit</th><th scope="col">B · Foundation advance</th></tr></thead><tbody>' +
             ''.join('<tr><th scope="row">%s</th>%s</tr>' % (esc(label), ''.join('<td>%s</td>' % cell for cell in cells)) for label, cells in rows) + '</tbody></table></div>')
        savings_note = "After deal costs, compared with A"
        if savings["net"] is None:
            savings_note = "Enter deal cost to calculate savings" if savings["gross"] is not None else "Confirm rates and timing to calculate savings"
        elif savings["net"] < 0:
            savings_note = "B costs more than A under these inputs"
        elif savings["net"] == 0:
            savings_note = "Both options cost the same under these inputs"
        color = " costlier" if savings["net"] is not None and savings["net"] < 0 else ""
        html('<div class="savings%s"><div><b>Net savings with B</b><small>%s</small></div><strong>%s</strong></div>' % (color, esc(savings_note), amount(savings["net"], states["net"])))
        st.caption("Habitat repays the loan from the city payment and pays interest and fees. The gift is never repaid.")
        with st.expander("Costs, repayment & blockers"):
            html('<p>Interest saved %s − deal cost %s = net savings %s.</p>' % (amount(savings["gross"], states["gross"]), amount(savings["deal_cost"], states["cost"]), amount(savings["net"], states["net"])))
            html('<p>Break-even deal cost: %s. A’s deal cost is an assumed baseline.</p>' % amount(savings["break_even_deal_cost"], states["gross"]))
            for label, opt in zip(("A · Existing credit", "B · Foundation advance"), opts):
                st.markdown("**" + label + "**")
                if not opt.get("blockers"):
                    st.caption("No model blocker under these inputs. Confirm written terms before acting.")
                for blocker in opt.get("blockers", []):
                    html('<p class="bad">%s</p>' % annotated(blocker))
            fact_row(facts, "holdback_release_condition", "City payment conditions")
    with next_step:
        st.subheader("Your next step")
        st.write("Take a separate gift request and borrowing plan to your team or funder.")
        if st.button("Draft proposal", type="primary", use_container_width=True, key="draft_proposal"):
            st.session_state["proposal_html"] = proposal_html(case, scenario, result, facts, fixture=fixture)
            st.session_state["proposal_snapshot"] = snapshot
        st.caption("One-page draft · review, download, share yourself")
        st.markdown("**Evidence still needed**")
        needed = evidence(result, facts)
        html('<ul class="evidence">%s</ul>' % ''.join('<li>%s</li>' % esc(item) for item in needed[:3]))
        with st.expander("View the full evidence checklist"):
            html('<ul class="evidence">%s</ul>' % ''.join('<li>%s</li>' % esc(item) for item in needed))
        st.caption("Assumptions remain on the checklist until independently verified.")

    with st.expander("Inputs, sources & dates"):
        st.caption("SOURCED = documented, not necessarily current · ASSUMPTION = modeled or entered · UNKNOWN = missing")
        source_cols = st.columns(2)
        names = [("construction_line_balance", "Construction loan drawn"), ("construction_line_rate", "Annual construction rate"), ("months_late", "Delay"), ("contingency_remaining", "Contingency"), ("city_holdback", "Holdback"), ("holdback_release_condition", "Release conditions"), ("existing_line_available", "Existing line room"), ("existing_line_rate", "Existing rate"), ("months_until_release", "Time to release"), ("foundation_advance_rate", "Foundation rate"), ("foundation_deal_cost", "Deal cost"), ("past_sponsorship_excluded", "Past gift — excluded from new money")]
        names += [(name, name.replace("_", " ").capitalize()) for name in ("construction_line_maturity", "scheduled_construction_completion", "scheduled_move_in", "building_permit_issued") if name in facts]
        for i, (name, label) in enumerate(names):
            with source_cols[i % 2]:
                fact_row(facts, name, label)
    st.caption("Prototype, not financial or legal advice. Confirm decisions with qualified finance and legal professionals.")
    if "proposal_html" in st.session_state:
        st.divider()
        st.subheader("Draft funding proposal")
        st.download_button("Download printable proposal", st.session_state["proposal_html"], file_name="washington-funding-proposal.html", mime="text/html")
        components.html(st.session_state["proposal_html"], height=850, scrolling=True)


if __name__ == "__main__":
    main()
