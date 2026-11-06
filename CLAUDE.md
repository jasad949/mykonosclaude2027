# CLAUDE.md — one-day hackathon build

Default operating rules for a team building, testing and demonstrating a product in one day.
**Precedence:** organizer instructions, then this project's spec (the Project facts below and any
spec they link to), then these notes. Product and architecture come from the spec, never from
these notes. `docs/HACKATHON_PLAYBOOK.md` (reasoning), `docs/TEAM_WORKFLOW.md` (shared-repo
process), `docs/EVENT_BRIEF.md` (event context) and `docs/BACKGROUND.md` (public research on
Habitat OC, unverified) hold the detail. `TEAM.md` holds owners and checkpoints; `NOTES.md` the
running status.

## Objective

Ship one working, demonstrable vertical slice: a real user action going through every layer the
product needs, and producing a real result. One finished path beats five half-built features.

## Project facts (fill in; never invent)

- Problem, target user, and the stakeholder who confirmed it: _TBD_
- The one demo path (input → visible result): _TBD_
- Acceptance criteria, judging rules, submission deadline and format: _TBD_
- Stack and delivery form, chosen for this project: _TBD_
- Owners: who owns which directories and the interface contract: _TBD_
- Commands that have actually run successfully here (setup / run / test): _none yet_

## Before writing code

1. Restate the problem, the user and the demo path in five lines or fewer. Ask when an ambiguity
   changes what gets built. Otherwise state the assumption in one line and continue.
2. Write the acceptance criteria as observable checks ("doing X shows Y within Z s").
3. Prove the riskiest assumption first with the smallest real test. That might be an API, model
   quality, data availability, platform capability, or an unfamiliar technique.
4. Split the work into increments, each of which ends in something runnable.

Plan explicitly only for multi-module changes, an undecided interface, or after two failed attempts.

## Technology and architecture

- Choose the stack the team can debug fastest that meets the requirements. If the requirements
  force something unfamiliar, spike it within the first hour.
- Add no infrastructure (extra services, queues, caches, stores) unless the demo path needs it.
- Add dependencies sparingly. Pin them, skip prereleases, and make no major upgrades today.
- Keep core logic in plain functions, testable without the UI, network or clock.
- No speculative abstraction or "for later" configurability.

## Shared repository (see TEAM_WORKFLOW.md)

- Work on your own branch in your own checkout. Never commit straight to `main` (only the
  integrator's first skeleton push does). Known-good states are tags, not branches.
- Edit only files you own. Changes to the interface contract, shared config or dependencies need
  their owner's agreement and go in their own commit.
- Before starting a task, and before saying anything about repository state, run `git fetch` and
  compare with `origin`. A local branch may be many commits stale.
- If files changed under you, re-read them before editing. Never discard or overwrite changes you
  didn't make. Ask instead.

## Working loop

- Make small changes, run them, and read the actual output: exit codes, warnings, skipped tests,
  "0 tests ran". Never report success based on code that hasn't been executed.
- When something fails, reproduce it, read the real value, and check the premise before theorising.
- If a fix fails twice, write down both attempts and what they ruled out before trying a third.
- Before blaming product code, rule out stale builds, dev-mode flags, a full disk, colliding test
  runs, expired tokens and missing env vars.
- Installed is not wired. Confirm a new library or provider actually takes effect in the running app.
- Don't rewrite working code for looks. Don't expand scope without being asked.
- If a command was interrupted, check whether its effect (deploy, push, paid call) happened anyway.

## Verification and tests

Test by risk and remaining time: (1) a fast smoke test of the demo path; (2) exact-assertion
tests on critical logic; (3) a regression test per bug fixed, failing first; (4) failure cases
the demo can hit; (5) contract tests where teammates' parts meet.

- Watch critical tests fail once. Commit, break the code on purpose, see red, restore with version
  control. Skip this when under an hour remains.
- Never mock the unit under test. Mock only external or non-deterministic boundaries.
- A paid or slow dependency gets two smoke tests: a fast one against a recorded real response, and
  a live one at checkpoints.
- Proxies (mocks, a different platform build) aren't proof. Verify what the *running* app is
  connected to (which environment, data and keys), not what a config file intends.

## Data, AI output, secrets, cost

- Use synthetic or de-identified data. Never put real personal or financial records into
  prompts, logs, fixtures or git unless the data owner explicitly allows it.
- Never commit secrets or embed them in anything distributed to users. Missing required config
  fails loudly. An optional integration without credentials says "not configured".
- Every outbound call gets a timeout, bounded input and error handling. Don't blindly retry
  operations that may already have been charged or applied.
- Model output is a suggestion. Validate it, show which inputs were missing or assumed, and let a
  person confirm anything consequential.
- The UI must claim only what actually happened ("saved", "sent", "complete").
- Use dedicated keys with spend limits. Log real usage. Check model names and prices in current docs.

## Checkpoints and demo

- Commit every working increment. Merge to `main` only through review, at agreed checkpoints.
- Tag known-good states of `main` (`demo-<n>`), and build or deploy only from clean, committed trees.
- After feature freeze, fix demo-path bugs only.
- Rehearse from a cold start on the real environment. Have a labelled fallback (a recording or a
  cached real result), never a fake result presented as live.

## Communication

Lead with the outcome. Then give what was verified and how, what wasn't and why, and any
assumptions, blockers or stubbed features. Every "works" points to evidence. Keep this file short
and correct, and change it only through a reviewed commit.

## Hackathon Development Workflow

Optimize for a working, demonstrable product within the available time.

- Translate each major feature into explicit, observable acceptance criteria.
- For uncertain integrations, prove the critical capability with a small end-to-end experiment before expanding the implementation.
- Work in small, verifiable increments. Implement, run, inspect results, and correct failures before moving to unrelated tasks.
- Independently investigate ordinary errors and apply well-supported fixes without requiring the user to approve each debugging step.
- If two materially different attempts fail, stop repeating fixes. Summarize the evidence, likely root causes, and recommended next action.
- Ask for user input when product requirements are genuinely ambiguous, a decision has substantial consequences, or a proposed action is difficult to reverse.
- Avoid lengthy planning for minor, reversible changes.
- Prefer a reliable core workflow over additional features.
- Maintain a short record of completed features, known defects, test results, and the next priority.
- Preserve a stable, working state before making risky changes.
- Reserve sufficient time for an actual end-to-end demonstration, including realistic failure handling and submission requirements.
- Do not declare a feature complete without observable evidence. Report what was tested and what remains unverified.

User decisions should focus on product direction, tradeoffs, and acceptance of results rather than routine implementation mechanics.
