# Hassan: status

Owned by Hassan only, so it never conflicts. Newest entry first. Update after every meaningful step
(your Claude should do this before each commit). Teammates and their Claudes read this to know
what you are doing.

## Now
- Working on: _nothing yet_
- Branch:
- Files I'm touching:

## Log
- 13:05 extract/extract_case.py + extract/prompt.md. Sends one document's text + prompt to Claude, writes
  CANDIDATE facts (never into data/cases/). Every quote must appear verbatim in the document and be <=15
  words, else the fact is downgraded to unknown; conflicts become unknown. Verified offline: --dry-run,
  missing-key error, refusal to write into data/cases/, and the quote checks on the real FY2026-27 Q1 text
  (a fake $9,999,999 is caught). NOT verified: a live API call (no key on this machine).
- 13:00 washington.json on the merged engine: check_contract PASS on example and on washington; historical
  verdict conditional; permanent need $150,211 (assumption, upper bound); temporary need $220,000 (sourced).
