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
- **PACKET**: Santa Ana City Council packet, July 16, 2024 (Conditional Grant Agreement). PDF held by Jawad.
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
| months_late | 16 (ASSUMPTION) | Derived: Jun 2025 planned sales → Oct 2026 scheduled completion | PACKET Exhibit C (Jun 2025, not re-read) + Q1-27 Exhibit 2 | ⚠️ partly: Oct 2026 read; Jun 2025 from team example |
| months_until_release | 6 (ASSUMPTION) | none. Schedule suggests Nov 2026 move-in; closings not public | Q1-27 Exhibit 2 | n/a (assumption) |
| building_permit_issued | unknown: sources disagree | p.11: "Building permits were issued on October 1, 2026" vs p.16: "Oct 25 Building permit issued" | Q1-27 PDF p.11 vs p.16 | ✅ both read; conflict unresolved |
| holdback_release_condition | CofO + all six buyers closed escrow | (from team example) | PACKET Sec. 4.2 | ❌ not yet: need the PDF from Jawad |
| assignment_consent | unknown | (from team example) | PACKET Sec. 7.13 | ❌ not yet |
| contingency_remaining | unknown ($477,762 budgeted) | (from team example) | PACKET Exhibit C | ❌ not yet |
| past_sponsorship_excluded | $125,000 | (from team example) | NEWS, May 20, 2024 | ❌ not yet |
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
4. **The same city report contradicts itself on the building permit date** (Oct 1, 2026 on p.11 vs
   Oct 2025 in Exhibit 2). This is shown as unknown, not resolved.

No personal information: the reports mention "six (6) families" but give no names, and none are recorded here.
