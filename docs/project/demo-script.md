# Live demo script (finalists, 3:00 PM)

**Setup (before going on stage):** `bash scripts/run_demo.sh`, open http://localhost:8501, case =
`data/cases/washington.json`, all sidebar inputs on their defaults (HISTORICAL badge showing).
Fallback if `main` breaks: `git worktree add ../demo-stable demo-2`, then run the demo from there.
Last resort: play the uploaded video.

1. **User and problem (20 s).** "A nonprofit finance lead has one shortfall number. The facts that
   decide how to close it are spread across an audit, a city report and a council agreement."
2. **Needs (30 s).** Permanent need $150,211 (upper bound: contingency unknown) vs temporary need
   $220,000 (the city pays it only after completion, all six closings and a lien-free period, §4.2).
   Point at the source chips.
3. **Options (30 s).** A: gift + existing 4.50% line, $4,950 interest. B: gift + foundation advance,
   $0 interest but deal cost unknown, and the city must consent (§7.13). Gifts and loans never summed.
4. **What-if (30 s).** Foundation willing = yes, city consents = yes, deal cost $2,000 → WHAT-IF badge,
   verdict flips to the advance, net savings $2,950. Then set the foundation back to "unknown" and
   "Existing line room" to "verified: has room" → verdict becomes gift + existing credit.
5. **Proposal (20 s).** Click Draft proposal; read the evidence still needed.
6. **The finding (15 s).** "A buyer rate buydown doesn't shrink this gap: the city prices homes at the
   prevailing market rate (§1.1.34)."
7. **Scale (15 s).** "Claude pulls the same facts from the next project's documents, with every
   quote checked against the source."

Be straight: the permanent need is an upper bound, the timing months are assumptions, and the
extractor's live run is the only part not demonstrated today.
