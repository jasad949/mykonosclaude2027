# CLAUDE.md: Team Mykonos 2027, Claude Impact Lab (UCI × SoCal Affordable Housing)

This repo is the team's **single source of truth**. It holds the organizers' full lane repo, the
event hub, the kickoff slides, our decisions and our running status. Answer from these files
before going to the web. Every teammate's Claude reads this file first.

**Precedence:** organizer instructions given today → the organizers' material (`docs/*.md`,
`lanes/`, `docs/event/`) → the Project facts below → our general notes (`docs/team/`).

## Before you do anything in this repo

1. `git fetch origin` and compare with `origin/main` (`git log --oneline HEAD..origin/main`).
   Teammates push all day; a local copy is stale within the hour.
2. Read `NOTES.md` (status, newest first) and `TEAM.md` (who owns what).
3. If files changed under you, re-read them before editing. Never discard or overwrite changes you
   didn't make. Ask instead.

## The event (verified Nov 7; details in `docs/event/`)

- **Deadline: 2:30 PM PT today.** One submission per team on the hub: public GitHub repo with a
  README following `templates/TEAM-README.md`, a demo video (30 s ideal, 2 min max, *made with
  Claude's help*), and the form. Everything pushed to `main` by 2:30; later commits are flagged.
- **The video picks the finalists.** At 2:30 judges watch every video and pick 10. Only those 10
  demo live (3:00 PM) and get scored. Treat the video as a deliverable, not an afterthought.
- **Scoring:** four equal areas, 1–5 each, ties go to Impact.
  - **Impact:** a nonprofit or city would use it next month to help get homes built.
  - **Works:** live demo on real data, sources shown. Rough and working beats polished.
  - **Scale:** a believable path to the next 100 projects.
  - **Innovation:** a new way to see or solve the problem. Bending the brief is allowed.
  Slides without a working demo do not place.
- **Judges:** Ed Coulson (UCI Center for Real Estate), Michael Imerman (FinTech professor),
  Noah Samuels (Design & Development), Jason Bigman (Anthropic), Travis Johnson (host, wrote the
  brief). Expect scrutiny of real-estate and finance correctness.
- **The problem:** what the family can pay + public subsidies + fundraising − cost to create the
  home = $0. In OC the cost side wins by six figures per home, and land-to-keys takes about four
  years. Lane 1 **Find it** (land), Lane 2 **Clear it** (time), Lane 3 **Fund it** (closing the
  gap). See `docs/background.md` and `lanes/*/README.md`.

## Rules that do not bend (from the organizers' `CLAUDE.md`, verbatim in `docs/event/upstream-CLAUDE.md`)

- **Never invent a statute, number, fee, address or parcel fact.** No made-up section numbers,
  dollar amounts, fee schedules, deadlines, zoning codes, APNs or street addresses. If a source
  doesn't say, the answer is "unknown". Say it plainly.
- **Label assumptions.** A number the team doesn't have gets marked `ASSUMPTION` in the code, the
  UI and the README, with what it's based on.
- **Cite sources.** Every claim about a law, program, rate or dataset carries its source: a URL, a
  section number and the date it was checked. Each lane's slide has its own rule:
  - Find it: cite the law and dataset behind every site.
  - Clear it: cite the statute or city rule behind every step, and show both where they disagree.
  - Fund it: label every assumed number.
- **When sources disagree or look stale, show it.** Don't pick silently. Laws get renumbered (ADU
  law moved from Gov Code 65852.2 to 66310–66342) and income limits get revised mid-year (HCD 2026
  State limits were revised June 23, 2026).
- **No personal information.** Nothing real about a tenant, buyer, resident or applicant. If
  something looks like a real person's personal information, stop, say so, don't process, save or
  commit it, and tell an organizer. Test with made-up people and say they're made up.
- **No scraping at volume.** Use public or provided data only. Prefer downloads, documented APIs
  and cached copies. Respect each source's terms. No private plans or blueprints.
- **No secrets in git.** Keys go in `.env` (ignored). `env.example` lists names only.
- **Prototype only.** Never file an application, send an email, text or letter, or change any real
  system. Draft it; don't send it.
- **Not legal, financial or lending advice.** Anything user-facing says it's a prototype and points
  to a professional for decisions.
