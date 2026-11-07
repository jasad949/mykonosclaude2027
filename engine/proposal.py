"""Gap engine v1. Owner: Omar. Standard library only, Python 3.9+.

evaluate(case, scenario) -> result dict shaped like contracts/example_result.json.

Rules (contracts/README.md):
- Permanent need (fundraising, never repaid) is kept apart from temporary need (timing gap,
  repaid from the city's final disbursement). Gift money and repayable principal are never summed.
- None means unknown, never 0. Dollars are rounded only at output.
- Status: any unknown input -> unknown; else any assumption -> assumption; else sourced.
"""
import copy
import math

HISTORICAL_LABEL = "Historical (as documented)"
OPTION_A = "gift_plus_existing_credit"
OPTION_B = "gift_plus_foundation_advance"

PERMANENT_FORMULA = ("construction_line_balance * construction_line_rate / 12 * months_late"
                     " - contingency_remaining")


# ---------------------------------------------------------------- helpers

def _fact(facts, name):
    f = facts.get(name)
    if not isinstance(f, dict):
        return {"value": None, "status": "unknown"}
    return f


def _status(facts, name):
    f = _fact(facts, name)
    st = f.get("status")
    if st not in ("sourced", "assumption", "unknown") or (f.get("value") is None):
        return "unknown"
    return st


def _num(facts, name):
    """Numeric value or None. Unknown status or non-numeric value -> None."""
    if _status(facts, name) == "unknown":
        return None
    v = _fact(facts, name).get("value")
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return float(v)


def _bool(facts, name):
    """True / False / None (unknown)."""
    if _status(facts, name) == "unknown":
        return None
    v = _fact(facts, name).get("value")
    return v if isinstance(v, bool) else None


def _combine(statuses):
    statuses = list(statuses)
    if "unknown" in statuses:
        return "unknown"
    if "assumption" in statuses:
        return "assumption"
    return "sourced"


def _money(x):
    """Round half away from zero to whole dollars; None stays None."""
    if x is None:
        return None
    return int(math.copysign(math.floor(abs(x) + 0.5), x))


def _usd(x):
    return "unknown" if x is None else "${:,}".format(_money(x))


def _pct(rate):
    return "rate unknown" if rate is None else "{:.2f}%".format(rate * 100)


def _locator(facts, name, default):
    src = _fact(facts, name).get("source") or {}
    return src.get("locator") or default


# ---------------------------------------------------------------- calculations

def _permanent_need(facts):
    bal = _num(facts, "construction_line_balance")
    rate = _num(facts, "construction_line_rate")
    late = _num(facts, "months_late")
    cont = _num(facts, "contingency_remaining")
    base_status = _combine(_status(facts, n) for n in
                           ("construction_line_balance", "construction_line_rate", "months_late"))
    out = {"value": None, "status": "unknown", "formula": PERMANENT_FORMULA, "upper_bound": False}
    if bal is None or rate is None or late is None:
        out["note"] = "Unknown: construction line balance, rate or months late is missing"
        return out, None
    carry = bal * rate / 12.0 * late
    if cont is None:
        raw = max(0.0, carry)
        out["status"] = base_status
        out["upper_bound"] = True
        out["note"] = "Upper bound: contingency_remaining unknown, treated as 0"
    else:
        raw = max(0.0, carry - cont)
        out["status"] = _combine([base_status, _status(facts, "contingency_remaining")])
    out["value"] = _money(raw)
    return out, raw


def _interest(principal, rate, months):
    if principal is None or rate is None or months is None:
        return None
    return principal * rate * months / 12.0


# ---------------------------------------------------------------- main entry

