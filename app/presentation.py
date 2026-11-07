"""Presentation only: preserve engine amounts; never combine gifts and loans."""
import html
import re

LABELS = {"sourced": "SOURCED", "assumption": "ASSUMPTION", "unknown": "UNKNOWN"}
VERDICTS = {
    "conditional": "Conditional — confirm the evidence",
    "gift_plus_existing_credit": "Option A · gift + existing credit",
    "gift_plus_foundation_advance": "Option B · gift + foundation advance",
    "no_bridge": "Neither bridge is feasible",
}


def esc(value):
    return html.escape(str(value))


def chip(status):
    status = status if status in LABELS else "unknown"
    return '<span class="chip %s">%s</span>' % (status, LABELS[status])


def usd(value):
    if value is None:
        return "Unknown"
    return "-${:,.0f}".format(-value) if value < 0 else "${:,.0f}".format(value)


def amount(value, status):
    return esc(usd(value)) + " " + chip("unknown" if value is None else status)


def combine(*statuses):
    return "unknown" if "unknown" in statuses else "assumption" if "assumption" in statuses else "sourced"


def fact_status(facts, name):
    f = facts.get(name, {})
    return f.get("status", "unknown") if f.get("value") is not None else "unknown"


def statuses(result, facts):
    a = result["options"][0].get("interest_cost_status", combine(*(fact_status(facts, n) for n in
        ("city_holdback", "existing_line_rate", "months_until_release"))))
    b = result["options"][1].get("interest_cost_status", combine(*(fact_status(facts, n) for n in
        ("city_holdback", "foundation_advance_rate", "months_until_release"))))
    gross = combine(a, b)
    cost = fact_status(facts, "foundation_deal_cost")
    return {"a": a, "b": b, "gross": gross, "cost": cost, "net": combine(gross, cost)}


def upper_bound(result):
    p = result["permanent_need"]
    return p.get("upper_bound", "upper bound" in p.get("note", "").lower())


def evidence(result, facts):
    items = [x if isinstance(x, str) else x.get("item", str(x)) for x in result.get("evidence_needed", [])]
    if facts.get("construction_line_balance", {}).get("verified_current") is False:
        items.append("Current construction loan balance, rate and renewal after recorded maturity")
    # The case owner explicitly records incomplete checks; do not hide those caveats.
    if any("not yet re-read" in f.get("note", "") for f in facts.values()):
        items.append("Re-read council packet conditions and confirm carried-over evidence")
    return list(dict.fromkeys(items))


def annotated(text, status="assumption"):
    """Narrative amounts are model statements, not verified offers."""
    return re.sub(r'\$[\d,]+(?:\.\d+)?|\d+(?:\.\d+)?%',
                  lambda m: m.group(0) + " " + chip(status), esc(text))


def source_link(fact, short=None):
    src = fact.get("source") or {}
    url = src.get("url", "")
    if not url.startswith(("https://", "http://")):
        return ""
    label = short or src.get("doc", "Source")
    return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a> · %s · source date %s' % (
        esc(url), esc(label), esc(src.get("locator", "")), esc(src.get("date", "unknown")))