- Entries marked UNVERIFIED in `lanes/*/data/DATA-SOURCES.md` are leads, not facts.
  `lanes/3-fund-it/data/synthetic-example-deal.json` and `lanes/*/scenarios.json` are made up:
  never present them as real.

## Project facts (fill in as the team decides; never invent)

- Lane: _TBD_
- The one real user and their before/after: _TBD_
- The one demo path (input → visible result): _TBD_
- Acceptance checks ("doing X shows Y within Z s"): _TBD_
- Stack and delivery form: _TBD_
- Owners: see `TEAM.md`
- Commands that have actually run successfully here: `scripts/smoke_claude_api.sh` failure paths
  only (no key yet). Its success path is unverified.

## How we work today

- Ship one working vertical slice: one real user action through every layer the product needs,
  producing a real result on real public data. One finished path beats five half-built features.
- Before code: restate user, problem and demo path in five lines. Ask when an ambiguity changes
  what gets built; otherwise state the assumption in one line and continue.
- Prove the riskiest assumption first (data access, model quality, an API) with the smallest real
  test.
- Small changes. Run them and read the real output: exit codes, warnings, "0 tests ran". Never
  report success on code that hasn't run. Every "works" points to evidence.
- If a fix fails twice, write down both attempts before trying a third.
- Choose the stack the team can debug fastest. No extra infrastructure. Pin dependencies.
- Core logic in plain functions, testable without UI, network or clock.
- Every outbound call gets a timeout, bounded input and error handling. Cache public data locally
  so the demo doesn't depend on a slow city server.
- Model output is a suggestion. Validate it, show which inputs were missing or assumed, and let a
  person confirm anything consequential. The UI claims only what actually happened.
- Use event-credit keys with spend limits. Check model names and prices in current docs.

## Shared repository (details: `docs/team/TEAM_WORKFLOW.md`)

- Each person works on their own branch (`feat/<name>`) in their own checkout, and never in the
  same folder as another Claude session. Merge to `main` by pull request at checkpoints.
- Edit only files you own (see `TEAM.md`). Shared files (`CLAUDE.md`, dependencies, the interface
  contract) change only in their own commit, with the owner's agreement.
- Commit every working increment and push at least hourly.
- **Keep `NOTES.md` current:** after each meaningful step, add what was done and verified, what's
  broken, and what's next. This is how teammates' Claudes stay in sync.
- Tag known-good states of `main` as `demo-<n>`. After feature freeze, fix demo-path bugs only.
- The repo is public: check no personal information and no keys are in it or its history.

## Where things are

| Path | What |
|---|---|
| `NOTES.md`, `TEAM.md` | Live status and owners/checkpoints. Read first |
| `docs/event/` | Hub snapshot, kickoff-slides summary, the organizers' README and CLAUDE.md verbatim, provenance |
| `docs/challenge-brief.pdf`, `docs/kickoff-slides.pdf` | The 3-page brief and the 35 kickoff slides |
| `docs/background.md`, `docs/glossary.md` | The $0 equation, the laws, the terms |
| `docs/ground-rules.md`, `docs/judging.md`, `docs/submission.md` | Rules, scoring, what to hand in |
| `docs/getting-started.md`, `docs/first-hackathon.md` | Setup and orientation |
| `lanes/<n>-*/README.md` | Each lane's problem, who's stuck, ideas (not a spec) |
| `lanes/<n>-*/data/DATA-SOURCES.md` | Sourced data lists, VERIFIED/UNVERIFIED |
| `lanes/1-find-it/data/pathways.json`, `lanes/2-clear-it/data/oc-cities.json`, `timeline.json` | Starter lists (summaries are not the rule) |
| `lanes/3-fund-it/data/synthetic-example-deal.json` | Made-up one-home bill ($535k cost, $95k gap) |
| `lanes/*/scenarios.json` | Made-up users to design and test against |
| `templates/TEAM-README.md` | What our final README must cover |
| `docs/team/` | Our pre-event playbook, team workflow and research (lower precedence) |
| `scripts/smoke_claude_api.sh` | One real Claude API call to check a key works |

## Communication

Lead with the outcome. Then what was verified and how, what wasn't and why, and any assumptions,
blockers or stubbed parts. Keep this file short and correct; change it only through a reviewed
commit.
