# Team: Mykonos 2027

Room: **Eric Li Classroom, Room 1128, 1st floor** (Merage SB1). Lane: **3 Fund it**.
Change this file by pull request (owner: Jawad). Process: [`docs/COLLABORATION.md`](docs/COLLABORATION.md).
Four people; this supersedes the earlier three-person notes.

## People, roles and exclusive write paths

| Name | GitHub | Workstream | Owns (only they edit) | Branch |
|---|---|---|---|---|
| Jawad | jasad949 | Integration, contracts, dependencies, final README, submission | `contracts/`, `requirements.txt`, `scripts/`, `README.md`, `CLAUDE.md`, `TEAM.md`, `NOTES.md`, `.github/`, `.claude/`, `status/jawad.md` | `jawad/<task>` |
| Hassan | hasan-yaghmour | Public evidence and Claude extraction | `data/`, `extract/`, `docs/project/evidence.md`, `status/hassan.md` | `hassan/evidence` |
| Omar | omard05 | Financial logic and tests | `engine/`, `tests/`, `status/omar.md` | `omar/engine` |
| _Member 4 (name TBD)_ | _TBD_ | UI, video and live demo | `app/`, `assets/`, `docs/project/demo-script.md`, `docs/project/video-script.md`, `status/<member4>.md` | `<member4>/ui` |

Swap people between workstreams if skills fit better; the paths stay with the workstream.

## Interface contract

- Folder: [`contracts/`](contracts/README.md) (owner: Jawad). Case file → `engine.proposal.evaluate(case, scenario)` → result.
- Contract test: `python3 scripts/check_contract.py`
- Integrated demo: `bash scripts/run_demo.sh`

## Checkpoints (D = 2:30 PM PT; submit by 2:20)

| Time | Checkpoint | Owner | Done when |
|---|---|---|---|
| 12:20 | Contracts on `main`, prompts distributed | Jawad | Every teammate has a branch and an issue |
| 12:32 | End to end on the shared example | Jawad (merges Omar's minimal engine + Member 4's static UI) | `run_demo.sh` shows engine output; `check_contract` PASS |
| 12:50 | Real sourced case end to end; tag `demo-1` | Hassan → Jawad | `data/cases/washington.json` drives the screen |
| 1:35 | Complete engine and UI PRs | Omar, Member 4 | What-ifs, verdict and proposal draft work |
| 1:40 | **Feature freeze**; tag `demo-2` | Jawad | Demo-path fixes only |
| 1:40–2:05 | Video recorded and uploaded | Member 4 + Jawad | 30–60 s, made with Claude |
| 2:05–2:15 | README, sources table, repo checked signed out | Jawad (+ Hassan's sources) | Follows `templates/TEAM-README.md` |
| 2:20 | Submitted on the hub | Jawad | Confirmation shown |

**Cut first if behind:** (1) live Claude re-extraction in the app, (2) Claude-written proposal text
(keep the template), (3) what-if inputs beyond line room, consent and deal cost, (4) styling.
**Never cut:** the dated historical case, gifts kept separate from loans, sources and unknowns on screen,
the conditional recommendation.
