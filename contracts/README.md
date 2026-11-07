# Shared contract (v1). Owner: Jawad

Changes to this folder go through Jawad in their own PR. Everyone else builds against these files.

```
extraction (Hassan)  --data/cases/<case>.json-->  engine (Omar)  --result dict-->  UI (Member 4)
                       shape = example_case.json   evaluate(case, scenario)   shape = example_result.json
```

- Run the integrated demo: `bash scripts/run_demo.sh`
- Check the contract: `python3 scripts/check_contract.py` (engine output vs `example_result.json`),
  or `python3 scripts/check_contract.py --case data/cases/washington.json` (schema check of a case file)
- Python 3.9 compatible. The engine uses the standard library only.

## 1. Case file (extraction → engine)

`{contract_version: "1", case_id, title, as_of: "YYYY-MM-DD", facts: {name: Fact}}`

A **Fact** is:

| Field | Meaning |
|---|---|
| `value` | number, string, boolean, or `null` when unknown |
| `status` | `"sourced"` (from a public document), `"assumption"` (we chose it; label ASSUMPTION everywhere), or `"unknown"` (value must be `null`) |
| `source` | required when `status` is `"sourced"`: `{doc, locator, url, date}` |
| `as_of` | optional date the value was true |
| `verified_current` | optional boolean; `false` means true once but not confirmed today |
| `note` | optional plain-language note |

Required fact names (v1): `construction_line_balance`, `construction_line_rate`, `months_late`,
`contingency_remaining`, `city_holdback`, `holdback_release_condition`, `months_until_release`,
`existing_line_rate`, `existing_line_available`, `foundation_advance_rate`, `foundation_deal_cost`,
`foundation_willing`, `assignment_consent`, `past_sponsorship_excluded`. Extra facts are allowed.

## 2. Scenario (UI → engine)

`{label: str, overrides: {fact_name: Fact}}`. The engine replaces the named facts. An empty
`overrides` with label `"Historical (as documented)"` is the dated case; anything else is a
**What-if** (`is_what_if: true`). Examples: `example_scenarios.json`.

## 3. Result (engine → UI)

`engine.proposal.evaluate(case: dict, scenario: dict) -> dict`, shaped like `example_result.json`.
Money is rounded to whole dollars at output only. `null` means unknown, never 0.

## Engine rules (v1; Omar may refine inside engine/, keeping the result shape)

- `monthly_carry = construction_line_balance * construction_line_rate / 12`
- `permanent_need = max(0, monthly_carry * months_late - contingency_remaining)`; if contingency is unknown,
  treat it as 0 and label the value an upper bound
- `temporary_need = city_holdback` (repaid from the city's final disbursement)
- `interest_cost(rate) = temporary_need * rate * months_until_release / 12`
- `advance_savings.gross = interest(existing) - interest(advance)`; `net = gross - deal_cost`
  (`null` if the deal cost is unknown); `break_even_deal_cost = gross`
- Status propagation: any unknown input makes an output `unknown` (or an upper bound, as above);
  otherwise any assumption input makes it `assumption`; otherwise `sourced`
- Option A feasible: `yes` if `existing_line_available` is verified current and covers the temporary need;
  `no` if verified current and too small; else `unknown`
- Option B feasible: `yes` only if `foundation_willing` and `assignment_consent` are both true; `no` if
  either is false; else `unknown`
- Verdict: A if A=`yes` and B isn't better after costs; B if B=`yes` and net > 0, or if A=`no` and
  B=`yes`; `no_bridge` if both are `no`; otherwise `conditional`
- Never add gift money and repayable principal into one total

## Expected verdicts for example_scenarios.json

| Scenario | Verdict |
|---|---|
| Historical (as documented) | `conditional` (exactly `example_result.json`) |
| What-if: existing line has verified room | `gift_plus_existing_credit` |
| What-if: existing line is full | `conditional` (B must be confirmed) |
| What-if: foundation says yes, city consents, $2,000 deal cost | `gift_plus_foundation_advance` (net savings $2,950) |