def proposal_html(case, scenario, result, facts, fixture=False):
    """Printable one-page HTML, entirely from the evaluated snapshot and its evidence."""
    p, t, s = result["permanent_need"], result["temporary_need"], result["advance_savings"]
    st = statuses(result, facts)
    mode = "WHAT-IF — user assumptions, not verified offers" if result["is_what_if"] else "Historical (as of %s)" % case["as_of"]
    if fixture:
        mode = "CONTRACT FIXTURE — older saved example, not the current case"
    rows = []
    for i, option in enumerate(result["options"]):
        funds = []
        for m in option["money"]:
            status = t["status"] if m["repayable"] else p["status"]
            provider = m["provider"].split(" (")[0]
            funds.append("%s: %s · %s%s" % (esc(provider), amount(m["amount"], status),
                "REPAYABLE" if m["repayable"] else "GIFT, NOT REPAID",
                " (upper bound)" if not m["repayable"] and upper_bound(result) else ""))
        rows.append('<tr><td><b>%s</b><br>%s</td><td>%s</td><td>%s<br>%s</td></tr>' % (
            "A" if i == 0 else "B", esc(option["label"]), "<br>".join(funds),
            "Interest: " + amount(option["interest_cost"], st["a" if i == 0 else "b"]),
            "Deal cost: " + amount(option["deal_cost"], "assumption" if i == 0 else st["cost"])))
    sources = []
    for name in ("construction_line_balance", "city_holdback", "holdback_release_condition"):
        link = source_link(facts.get(name, {}))
        if link:
            sources.append(link)
    assumptions = []
    for name in ("months_late", "months_until_release", "existing_line_rate", "foundation_advance_rate", "contingency_remaining"):
        f = facts.get(name, {})
        value = f.get("value")
        display = "Unknown" if value is None else ("{:.2f}%".format(value * 100) if "rate" in name else usd(value) if "contingency" in name else str(value))
        assumptions.append(esc(name.replace("_", " ")) + ": " + esc(display) + " " + chip(fact_status(facts, name)))
    conditions = result["recommendation"].get("conditions", [])
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Draft funding proposal</title>
<style>
@page {size:letter; margin:0.42in} *{box-sizing:border-box} body{font:11px/1.35 Arial,sans-serif;color:#172c34;margin:24px auto;max-width:760px}
h1{font-size:23px;margin:4px 0} h2{font-size:13px;margin:12px 0 4px} p{margin:5px 0} table{border-collapse:collapse;width:100%%;font-size:11px} td,th{padding:8px;border:1px solid #c9d4d5;vertical-align:top;text-align:left}
.chip{display:inline-block;font-size:8px;font-weight:bold;border:1px solid;padding:1px 4px;border-radius:4px;white-space:nowrap}.sourced{color:#14604c;background:#e7f3ed}.assumption{color:#7c5100;background:#fff2d5}.unknown{color:#a32432;background:#fff0f0}
.mode{font-weight:bold;color:#875209} .evidence{color:#a32432} ul{margin:4px 0;padding-left:16px;columns:2;column-gap:24px} li{break-inside:avoid;margin-bottom:3px} a{color:#14604c} .sources{font-size:9px;overflow-wrap:anywhere} footer{margin-top:10px;border-top:1px solid #bbcaca;padding-top:6px;font-size:10px} @media print{body{margin:0;max-width:none}button{display:none}a{text-decoration:none}}
</style></head><body><button onclick="window.print()">Print / Save as PDF</button>
<p class="mode">DRAFT · NOT SENT · %s</p><h1>Funding proposal</h1><p>%s %s</p>
<h2>Two distinct requests</h2><p>Permanent gift: <b>%s</b>%s. Temporary principal: <b>%s</b>, repaid from %s. These are separate requests, never a combined fundraising total.</p>
<table><thead><tr><th>Structure</th><th>Who supplies the money</th><th>Modeled costs</th></tr></thead><tbody>%s</tbody></table>
<p>Feasibility: A — <b>%s</b>; B — <b>%s</b>. What-if feasibility remains an assumption, not an approval. Existing-credit deal cost is an assumed baseline.</p>
<h2>Savings from the advance</h2><p>Gross interest saved %s; less deal cost %s; net savings %s. Break-even deal cost %s. Savings compare costs only; they do not reduce the gift request automatically.</p>
<h2>Recommendation: %s</h2><p>%s</p><p>%s</p>
<h2 class="evidence">Evidence still needed before commitment</h2><ul class="evidence">%s</ul>
<h2>Model inputs and limits</h2><p>%s</p><p>Flat balance and simple interest; this is modeled delay carry, not the full project budget. Public loan data may be stale. Repayment also depends on all documented release conditions, including lien-free completion. The nonprofit pays interest and deal costs.</p>
<h2>Public evidence</h2><div class="sources">%s</div>
<footer>Prototype, not financial or legal advice. Consult qualified finance and legal professionals. No lender or foundation commitment is implied. Generated locally from the displayed result; no API call.</footer></body></html>''' % (
        esc(mode), esc(case["title"]), chip("sourced"), amount(p["value"], p["status"]),
        " (upper bound; contingency unknown)" if upper_bound(result) else "", amount(t["value"], t["status"]), esc(t["repaid_from"]),
        "".join(rows), esc(result["options"][0]["feasible"]), esc(result["options"][1]["feasible"]),
        amount(s["gross"], st["gross"]), amount(s["deal_cost"], st["cost"]), amount(s["net"], st["net"]), amount(s["break_even_deal_cost"], st["gross"]),
        esc(VERDICTS.get(result["recommendation"]["verdict"], "Review required")), annotated(result["recommendation"]["text"]),
        "Conditions: " + "; ".join(annotated(c) for c in conditions) if conditions else "Subject to evidence verification and professional review.",
        "".join("<li>%s</li>" % esc(e) for e in evidence(result, facts)), " · ".join(assumptions), "<br>".join(sources))
