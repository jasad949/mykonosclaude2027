"""Gap-to-Proposal: a one-page brief for a nonprofit finance lead preparing a foundation request.

Owner: app/ (UI). Reads the case file and calls engine.proposal.evaluate(case, scenario).
Run: bash scripts/run_demo.sh
"""
import copy
import datetime as dt
import html
import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine.proposal import evaluate  # noqa: E402

HISTORICAL = "Historical (as documented)"
SAMPLE_OFFER = "What-if: foundation says yes, city consents, $2,000 deal cost"
STATUS_WORD = {"sourced": "Documented", "assumption": "Assumed", "unknown": "Unknown"}
FEASIBLE_WORD = {"yes": "Ready", "no": "Not available", "unknown": "Not confirmed"}
LINE_MODES = ["As documented (not confirmed today)", "Confirmed: has room", "Confirmed: full"]
YN = ["Unknown", "Yes", "No"]

st.set_page_config(page_title="Gap-to-Proposal", page_icon="📄", layout="wide",
                   initial_sidebar_state="collapsed")

# ---------- style ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Inter:wght@400;500;600&display=swap');
:root { --paper:#F6F1E7; --card:#FBF8F2; --ink:#1C1A17; --muted:#6B645A; --rule:#D9CFBF; --accent:#A4532F; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] { background: var(--paper) !important; color: var(--ink); }
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="collapsedControl"], footer { display:none !important; }
.block-container, [data-testid="stMainBlockContainer"], [data-testid="block-container"] { max-width: 1060px !important; margin: 0 auto !important; padding: 2.2rem 1.5rem 4rem !important; }
html, body, p, li, label, div, span, button, input { font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif; }
.gp-brand { display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap; font-size:.78rem; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); border-bottom:1px solid var(--rule); padding-bottom:.6rem; }
.gp-brand b { color: var(--accent); font-weight:600; }
.gp-h1 { font-family:'Source Serif 4', Georgia, serif; font-weight:600; font-size:clamp(1.9rem, 4.2vw, 2.7rem); line-height:1.12; margin:1.4rem 0 .5rem; color:var(--ink); }
.gp-sub { color:var(--muted); font-size:.98rem; margin:0; }
.gp-dates { color:var(--muted); font-size:.84rem; margin:.35rem 0 0; }
.gp-section { margin-top:2.6rem; }
.gp-kicker { font-size:.74rem; letter-spacing:.1em; text-transform:uppercase; color:var(--accent); font-weight:600; border-top:1px solid var(--ink); padding-top:.55rem; margin-bottom:.9rem; }
.gp-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:1rem; }
.gp-card { background:var(--card); border:1px solid var(--rule); padding:1.1rem 1.2rem 1rem; }
.gp-label { font-size:.82rem; color:var(--muted); font-weight:500; }
.gp-fig { font-family:'Inter', sans-serif; font-variant-numeric: tabular-nums; font-weight:600; font-size:clamp(1.9rem, 4vw, 2.4rem); color:var(--ink); margin:.15rem 0 .35rem; white-space:nowrap; }
.gp-fig small { font-size:.55em; font-weight:500; color:var(--muted); margin-right:.3rem; }
.gp-status { display:inline-block; font-size:.72rem; letter-spacing:.06em; text-transform:uppercase; font-weight:600; padding:.12rem .45rem; border:1px solid currentColor; }
.st-doc { color:#3E6B4A; } .st-ass { color:var(--accent); } .st-unk { color:#8A3B3B; }
.gp-card p, .gp-text { font-size:.92rem; line-height:1.5; margin:.5rem 0 0; }
.gp-assume { list-style:none; padding:0 !important; margin:.6rem 0 0 !important; font-size:.86rem; }
.gp-assume li { margin:0 !important; padding-left:0 !important; }
.gp-assume li { padding:.28rem 0; border-top:1px solid var(--rule); }
.gp-assume li b { font-weight:600; margin-right:.35rem; }
.gp-note { font-size:.82rem; color:var(--muted); margin-top:.7rem; }
.gp-state { display:flex; flex-wrap:wrap; align-items:baseline; gap:.6rem; margin-bottom:.4rem; }
.gp-state .tag { font-size:.75rem; letter-spacing:.08em; text-transform:uppercase; font-weight:600; color:#fff; background:var(--ink); padding:.18rem .55rem; }
.gp-state .tag.whatif { background:var(--accent); }
.gp-verdict { font-family:'Source Serif 4', Georgia, serif; font-size:clamp(1.35rem, 2.8vw, 1.7rem); line-height:1.3; margin:.2rem 0 .4rem; }
.gp-table-wrap { overflow-x:auto; margin-top:.9rem; }
.gp-table { width:100%; border-collapse:collapse; font-size:.9rem; font-variant-numeric: tabular-nums; }
.gp-table th { text-align:left; font-size:.74rem; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); font-weight:600; border-bottom:1px solid var(--ink); padding:.45rem .5rem; white-space:nowrap; }
.gp-table td { border-bottom:1px solid var(--rule); padding:.6rem .5rem; vertical-align:top; }
.gp-table td.num { text-align:right; white-space:nowrap; } .gp-table th.num { text-align:right; }
.gp-savings { margin-top:.9rem; font-size:.95rem; padding:.7rem .9rem; border-left:3px solid var(--accent); background:var(--card); }
.gp-memo { background:#fff; border:1px solid var(--rule); padding:1.4rem 1.6rem; font-family:'Source Serif 4', Georgia, serif; font-size:1rem; line-height:1.55; margin-top:.8rem; }
.gp-memo .hd { font-family:'Inter', sans-serif; font-size:.84rem; color:var(--muted); border-bottom:1px solid var(--rule); padding-bottom:.6rem; margin-bottom:.8rem; }
.gp-memo h4 { font-family:'Inter', sans-serif; font-size:.78rem; letter-spacing:.08em; text-transform:uppercase; margin:1rem 0 .3rem; color:var(--accent); }
.gp-memo p, .gp-memo li, .gp-memo b { font-family:'Source Serif 4', Georgia, serif !important; font-size:1rem; }
.gp-table th, .gp-table td { border-left:none !important; border-right:none !important; border-top:none; background:transparent !important; }
.gp-table { border:none !important; }
.gp-foot { margin-top:3rem; border-top:1px solid var(--rule); padding-top:.7rem; font-size:.8rem; color:var(--muted); }
[data-testid="stPopover"] button { border-radius:0; border:1px solid var(--ink); background:transparent; color:var(--ink); }
div.stButton > button { border-radius:0; border:1px solid var(--ink); background:transparent; color:var(--ink); font-weight:500; }
div.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] { background:var(--accent); border-color:var(--accent); color:#fff; }
div.stButton > button:hover { border-color:var(--accent); color:var(--accent); }
div.stButton > button[kind="primary"]:hover { color:#fff; filter:brightness(.95); }
[data-testid="stExpander"] details { border:1px solid var(--rule); border-radius:0; background:var(--card); }
[data-testid="stExpander"] summary p { font-size:.88rem; font-weight:500; }
.stMarkdown a { color: var(--accent); }
</style>
""", unsafe_allow_html=True)


# ---------- helpers ----------
def h(text):
    """HTML-escape and stop Streamlit from reading $...$ as math."""
    return html.escape(str(text)).replace("$", "&#36;")


def money(x):
    if x is None:
        return "unknown"
    return "−&#36;{:,.0f}".format(-x) if x < 0 else "&#36;{:,.0f}".format(x)


def md(text):
    st.markdown(str(text).replace("$", "\\$"))


def nice_date(s):
    try:
        return dt.date.fromisoformat(str(s)[:10]).strftime("%-d %b %Y")
    except ValueError:
        return str(s)


def status_html(status):
    cls = {"sourced": "st-doc", "assumption": "st-ass", "unknown": "st-unk"}.get(status, "st-unk")
    return '<span class="gp-status {}">{}</span>'.format(cls, STATUS_WORD.get(status, "Unknown"))


def source_line(fact):
    src = (fact or {}).get("source") or {}
    if not src:
        return ""
    label = "{}, {}".format(src.get("doc", ""), src.get("locator", ""))
    url = src.get("url")
    return "[{}]({})".format(label, url) if url else label


def fval(facts, name):
    return (facts.get(name) or {}).get("value")


def load_cases():
    cases = {}
    for p in sorted((ROOT / "data" / "cases").glob("*.json")):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
            cases[c.get("title", p.stem)] = c
        except (OSError, ValueError):
            continue
    try:
        ex = json.loads((ROOT / "contracts" / "example_case.json").read_text(encoding="utf-8"))
        cases["Test data: contract example"] = ex
    except (OSError, ValueError):
        pass
    return cases


def load_scenarios():
    try:
        return json.loads((ROOT / "contracts" / "example_scenarios.json").read_text(encoding="utf-8"))["scenarios"]
    except (OSError, ValueError, KeyError):
        return [{"label": HISTORICAL, "overrides": {}}]


CASES = load_cases()
SCENARIOS = load_scenarios()


# ---------- state: controls are the single source of truth ----------
def defaults(case):
    return {
        "line_mode": LINE_MODES[0], "line_room": int(fval(case["facts"], "existing_line_available") or 0),
        "months_release": int(fval(case["facts"], "months_until_release") or 6),
        "willing": "Unknown", "consent": "Unknown",
        "deal_known": False, "deal_cost": 2000, "cont_known": False, "contingency": 0, "show_draft": False,
    }


def write_controls(values):
    for k, v in values.items():
        st.session_state[k] = v


def reset_documented():
    write_controls(defaults(CASES[st.session_state["case_key"]]))


def apply_scenario(label):
    case = CASES[st.session_state["case_key"]]
    vals = defaults(case)
    sc = next((s for s in SCENARIOS if s["label"] == label), None)
    for name, f in (sc or {}).get("overrides", {}).items():
        v = f.get("value")
        if name == "existing_line_available" and f.get("verified_current"):
            vals["line_mode"] = LINE_MODES[1] if (v or 0) > 0 else LINE_MODES[2]
            vals["line_room"] = int(v or 0)
        elif name == "foundation_willing":
            vals["willing"] = "Yes" if v else "No"
        elif name == "assignment_consent":
            vals["consent"] = "Yes" if v else "No"
        elif name == "foundation_deal_cost" and v is not None:
            vals["deal_known"], vals["deal_cost"] = True, int(v)
        elif name == "months_until_release" and v is not None:
            vals["months_release"] = int(v)
        elif name == "contingency_remaining" and v is not None:
            vals["cont_known"], vals["contingency"] = True, int(v)
    write_controls(vals)


if "case_key" not in st.session_state:
    st.session_state["case_key"] = next(iter(CASES))
    reset_documented()
CASE = CASES[st.session_state["case_key"]]
FACTS = CASE["facts"]


def build_overrides():
    s, ov = st.session_state, {}
    if s["line_mode"] != LINE_MODES[0]:
        room = s["line_room"] if s["line_mode"] == LINE_MODES[1] else 0
        ov["existing_line_available"] = {"value": room, "status": "assumption", "verified_current": True}
    if s["months_release"] != fval(FACTS, "months_until_release"):
        ov["months_until_release"] = {"value": s["months_release"], "status": "assumption"}
    if s["willing"] != "Unknown":
        ov["foundation_willing"] = {"value": s["willing"] == "Yes", "status": "assumption"}
    if s["consent"] != "Unknown":
        ov["assignment_consent"] = {"value": s["consent"] == "Yes", "status": "assumption"}
    if s["deal_known"]:
        ov["foundation_deal_cost"] = {"value": s["deal_cost"], "status": "assumption"}
    if s["cont_known"]:
        ov["contingency_remaining"] = {"value": s["contingency"], "status": "assumption"}
    return ov


def scenario_label(ov):
    if not ov:
        return HISTORICAL
    for sc in SCENARIOS:
        if sc["overrides"] and {k: v.get("value") for k, v in sc["overrides"].items()} == {k: v.get("value") for k, v in ov.items()}:
            return sc["label"]
    return "What-if: custom assumptions"


def assumption_words(ov):
    words = []
    if "existing_line_available" in ov:
        v = ov["existing_line_available"]["value"]
        words.append("Existing credit line confirmed with {} of room".format(money(v)) if v else "Existing credit line confirmed full")
    if "foundation_willing" in ov:
        words.append("Foundation {} to advance funds".format("is willing" if ov["foundation_willing"]["value"] else "declines"))
    if "assignment_consent" in ov:
        words.append("City {} repayment from its final disbursement (§7.13)".format("consents to" if ov["assignment_consent"]["value"] else "refuses"))
    if "foundation_deal_cost" in ov:
        words.append("Advance costs {} all-in (legal and fees)".format(money(ov["foundation_deal_cost"]["value"])))
    if "months_until_release" in ov:
        words.append("City releases its holdback in {} months".format(ov["months_until_release"]["value"]))
    if "contingency_remaining" in ov:
        words.append("{} of budget contingency remains".format(money(ov["contingency_remaining"]["value"])))
    return words


OVERRIDES = build_overrides()
SCENARIO = {"label": scenario_label(OVERRIDES), "overrides": OVERRIDES}
R = evaluate(copy.deepcopy(CASE), SCENARIO)
PN, TN = R["permanent_need"], R["temporary_need"]
OPT_A, OPT_B = R["options"][0], R["options"][1]
SAV = R["advance_savings"]
REC = R["recommendation"]
MERGED = dict(FACTS, **OVERRIDES)

# ---------- 1. masthead ----------
title = CASE.get("title", "")
org, _, place = title.partition(" - ")
address, _, units = place.partition(" (")
hold = FACTS.get("city_holdback", {})
hold_src = hold.get("source") or {}
city_asof = hold.get("as_of")
st.markdown(
    '<div class="gp-brand"><span><b>Gap-to-Proposal</b> &nbsp;·&nbsp; funding brief</span>'
    '<span>Prototype · not financial, legal or lending advice</span></div>'
    '<div class="gp-h1">How should we cover the wait for city funding?</div>'
    '<p class="gp-sub">{addr} · {units} · {org}</p>'
    '<p class="gp-dates">Case checked {checked}{city}</p>'.format(
        addr=h(address or title), units=h(units.rstrip(")")) if units else "", org=h(org),
        checked=nice_date(CASE.get("as_of", "")),
        city=(" · City figures as of {} ({}, published {})".format(
            nice_date(city_asof), h(hold_src.get("doc", "city report")), nice_date(hold_src.get("date", "")))
            if city_asof else "")),
    unsafe_allow_html=True)

# ---------- 2. the two amounts ----------
grant_total = fval(FACTS, "city_grant_total")
months_late = fval(MERGED, "months_late")
rate = fval(FACTS, "construction_line_rate")
bal = fval(FACTS, "construction_line_balance")
cont = MERGED.get("contingency_remaining", {})
assume_items = [
    ("Assumed", "{} months behind the budgeted sales date".format(months_late)),
    ("Documented", "Construction line {} drawn at {:.2f}%, interest-only".format(money(bal), (rate or 0) * 100)),
    ("Assumed", "The line stayed fully drawn the whole time"),
    (STATUS_WORD.get(cont.get("status"), "Unknown"),
     "Contingency remaining: {}".format(money(cont.get("value")) if cont.get("value") is not None else "unknown, treated as &#36;0")),
]
past = fval(FACTS, "past_sponsorship_excluded")
st.markdown(
    '<div class="gp-section"><div class="gp-kicker">Two different amounts</div><div class="gp-grid">'
    '<div class="gp-card"><div class="gp-label">City grant awaiting release</div>'
    '<div class="gp-fig">{tn}</div>{tn_st}'
    '<p>The city is holding the last part of its {gt} grant until every home closes and the site is lien-free. '
    'It repays whatever bridges the wait, so this is <b>temporary cash</b>, not new fundraising.</p></div>'
    '<div class="gp-card"><div class="gp-label">Additional fundraising (modeled)</div>'
    '<div class="gp-fig"><small>Up to</small>{pn}</div>{pn_st}'
    '<p>Extra interest from the delay. This is the <b>permanent</b> gap a gift must cover.</p>'
    '<ul class="gp-assume">{items}</ul></div>'
    '</div><p class="gp-note">Not counted as new money: {past} already raised at Leaders Build 2024.</p></div>'.format(
        tn=money(TN["value"]), tn_st=status_html(TN["status"]),
        gt=money(grant_total) if grant_total else "city",
        pn=money(PN["value"]), pn_st=status_html(PN["status"]),
        items="".join("<li><b>{}</b>{}</li>".format(h(w), t) for w, t in assume_items),
        past=money(past) if past else "Past sponsorship"),
    unsafe_allow_html=True)
e1, e2 = st.columns(2)
with e1:
    with st.expander("Release conditions and source"):
        md(fval(FACTS, "holdback_release_condition") or "Unknown")
        md("Holdback: " + source_line(hold))
        md("Conditions: " + source_line(FACTS.get("holdback_release_condition")))
with e2:
    with st.expander("How the fundraising estimate is built"):
        md("Interest = line balance × rate ÷ 12 × months late − contingency remaining.")
        md("Line: " + source_line(FACTS.get("construction_line_balance")))
        md("Months late: " + (FACTS.get("months_late", {}).get("note") or "assumption"))
        md("Contingency: " + (FACTS.get("contingency_remaining", {}).get("note") or "unknown"))

# ---------- 3. test a foundation offer ----------
st.markdown('<div class="gp-section"><div class="gp-kicker">Test a foundation offer</div></div>', unsafe_allow_html=True)
is_doc = not R.get("is_what_if")
state_tag = '<span class="tag">Documented case</span>' if is_doc else '<span class="tag whatif">What-if</span>'
state_txt = "Public records only. Nothing assumed beyond the modeled figures above." if is_doc else h(SCENARIO["label"].replace("What-if: ", "").capitalize())
st.markdown('<div class="gp-state">{}<span class="gp-text">{}</span></div>'.format(state_tag, state_txt), unsafe_allow_html=True)
words = assumption_words(OVERRIDES)
if words:
    st.markdown('<ul class="gp-assume">{}</ul>'.format("".join("<li><b>Assumed</b>{}</li>".format(w) for w in words)), unsafe_allow_html=True)

b1, b2, b3 = st.columns([1.3, 1.3, 1])
b1.button("Test a foundation offer", type="primary", on_click=apply_scenario, args=(SAMPLE_OFFER,), use_container_width=True,
          help="Foundation willing, city consents, $2,000 all-in costs (all assumed)")
b2.button("Reset to documented case", on_click=reset_documented, use_container_width=True)
other = [s["label"] for s in SCENARIOS if s["label"] not in (HISTORICAL, SAMPLE_OFFER)]
with b3.popover("More scenarios", use_container_width=True):
    for lab in other:
        st.button(lab.replace("What-if: ", "").capitalize(), key="sc_" + lab, on_click=apply_scenario, args=(lab,), use_container_width=True)

with st.expander("Edit assumptions"):
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Existing credit line today", LINE_MODES, key="line_mode")
        st.number_input("Room on the existing line (USD)", min_value=0, step=25000, key="line_room",
                        disabled=st.session_state["line_mode"] != LINE_MODES[1])
        st.number_input("Months until the city releases its holdback", min_value=1, max_value=36, key="months_release")
        st.checkbox("I know the contingency remaining", key="cont_known")
        st.number_input("Contingency remaining (USD)", min_value=0, step=5000, key="contingency",
                        disabled=not st.session_state["cont_known"])
    with c2:
        st.selectbox("Foundation willing to advance?", YN, key="willing")
        st.selectbox("City consents to repayment from its final disbursement (§7.13)?", YN, key="consent")
        st.checkbox("I have a quote for the advance's all-in costs", key="deal_known")
        st.number_input("Advance all-in costs (USD)", min_value=0, step=500, key="deal_cost",
                        disabled=not st.session_state["deal_known"])
    if len(CASES) > 1:
        st.selectbox("Case", list(CASES), key="case_key", on_change=reset_documented)

# ---------- 4. result ----------
VERDICT = {
    "conditional": "Not decided yet: confirm the open items before choosing how to bridge the wait.",
    "gift_plus_existing_credit": "Ask for a gift and bridge the wait on the existing credit line.",
    "gift_plus_foundation_advance": "Ask for a gift and take the foundation advance to bridge the wait.",
    "no_bridge": "Neither bridge is available: another source is needed for the wait.",
}
st.markdown(
    '<div class="gp-section"><div class="gp-kicker">Recommendation</div>'
    '<div class="gp-verdict">{v}</div><p class="gp-text">{t}</p>'
    '<p class="gp-note">Both options ask the foundation for the same gift, <b>up to {gift}</b> (not repaid). '
    'They differ only in how the {wait} wait is bridged.</p>'.format(
        v=h(VERDICT.get(REC["verdict"], REC["verdict"])), t=h(REC["text"]),
        gift=money(PN["value"]), wait=money(TN["value"])),
    unsafe_allow_html=True)


def bridge_name(opt):
    m = [x for x in opt["money"] if x["repayable"]]
    return h(m[0]["provider"]) if m else "None"


rows = "".join(
    "<tr><td><b>{name}</b><br><span class='gp-note'>{bridge} · repaid from the city's final disbursement</span></td>"
    "<td class='num'>{amt}</td><td class='num'>{intr}</td><td class='num'>{deal}</td><td>{feas}</td></tr>".format(
        name=h(o["label"]), bridge=bridge_name(o),
        amt=money(next((x["amount"] for x in o["money"] if x["repayable"]), None)),
        intr=money(o["interest_cost"]), deal=money(o["deal_cost"]),
        feas=FEASIBLE_WORD.get(o["feasible"], o["feasible"]))
    for o in (OPT_A, OPT_B))
if SAV.get("net") is None:
    sav = "Break-even: the advance beats the credit line only if its all-in costs stay below <b>{}</b>.".format(money(SAV["break_even_deal_cost"]))
elif SAV["net"] >= 0:
    sav = "Modeled net savings from the advance: <b>{}</b> ({} of interest avoided, less {} of costs).".format(
        money(SAV["net"]), money(SAV["gross"]), money(SAV["deal_cost"]))
else:
    sav = "The advance costs <b>{}</b> more than the credit line after its {} of costs.".format(money(-SAV["net"]), money(SAV["deal_cost"]))
st.markdown(
    '<div class="gp-table-wrap"><table class="gp-table"><thead><tr><th>Option</th><th class="num">Bridge</th>'
    '<th class="num">Interest</th><th class="num">Costs</th><th>Status</th></tr></thead><tbody>{}</tbody></table></div>'
    '<div class="gp-savings">{}</div></div>'.format(rows, sav),
    unsafe_allow_html=True)

blockers = OPT_A.get("blockers", []) + OPT_B.get("blockers", [])
with st.expander("Open items before sending ({})".format(len(R.get("evidence_needed", [])))):
    for e in R.get("evidence_needed", []):
        md("- " + e)
    if blockers:
        md("**Blocking the options now:**")
        for b in blockers:
            md("- " + b)

st.button("Hide draft proposal" if st.session_state["show_draft"] else "Draft proposal", type="primary",
          on_click=lambda: st.session_state.update(show_draft=not st.session_state["show_draft"]))
if st.session_state["show_draft"]:
    bridge = OPT_B if REC["verdict"] == "gift_plus_foundation_advance" else OPT_A
    open_items = "".join("<li>{}</li>".format(h(e)) for e in R.get("evidence_needed", []))
    st.markdown(
        '<div class="gp-memo"><div class="hd">DRAFT · not sent · {scen}<br>To: Foundation program officer &nbsp;·&nbsp; '
        'From: Finance lead, {org} &nbsp;·&nbsp; Re: {addr}</div>'
        '<p>We are completing {units} at {addr}. Construction delays added interest that our budget did not cover, and '
        'the city is holding {wait} of its grant until every home closes.</p>'
        '<h4>1. Gift request (not repaid)</h4><p>Up to <b>{gift}</b> to cover the additional interest from the delay. '
        'This is an upper bound; we will confirm the final figure from our books.</p>'
        '<h4>2. Bridging the wait (repaid)</h4><p>{wait} until the city\'s final disbursement. {bridge_txt}</p>'
        '<h4>Before we finalize</h4><ul>{open}</ul>'
        '<p class="gp-note">Gifts and repayable amounts are listed separately and never added together.</p></div>'.format(
            scen=h("Documented case" if is_doc else SCENARIO["label"]), org=h(org or "the nonprofit"),
            addr=h(address or title), units=h(units.rstrip(")")) if units else "these homes",
            wait=money(TN["value"]), gift=money(PN["value"]),
            bridge_txt=("We propose a foundation advance of {} at {}, repaid from the city's release; it saves an estimated {} versus our credit line.".format(
                money(TN["value"]), bridge_name(OPT_B).split("(")[-1].rstrip(")"), money(SAV["net"]))
                if bridge is OPT_B else
                "We plan to carry it on our existing credit line (estimated interest {}). An interest-free advance would help only if its all-in costs stay below {}.".format(
                    money(OPT_A["interest_cost"]), money(SAV["break_even_deal_cost"]))),
            open=open_items),
        unsafe_allow_html=True)

# ---------- 5. sources ----------
with st.expander("Sources"):
    seen = set()
    for name, f in FACTS.items():
        line = source_line(f)
        if line and line not in seen:
            seen.add(line)
            md("- " + line + " (" + str((f.get("source") or {}).get("date", "")) + ")")
st.markdown('<div class="gp-foot">Gap-to-Proposal · Prototype built at the Claude Impact Lab, 7 Nov 2026. '
            'Public data only; not financial, legal or lending advice. Every figure is documented, assumed or unknown.</div>',
            unsafe_allow_html=True)
