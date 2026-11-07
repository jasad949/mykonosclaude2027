# Gap-to-Proposal

> For a nonprofit housing finance lead: split a project's funding gap into money that must be
> raised permanently and cash that is only needed until a committed payment arrives, then compare an
> ordinary gift + existing credit with a gift + foundation advance, with every number sourced or
> labelled ASSUMPTION / unknown.

**Team:** Mykonos 2027
**Members:** Jawad, Omar, Hassan, Nabheel
**Lane:** 3 Fund it
**Built at:** Claude Impact Lab: UCI × SoCal Affordable Housing, November 7, 2026

## The real user

A finance lead at a nonprofit that builds affordable ownership homes. Our dated case is Habitat for
Humanity of Orange County's six-home project at 1921 W. Washington Ave, Santa Ana, built entirely from
public documents (we did not interview Habitat staff; nothing here is their view).

**Before:** the shortfall is one fundraising number. The facts that decide how to close it sit in
three places (an audit, a city quarterly report, a council packet), and permanent need is mixed with
timing gaps that will be repaid.

**After:** one screen separates the **permanent need** (upper bound $150,211) from the **temporary
need** ($220,000 the city releases only after every home closes and the property is lien-free),
compares two ways to cover them, and drafts a proposal that says what is still unconfirmed.

## What we built

A Streamlit screen backed by a pure calculation engine and a sourced case file:

- **Needs:** permanent vs temporary, each with its source, ASSUMPTION or unknown chip.
- **Options side by side:** (A) ordinary gift + existing credit line; (B) gift + foundation advance.
  Gifts and repayable principal are always listed separately and never summed. Shows who provides
  each dollar, what is repaid and from what, interest, deal cost, and blockers.
- **What the advance saves:** gross interest saved, net after deal costs, and the break-even deal cost.
- **Recommendation:** `conditional` when evidence is missing, with the evidence still needed.
- **What-if inputs:** existing-line room, months until release, foundation willingness, city consent,
  deal cost, contingency remaining. Changing any input switches the badge from HISTORICAL to WHAT-IF.
- **Draft proposal:** a one-page text draft (not sent anywhere).

**A finding we kept:** a buyer mortgage-rate buydown does *not* shrink this gap. Santa Ana's recorded
Affordable Housing Agreement (§1.1.34) prices each home at the *prevailing market* rate, so a cheaper
partner-bank rate lowers the buyer's payment but not Habitat's price.

**Demo video:** uploaded on the hub
**Live demo:** run locally (below)

## How Claude is used

- **Building it:** four teammates each ran Claude Code in their own checkout against one shared
  contract (`contracts/`), with research, review and integration done with Claude.
- **Inside the tool:** `extract/extract_case.py` sends a public document's text to Claude, which
  returns candidate facts with a quote of 15 words or fewer and a locator. Code then checks every
  quote verbatim against the document and downgrades anything unquoted, over-long or conflicting to
  `unknown`. A person verifies each fact (`docs/project/evidence.md`) before it enters the case file.
- **What a person checks:** every extracted fact, every assumption, and the final proposal.

## Try it

Needs Python 3.9 or newer (tested on 3.9.6 and 3.13).

```bash
git clone https://github.com/jasad949/mykonosclaude2027.git
cd mykonosclaude2027
bash scripts/run_demo.sh            # creates .venv, installs pinned requirements, opens the app
```

Checks:

```bash
python3 scripts/check_contract.py                                   # engine vs expected result
python3 scripts/check_contract.py --case data/cases/washington.json # real case: schema + verdicts
python3 -m unittest discover -s tests                               # engine unit tests
```

The demo needs no API key. Only the optional extractor does: copy `env.example` to `.env` and set
`ANTHROPIC_API_KEY` (never commit it). `--dry-run` runs the extractor without an API call.

## Sources and assumptions

