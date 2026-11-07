# Nabheel — UI, video and demo

## Now — 2026-11-07

- Branch: `nabheel/ui`; task: #17 (continues #5).
- Own files: `app/`, `docs/project/demo-script.md`, `docs/project/video-script.md`, this status.
- Built: three-column historical Washington screen, source links/dates and status chips;
  all requested sidebar controls mapped to scenario.overrides; live engine evaluation;
  static contract fixture preview; deterministic printable HTML proposal with separated gift
  and repayable principal; stale drafts cleared when scenario changes; demo and video scripts.
- No requirements, contracts, engine, evidence, or other teammate-owned files changed.

## Verified

- `python3 scripts/check_contract.py`: PASS.
- `python3 scripts/check_contract.py --case data/cases/washington.json`: PASS.
- `python3 -m unittest discover -s tests`: 13 passed.
- Streamlit AppTest: historical $150,211 assumption upper bound / $220,000 sourced;
  what-if foundation/city yes and $2,000 cost => $2,950 assumption savings;
  foundation rate 2% => $750 assumption savings; old proposal invalidated; historical reset;
  static fixture loads $103,270 directly. No exceptions after fixing HTML percent escaping.
- Pinned Streamlit 1.39.0: six committed UI regression tests pass; after merging latest main,
  14 engine tests pass. Both contract checks pass.
- `bash scripts/run_demo.sh` installed pinned dependencies in a new venv. Headless launch passes
  (noninteractive first run otherwise prompts for email). Real Chrome interactions passed for
  historical badge, sources, what-if rate changes, draft generation and stale-draft clearing.
- Printed historical and what-if HTML via Chrome: both one US-letter page; desktop screenshot
  inspected with all primary content and draft button visible.
- Merged main 3b81bd1: preserved negative-currency formatting and effective-fact display fixes,
  Omar's consent locator fix, and incorporated Jawad's Claude-assisted storyboards.

## Remaining / handoff

- CLI authenticated as nabkaz-bot using writable temporary GH_CONFIG_DIR. Issue #17 created.
- Pulled main c292108, including Hassan's newly verified packet conditions and evidence.
- Draft PR #18: https://github.com/jasad949/mykonosclaude2027/pull/18. Local implementation is at
  `/private/tmp/mykonosclaude2027` (provided workspace path was absent on execution host).
- Recording with Jawad and upload remain human handoff steps; not yet done.
- Have Jawad/Claude review storyboard for the event's Claude-help requirement.