def evaluate(case, scenario):
    """Pure function: no I/O, no clock, no network. Does not mutate its inputs."""
    scenario = scenario or {}
    facts = copy.deepcopy(case.get("facts") or {})
    overrides = scenario.get("overrides") or {}
    for name, f in overrides.items():
        facts[name] = copy.deepcopy(f)
    label = scenario.get("label") or HISTORICAL_LABEL
    is_what_if = bool(overrides) or label != HISTORICAL_LABEL

    # Needs
    permanent, perm_raw = _permanent_need(facts)
    temp_raw = _num(facts, "city_holdback")
    case_facts = case.get("facts") or {}
    # What-if overrides carry no source; keep the documented section number from the case.
    release_loc = _locator(facts, "holdback_release_condition", "") or _locator(case_facts, "holdback_release_condition", "")
    temporary = {
        "value": _money(temp_raw),
        "status": _status(facts, "city_holdback"),
        "repaid_from": "City final disbursement" + (" after %s conditions" % release_loc if release_loc else ""),
    }

    months = _num(facts, "months_until_release")
    rate_a = _num(facts, "existing_line_rate")
    rate_b = _num(facts, "foundation_advance_rate")
    int_a = _interest(temp_raw, rate_a, months)
    int_b = _interest(temp_raw, rate_b, months)
    int_a_status = _combine(_status(facts, n) for n in ("city_holdback", "existing_line_rate", "months_until_release"))
    int_b_status = _combine(_status(facts, n) for n in ("city_holdback", "foundation_advance_rate", "months_until_release"))

    deal_b = _num(facts, "foundation_deal_cost")
    gross = None if (int_a is None or int_b is None) else int_a - int_b
    net = None if (gross is None or deal_b is None) else gross - deal_b
    savings_status = _combine([int_a_status, int_b_status, _status(facts, "foundation_deal_cost")])

    # Option A feasibility
    line = _fact(facts, "existing_line_available")
    room = _num(facts, "existing_line_available")
    verified = line.get("verified_current") is True
    blockers_a = []
    if room is None:
        feas_a = "unknown"
        blockers_a.append("Existing line room unknown")
    elif not verified:
        feas_a = "unknown"
        when = line.get("as_of")
        blockers_a.append("Existing line room not verified today (last public: %s%s)"
                          % (_usd(room), " on " + when if when else ""))
    elif temp_raw is None:
        feas_a = "unknown"
        blockers_a.append("Temporary need unknown, so line room can't be checked")
    elif room >= temp_raw:
        feas_a = "yes"
    else:
        feas_a = "no"
        blockers_a.append("Existing line room %s is less than the %s timing gap" % (_usd(room), _usd(temp_raw)))

    # Option B feasibility
    consent_loc = _locator(facts, "assignment_consent", "") or _locator(case_facts, "assignment_consent", "")
    consent_name = "City consent to assign" + (" (%s)" % consent_loc if consent_loc else "")
    willing = _bool(facts, "foundation_willing")
    consent = _bool(facts, "assignment_consent")
    blockers_b = []
    if willing is None:
        blockers_b.append("Foundation willingness unknown")
    elif willing is False:
        blockers_b.append("Foundation not willing to advance")
    if consent is None:
        blockers_b.append(consent_name + " unknown")
    elif consent is False:
        blockers_b.append(consent_name + " refused")
    if deal_b is None:
        blockers_b.append("Deal cost unknown")
    if willing is False or consent is False:
        feas_b = "no"
    elif willing is True and consent is True:
        feas_b = "yes"
    else:
        feas_b = "unknown"

    gift = {"provider": "Foundation gift", "amount": _money(perm_raw), "repayable": False}
    options = [
        {
            "id": OPTION_A, "label": "Ordinary gift + existing credit",
            "money": [dict(gift), {"provider": "Existing line (%s)" % _pct(rate_a), "amount": _money(temp_raw),
                                   "repayable": True, "repaid_from": "City final disbursement"}],
            "permanent_gap_reduction": _money(perm_raw), "temporary_cash": _money(temp_raw),
            "interest_cost": _money(int_a), "interest_cost_status": int_a_status,
            "deal_cost": 0, "feasible": feas_a, "blockers": blockers_a,
        },
        {
            "id": OPTION_B, "label": "Gift + foundation advance",
            "money": [dict(gift), {"provider": "Foundation advance (%s)" % _pct(rate_b), "amount": _money(temp_raw),
                                   "repayable": True, "repaid_from": "City final disbursement"}],
            "permanent_gap_reduction": _money(perm_raw), "temporary_cash": _money(temp_raw),
            "interest_cost": _money(int_b), "interest_cost_status": int_b_status,
            "deal_cost": _money(deal_b), "feasible": feas_b, "blockers": blockers_b,
        },
    ]

    # Verdict (contracts/README.md)
    b_better = feas_b == "yes" and net is not None and net > 0
    if feas_b == "yes" and (net is not None and net > 0 or feas_a == "no"):
        verdict = OPTION_B
    elif feas_a == "yes" and not b_better:
        verdict = OPTION_A
    elif feas_a == "no" and feas_b == "no":
        verdict = "no_bridge"
    else:
        verdict = "conditional"

    recommendation = _recommendation(verdict, permanent, temp_raw, gross, net, feas_a, feas_b,
                                     willing, consent, deal_b, consent_loc)

    assumptions = [n for n in facts if _status(facts, n) == "assumption"]
    unknowns = [n for n in facts if _status(facts, n) == "unknown"]

    return {
        "contract_version": "1",
        "case_id": case.get("case_id"),
        "scenario": label,
        "is_what_if": is_what_if,
        "permanent_need": permanent,
        "temporary_need": temporary,
        "options": options,
        "advance_savings": {"gross": _money(gross), "deal_cost": _money(deal_b), "net": _money(net),
                            "break_even_deal_cost": _money(gross)},
        "advance_savings_status": savings_status,
        "recommendation": recommendation,
        "evidence_needed": _evidence_needed(facts, consent_loc),
        "assumptions": assumptions,
        "unknowns": unknowns,
    }


