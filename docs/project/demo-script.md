# Live demo — Nabheel

## Run and reset

From a fresh clone, run `bash scripts/run_demo.sh`. No API key is needed. Open the local URL.
Keep **Contract fixture preview** off and **Explore a what-if** off. The fixture preview reads
`contracts/example_result.json` directly and is explicitly an older saved example, not the current case.
The normal path evaluates `data/cases/washington.json` with `engine.proposal.evaluate(case, scenario)`.

## Presenter path

1. **User and problem:** “A nonprofit finance lead needs to distinguish a permanent fundraising
   need from money that is only needed until the city pays.” Show the dated Washington Avenue case.
2. **Evidence:** point to $150,211 **ASSUMPTION, upper bound** and $220,000 **SOURCED** temporary
   principal. The former models delay interest, not the full project budget. Open Inputs, sources &
   dates briefly: audit balance is historical; current loan status and contingency are unverified.
3. **Comparison:** show A and B. Each has a separate gift row and repayable principal row.
   Historical net savings is **UNKNOWN**, because deal cost is unknown. Neither financing offer
   is confirmed. The evidence list remains red.
4. **What-if:** turn on Explore a what-if; set foundation willing Yes, city consent Yes, Set deal
   cost checked, $2,000 **ASSUMPTION**. At the existing assumed zero foundation rate and six-month
   release period, the model shows $2,950 **ASSUMPTION** net savings. Point at the WHAT-IF badge.
   Set the foundation rate to 2% **ASSUMPTION**: savings change to $750 **ASSUMPTION**.
5. **Result:** click Draft proposal. The one-page draft preserves gifts versus repayable principal,
   shows costs, conditional evidence and source links. Download the HTML and use its Print / Save
   as PDF button if needed. Nothing is sent. Changing inputs clears the previous draft.

## Alternate feasibility demonstration

In what-if mode, Line room verified? Yes with $0 **ASSUMPTION** makes A infeasible. Foundation
willing No makes B infeasible; the screen says neither bridge is feasible. Set Line room verified?
Unknown to show that missing evidence is not equivalent to no capacity. Turn off Explore a what-if
to restore the dated case regardless of widget values.

## Claims and limits

- Public case evidence is real; assumptions, offers and scenario “verification” are hypothetical.
- Simple interest on a flat balance; no implied lender commitment or legal consent.
- The construction loan maturity has passed in the public evidence; renewal must be checked.
- Council-packet facts were verified by Hassan in the latest main update. Release also requires
  lien-free completion; actual consent and closing dates remain unknown.
- Prior sponsorship is excluded from new money, visible under Inputs, sources & dates.
- Claude's extraction pipeline is a separate team component. This screen and proposal template
  make no model calls. Do not claim this UI was built with Claude: Nabheel used ChatGPT/Codex.
- Future scale: apply the same reviewed case contract to another project; do not claim that has
  already been tested across a portfolio.

## Handoff

Nabheel drives the screen; Jawad records and submits. Feature freeze 1:40 PM PT. Recording window
1:40–2:05 PM PT. Submission deadline 2:30 PM PT. Finalist live demo is 3:00 PM PT.
If launch fails, use the verified local checkout; disclose any fixture fallback clearly.
