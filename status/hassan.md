# Hassan: status

Owned by Hassan only, so it never conflicts. Newest entry first. Update after every meaningful step
(your Claude should do this before each commit). Teammates and their Claudes read this to know
what you are doing.

## Now
- Working on: waiting on review of PR #9 (case file) and the extraction PR
- Branch: hassan/evidence (PR #9), hassan/extract
- Files I'm touching: data/cases/washington.json, docs/project/evidence.md, extract/, status/hassan.md

## Log
- 13:05 extract/extract_case.py + extract/prompt.md. Sends one document's text + prompt to Claude, writes
  CANDIDATE facts (never into data/cases/). Every quote must appear verbatim in the document and be <=15
  words, else the fact is downgraded to unknown; conflicts become unknown. Verified offline: --dry-run,
  missing-key error, refusal to write into data/cases/, and the quote checks on the real FY2026-27 Q1 text
  (a fake $9,999,999 is caught). NOT verified: a live API call (no key on this machine).
- 13:00 washington.json on the merged engine: check_contract PASS on example and on washington; historical
  verdict conditional; permanent need $150,211 (assumption, upper bound); temporary need $220,000 (sourced).
- 12:50 data/cases/washington.json written. `python3 scripts/check_contract.py --case data/cases/washington.json`
  → Schema PASS. Read the newest Santa Ana report (FY2026-27 Q1, Sept 30, 2026)
  and the FY2025 audit Note 7 myself.
  **Number change for Jawad/Omar:** months_late 11 → 16 (city schedule now says all six homes complete
  Oct 2026, was May 2026). Permanent need under v1 rules: $103,270 → $150,211. Still ASSUMPTION.
  $220,000 holdback still unpaid at 2026-09-30. Construction line maturity (May 2026) has passed.
  City report contradicts itself on the permit date (shown as unknown).
  Not verified by me yet: council packet facts (Sec. 4.2, 7.13, Exhibit C) and the $125k news item.