| Item | Source or assumption | Date checked |
|---|---|---|
| Construction line: $2,253,168 drawn at 5.00%, interest-only, maturity extended to May 2026 | [Habitat OC FY2025 audited financial statements](https://habitatoc.org/wp-content/uploads/2026/02/Habitat-for-Humanity-of-OC-Inc.-HFHOC-FS-Audit-Report-2025-Final-1.pdf), Note 7, printed p.19 | 2026-11-07 |
| Existing line: $1,100,000 at 4.50%, $275,000 drawn (room $825,000 at 2025-06-30; today unknown) | Same audit, Note 7 | 2026-11-07 |
| City holdback $220,000 committed, not paid (at 2026-09-30); $1,980,000 of $2,200,000 paid | [Santa Ana Housing Division Quarterly Report FY2026-27 Q1](https://santa-ana.gov/documents/housing-division-quarterly-report-fy-2026-27-q1/), Tables 8–9, pp.11–12 | 2026-11-07 |
| Completion of all six homes scheduled Oct 2026; move-in scheduled Nov 2026 | Same report, Exhibit 2 (p.16) | 2026-11-07 |
| Building permit date: **sources disagree** (Oct 1, 2026 on p.11 vs Oct 2025 in Exhibit 2) | Same report; shown as unknown | 2026-11-07 |
| Release condition incl. lien-free test (§4.2), 21-day payment (§4.3), assignment needs City consent (§7.13), Jun 2025 planned sales (Exhibit B) | [Conditional Grant Agreement, Santa Ana City Council, July 16, 2024](https://santa-ana.primegov.com/api/compilemeetingattachmenthistory/historyattachment/?historyId=882d302a-6ca1-4d19-9ae5-2443041228db) | 2026-11-07 |
| Approved budget: $4,491,382 cost, $1,352,400 family sales, $2,200,000 city subsidy, $938,982 Habitat fundraising, $477,762 contingency | Same agreement, Exhibit C (PDF p.41). Planned at approval, not actual | 2026-11-07 |
| Homes priced at the prevailing market rate (why a buydown doesn't shrink the gap) | Same council packet, Affordable Housing Agreement §1.1.34, §3.3.2 | 2026-11-07 |
| "More than $125,000" from Leaders Build 2024, excluded as already raised | [New Santa Ana, May 20, 2024](https://newsantaana.com/habitat-oc-raises-125k-at-the-15th-annual-leaders-build-challenge-in-santa-ana) (news) | 2026-11-07 |
| Habitat Capital pilot: low-cost, subordinate, unsecured bridge line (background only) | [Habitat for Humanity International newsroom, 2025](https://www.habitat.org/newsroom/2025/habitat-capital-launches-pilot-fund-address-financing-challenges-nonprofit-real) | 2026-11-07 |
| Months late: 16 | **ASSUMPTION**: Jun 2025 planned sales to Oct 2026 scheduled completion | 2026-11-07 |
| Months until the city releases the holdback: 6 | **ASSUMPTION**: closing dates are not public | 2026-11-07 |
| Foundation advance rate: 0% | **ASSUMPTION**: an interest-free program-related advance | n/a |
| Contingency remaining, foundation deal cost, foundation willingness, city consent | **unknown**: not public; shown as evidence still needed | n/a |

Full per-fact quotes and page numbers: [`docs/project/evidence.md`](docs/project/evidence.md).
Every number we made up is labelled ASSUMPTION here and in the tool.

## What is real and what is mocked

| Part | Status |
|---|---|
| Washington case file (`data/cases/washington.json`) | Working: public documents, each fact verified by a person |
| Calculation engine (`engine/`) | Working: 13 unit tests, contract check PASS |
| One-screen app (`app/`) | Working: tested headless and in a browser |
| Claude extractor (`extract/`) | Partly working: dry run and quote checks tested offline; a live API call has not been run by the team yet |
| Foundation advance terms, city consent, current credit-line room | Not real: what-if inputs only, labelled ASSUMPTION |
| Proposal draft | Template text; nothing is sent |

## Where it gets things wrong

- The permanent need is an **upper bound**: it assumes the construction line stayed fully drawn for
  all 16 months and that the contingency is used up. Both are unknown.
- Months late and months until release are assumptions from city schedules, not closing records.
- The existing line's room is from June 30, 2025. Today it is unknown.
- One case, one city. Other cities' agreements may price homes differently.

## Next steps

To use this next month, a finance lead would enter four numbers only they have (line room today,
contingency remaining, closing dates, a foundation's terms) and send the draft. With one more week:
run the extractor on more city reports and agreements so each new project's case file starts
pre-filled, and add a second project to test whether the rules hold beyond Santa Ana.

## Data and privacy

This project uses only public data. It contains no personal information about real tenants, buyers or
residents. It does not file applications or contact any city, lender, foundation or person. It is a
prototype and not financial, legal or lending advice.

## License

MIT, see [LICENSE](LICENSE). Organizer starter material (`docs/`, `lanes/`, `templates/`) is from
[claude-impact-lab-uci](https://github.com/travcjohnson/claude-impact-lab-uci) under its own terms
(MIT / CC0); provenance in [`docs/event/README.md`](docs/event/README.md).
