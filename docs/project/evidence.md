# Evidence: Washington Avenue case (`data/cases/washington.json`)

Owner: Hassan. Every fact in the case file, its quote (15 words or fewer), where it is, and whether
Hassan read it in the source document. Checked 2026-11-07.

**Sources**
- **AUDIT**: Habitat OC FY2025 audited financial statements (report dated January 26, 2026).
  https://habitatoc.org/wp-content/uploads/2026/02/Habitat-for-Humanity-of-OC-Inc.-HFHOC-FS-Audit-Report-2025-Final-1.pdf
- **Q1-27**: Santa Ana Housing Division Quarterly Report FY2026-27 Q1 (July to Sept 2026; PDF created Nov 3, 2026). Newest published report.
  https://santa-ana.gov/documents/housing-division-quarterly-report-fy-2026-27-q1/
- **Q4-26**: Santa Ana Housing Division Quarterly Report FY2025-26 Q4 (used for comparison only).
  https://santa-ana.gov/documents/housing-division-quarterly-report-fy-2025-26-q4-2/
- **GRANT**: Conditional Grant Agreement, Exhibit 2 to Item 12, Santa Ana City Council, July 16, 2024 (117 pages):
  https://santa-ana.primegov.com/api/compilemeetingattachmenthistory/historyattachment/?historyId=882d302a-6ca1-4d19-9ae5-2443041228db
  (meeting page: https://santa-ana.primegov.com/Portal/Meeting?meetingTemplateId=22247)
- **NEWS**: New Santa Ana, May 20, 2024.

| Fact | Value | Quote (≤15 words) | Where | Verified by Hassan |
|---|---|---|---|---|
| construction_line_balance | $2,253,168 (at 2025-06-30) | "requires interest-only payments until maturity. $ 2,253,168" | AUDIT Note 7, printed p.19 | ✅ |
| construction_line_rate | 5.00% | "The revolving line of credit carries an interest rate of 5.00%" | AUDIT Note 7, printed p.19 | ✅ |
| construction_line_maturity | May 2026 | "renewed its construction line of credit extending the maturity to May 2026" | AUDIT Note 7, printed p.19 | ✅ |
| existing_line_rate | 4.50% | "maximum loan commitment amount is $1,100,000 with interest of 4.50% per annum" | AUDIT Note 7, printed p.19 | ✅ |
| existing_line_available | $825,000 (derived: $1,100,000 − $275,000, at 2025-06-30) | "the Organization initially drawn $275,000" | AUDIT Note 7, printed p.19 | ✅ (both inputs read; room today unknown) |
| city_holdback | $220,000 still committed (at 2026-09-30) | "Washington Avenue $220,000 6 1921 W. Washington Ave. (in progress)" | Q1-27 Table 9, PDF p.8 | ✅ |
| city_holdback (second place) | ($220,000) | "1921 W. Washington Project Pre-Commitment" | Q1-27 Available Funds, PDF p.12 | ✅ |
| city_funds_expended | $1,980,000 (at 2026-09-30) | "Washington Avenue $1,980,000 6 1921 W. Washington Ave. (in progress)" | Q1-27 Table 8, PDF p.8 | ✅ |
| city_grant_total | $2,200,000 | "City Funds Inclusionary Housing Funds ($2,200,000)" | Q1-27 project update, PDF p.11 | ✅ |
| scheduled_construction_completion | Oct 2026 (schedule) | "Oct 26 Construction completion of all six homes" | Q1-27 Exhibit 2, PDF p.16 | ✅ |
| scheduled_move_in | Nov 2026 (schedule) | "Nov 26 New first-time homeowner families move in" | Q1-27 Exhibit 2, PDF p.16 | ✅ |
| months_late | 16 (ASSUMPTION) | "Home Sales Complete 06/25/25 06/27/25" → "Oct 26 Construction completion of all six homes" | GRANT Exhibit B schedule, PDF p.40 + Q1-27 Exhibit 2 | ✅ both ends read |
| months_until_release | 6 (ASSUMPTION) | none. Schedule suggests Nov 2026 move-in; closings not public | Q1-27 Exhibit 2 | n/a (assumption) |
| building_permit_issued | unknown: sources disagree | p.11: "Building permits were issued on October 1, 2026" vs p.16: "Oct 25 Building permit issued" | Q1-27 PDF p.11 vs p.16 | ✅ both read; conflict unresolved |
| holdback_release_condition | Complete + CofO + buyers closed escrow + **lien-free** | "Final Disbursement Conditions Precedent"; "(d) Lien Free" | GRANT Sec. 4.2, PDF p.8 | ✅ |
| (release timing) | City pays within 21 days of conditions | "the City shall disburse the Inclusionary Grant within twenty one (21) days" | GRANT Sec. 4.3, PDF p.8 | ✅ |
| assignment_consent | unknown (consent required) | "only with the prior written consent of the City Project Manager" | GRANT Sec. 7.13, PDF p.13 | ✅ |
| contingency_remaining | unknown ($477,762 budgeted) | "Project Contingency 477,762 79,627" | GRANT Exhibit C, PDF p.41 | ✅ budget read; remaining not public |
| planned_total_cost | $4,491,382 ($748,564/home) | "Total Costs 4,491,382 748,564" | GRANT Exhibit C, PDF p.41 | ✅ |
| planned_unit_sales | $1,352,400 (avg $225,400) | "Unit Sales 1,352,400 225,400" | GRANT Exhibit C, PDF p.41 | ✅ |
| planned_habitat_fundraising | $938,982 ($156,497/home) | "Habitat Fundraising 938,982 156,497" | GRANT Exhibit C, PDF p.41 | ✅ |
| planned_construction_loan | $2,252,000 | "Construction Loan 2,252,000 375,333" | GRANT Exhibit C, PDF p.41 | ✅ |
| past_sponsorship_excluded | $125,000 (a minimum) | "The event raised more than $125,000" | NEWS, May 20, 2024 | ✅ |
| foundation_advance_rate, foundation_deal_cost, foundation_willing | 0% ASSUMPTION / unknown / unknown | none | none | n/a |

## What changed from the team example (tell Jawad)

1. **months_late 11 → 16.** The newest city schedule moves completion of all six homes to Oct 2026,
   from May 2026. Same method as before. With the v1 rule this raises the permanent need from
   $103,270 to $150,211 (2,253,168 × 0.05 / 12 × 16). It is still an ASSUMPTION and an upper bound,
   because contingency_remaining is unknown.
2. **city_holdback is still $220,000 unpaid as of Sept 30, 2026.** The source is now the newest
   report (FY2026-27 Q1), not FY2025-26 Q1.
3. **The construction line's maturity (May 2026) has passed.** Its balance is marked
   `verified_current: false`.
4. **The grant's release condition (Sec. 4.2) includes a lien-free test** the example left out: 35 days after a
   recorded Notice of Completion, or 95 days after completion, with no liens; then the City pays within 21 days (Sec. 4.3).
5. **The approved budget is the real $0 equation** (Exhibit C): $4,491,382 cost = $1,352,400 family sales +
   $2,200,000 city subsidy + $938,982 Habitat fundraising. Added as `planned_*` facts (planned, not actual).
6. **The same city report contradicts itself on the building permit date** (Oct 1, 2026 on p.11 vs
   Oct 2025 in Exhibit 2). This is shown as unknown, not resolved.

No personal information: the reports mention "six (6) families" but give no names, and none are recorded here.

## For the README: "Sources and assumptions" table (ready to paste)

| Item | Source or assumption | Date checked |
|---|---|---|
| Construction line: $2,253,168 drawn at 5.00%, interest-only, maturity extended to May 2026 | Habitat OC FY2025 audited financial statements, Note 7, printed p.19 (report dated Jan 26, 2026): https://habitatoc.org/wp-content/uploads/2026/02/Habitat-for-Humanity-of-OC-Inc.-HFHOC-FS-Audit-Report-2025-Final-1.pdf | 2026-11-07 |
| Existing line: $1,100,000 commitment at 4.50%, $275,000 drawn (room $825,000 at 2025-06-30; today unknown) | Same audit, Note 7, printed p.19 | 2026-11-07 |
| City holdback $220,000 still committed, not paid (at 2026-09-30); $1,980,000 of $2,200,000 paid | Santa Ana Housing Division Quarterly Report FY2026-27 Q1, Tables 8–9 and p.11–12: https://santa-ana.gov/documents/housing-division-quarterly-report-fy-2026-27-q1/ | 2026-11-07 |
| Completion of all six homes scheduled Oct 2026; move-in scheduled Nov 2026 | Same report, Exhibit 2 (p.16) | 2026-11-07 |
| Building permit date: **sources disagree** (Oct 1, 2026 on p.11 vs Oct 2025 in Exhibit 2) | Same report; shown as unknown | 2026-11-07 |
| Holdback release condition incl. lien-free test (Sec. 4.2), 21-day payment (Sec. 4.3), assignment needs City consent (Sec. 7.13), Jun 2025 planned sales (Exhibit B) | Conditional Grant Agreement, Exhibit 2 to Item 12, Santa Ana City Council, July 16, 2024: https://santa-ana.primegov.com/api/compilemeetingattachmenthistory/historyattachment/?historyId=882d302a-6ca1-4d19-9ae5-2443041228db | 2026-11-07 |
| Approved budget: $4,491,382 cost, $1,352,400 family sales (avg $225,400), $2,200,000 city subsidy, $938,982 Habitat fundraising, $477,762 contingency | Same agreement, Exhibit C Project Budget (PDF p.41). Planned at approval, not actual | 2026-11-07 |
| "More than $125,000" Leaders Build 2024, excluded as already raised | New Santa Ana, May 20, 2024: https://newsantaana.com/habitat-oc-raises-125k-at-the-15th-annual-leaders-build-challenge-in-santa-ana | 2026-11-07 |
| Months late: 16 | **ASSUMPTION**: Jun 2025 planned sales (grant Exhibit C) to Oct 2026 scheduled completion (FY2026-27 Q1 Exhibit 2) | 2026-11-07 |
| Months until the city releases the holdback: 6 | **ASSUMPTION**: the closing dates are not public; the city schedule suggests Nov 2026 move-in | 2026-11-07 |
| Foundation advance rate: 0% | **ASSUMPTION**: a program-related, interest-free advance | n/a |
| Contingency remaining, foundation deal cost, foundation willing, city consent to assignment | **unknown**: not public; the tool shows these as evidence still needed | n/a |
| Candidate facts from `extract/extract_case.py` | Claude output, verified against the document quote by quote by a person before use | n/a |