def _recommendation(verdict, permanent, temp_raw, gross, net, feas_a, feas_b,
                    willing, consent, deal_b, consent_loc):
    pn = permanent["value"]
    gift_txt = ("Ask the foundation for a gift of up to %s (upper bound)." % _usd(pn)) if permanent.get("upper_bound") \
        else ("Ask the foundation for a %s gift." % _usd(pn))
    if pn is None:
        gift_txt = "The permanent gift amount is unknown until the missing inputs are found."
    gap = _usd(temp_raw)
    sec = consent_loc or "the grant agreement"
    conditions = []

    if verdict == OPTION_A:
        text = ("%s Carry the %s timing gap on the existing line; repay it from the city's final disbursement."
                % (gift_txt, gap))
        if feas_b == "yes" and net is None:
            conditions.append("Foundation advance deal cost unknown; it beats the line only if below %s" % _usd(gross))
    elif verdict == OPTION_B:
        why = ("saves %s after deal costs" % _usd(net)) if (net is not None and net > 0) \
            else "the existing line can't carry it"
        text = ("%s Take the foundation advance for the %s timing gap (%s); repay it from the city's final "
                "disbursement." % (gift_txt, gap, why))
    elif verdict == "no_bridge":
        text = ("%s Neither the existing line nor a foundation advance can carry the %s timing gap. "
                "Another bridge source is needed." % (gift_txt, gap))
    else:
        if feas_a == "no":
            text = ("%s The existing line can't carry the %s timing gap, so a foundation advance is needed "
                    "if it can be confirmed." % (gift_txt, gap))
        else:
            text = ("%s Carry the %s timing gap on the existing line unless a foundation advance is offered with "
                    "all-in costs below %s and repayment from the city's final disbursement is permitted."
                    % (gift_txt, gap, _usd(gross)))
        if feas_a == "unknown":
            conditions.append("Confirm existing line room >= %s" % gap)
        if willing is not True:
            conditions.append("Foundation willing and terms in writing")
        if consent is not True:
            conditions.append("City consent under %s or the foundation accepts the nonprofit's unsecured promise" % sec)
        if deal_b is None:
            conditions.append("Deal cost < %s" % _usd(gross))
    return {"verdict": verdict, "text": text, "conditions": conditions}


_EVIDENCE = [
    # (label, fact names: listed if any is unknown/assumption, or line room not verified)
    ("Existing line room today", ["existing_line_available"]),
    ("Contingency remaining", ["contingency_remaining"]),
    ("Foundation willingness and terms", ["foundation_willing", "foundation_deal_cost", "foundation_advance_rate"]),
    ("City consent to assign", ["assignment_consent"]),
    ("Months until the city releases the holdback", ["months_until_release"]),
    ("Months of delay versus the budgeted sales date", ["months_late"]),
    ("Construction line balance and rate today", ["construction_line_balance", "construction_line_rate"]),
    ("City holdback amount", ["city_holdback"]),
    ("Existing line rate", ["existing_line_rate"]),
]


def _evidence_needed(facts, consent_loc):
    out = []
    for label, names in _EVIDENCE:
        need = any(_status(facts, n) != "sourced" for n in names)
        if "existing_line_available" in names and _fact(facts, "existing_line_available").get("verified_current") is not True:
            need = True
        if need:
            if label == "City consent to assign" and consent_loc:
                label = "City %s consent" % consent_loc
            out.append(label)
    return out
