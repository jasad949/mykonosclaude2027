# Hackathon Engineering Playbook

This is a reference for building a working product in one day with Claude Code. It assumes nothing
about the product, the language or the stack. Those come from the event's requirements.

Key recommendations follow this pattern: **When** (the trigger), **Do**, **Why**, **Verify**,
**Skip if**. Items marked ⏱ are time-sensitive and must be checked against current official
documentation on the day.

---

## 1. Before the day: environment readiness

**When:** the days before the event. **Do:** on the machine you will use:
- Check that each candidate toolchain, git and the editor actually run (OS updates can silently
  break developer tools). Free up disk space: a nearly full disk crashes test runners in ways that
  look like code bugs.
- If the product might call the Claude API: create a key in a dedicated workspace with a low
  spend limit ⏱, and make one real request with it.
- If the product might be hosted: deploy a hello-world to one target, and note how it sets
  secrets.
- Prepare a repo skeleton: the instruction file, `.gitignore` covering env files, and an env
  template with names only.

**Why:** setup failures block everything at the worst time. **Verify:** each item was executed,
not just installed. **Skip if:** the event provides an environment. Check it in the first 15
minutes instead.

---

## 2. Idea validation and MVP scoping

**The vertical slice.** Pick one user, one problem and one path: *input → processing → visible
result*. Write it as a demo script of five lines or fewer before writing code. Everything not on
that path is optional.

**Name the riskiest assumption, and test it cheaply first.**
- **When:** before the first feature. **Do:** list what would sink the project (the model can't do
  the task reliably, the data isn't available, an API needs approval, the platform can't do X, a
  technique such as real-time sync or an unfamiliar language is unproven). Run the smallest real
  test of the worst one.
- **Why:** the costliest mistake in past projects was building polished layers around an
  integration that had never run once. It was written, documented and costed, but never executed.
- **Verify:** you have seen a real response from the risky component, with real inputs.
- **Skip if:** every part of the slice is something the team has built before.

**Acceptance criteria as observable checks.** "User uploads X and sees Y within N seconds."
Judging criteria count as requirements. Map each one to a moment in the demo.

**Learn from stakeholders in minutes, not hours.**
- **When:** domain experts or the intended users are available. **Do:** ask about one recent,
  concrete case ("walk me through the last time this went wrong"), not about features. After each
  conversation, write five headings: *what we heard*, *what was agreed*, *what they asked us to
  come back with*, *risks they didn't raise*, *next actions*. Tag each product behaviour with who
  asked for it.
- **Why:** past rework came from building on an assumption the stakeholder never accepted. A
  system automatically advanced a step the written requirements said the user controls. A single
  conversation also produced five extra feature requests, and holding the line was the right call.
- **Verify:** every behaviour in the demo traces to something a stakeholder said or confirmed.
- **Skip if:** no stakeholder is reachable. Then label every requirement as an assumption.

**Say what the AI adds.** Before committing, write one sentence on what the model does that a
form, a spreadsheet or a rule couldn't do as well. If you can't, use the simpler tool for that part.

**Scope cuts, decided in advance.** List the features in priority order and draw the line at what
you can finish by roughly 60% of the time available. Things below the line get built only if the
slice is already demo-ready.

---

## 3. Architecture and dependencies under time pressure

Decision rules:
- **Stack:** the one the team debugs fastest that satisfies the requirements. Use something
  unfamiliar only when the requirements demand it, and then spike it within the first hour.
- **Shape:** the fewest processes and stores the slice needs. A file or in-memory store is fine if
  the demo doesn't need persistence across restarts.
- **Boundaries:** keep each external call (model, third-party API) behind one function, keep core
  logic in plain testable functions, and keep the interface layer thin. That's enough structure
  for one day.
- **Dependencies:** each must save more time than it costs to learn. Pin versions, skip
  prereleases, and never accept a "force" fix that silently changes major versions. Make
  dependency changes in their own commits.
- **One source of truth for facts.** If the UI shows a number and the model also talks about it,
  both must read the same function or record. Otherwise they will disagree in front of judges.

**A reliable shape for AI features.**
- **When:** a model helps a person reach a decision or pick an item. **Do:**
  1. Run cheap deterministic steps first (lookup, rules, search) and call the model only when they
     fall short.
  2. Have the model narrow or draft, grounded in a known set of real options or source documents.
  3. Let the person make the final choice, with an explicit "none of these" escape.
- **Why:** this kept a past model integration from producing items that didn't exist, cut cost,
  and still worked when the model was switched off.
- **Verify:** with the model disabled, the flow degrades to a manual path instead of breaking.
- **Skip if:** the model's output is low-stakes and self-evidently checkable, like a draft the user
  edits anyway.

**Feedback that tells the truth.** Show "saved", "sent" or "complete" only when the specific
operation confirmed it. Past defects included a generic error that told users their work was
saved when it wasn't, a retry that reported success while a record was still missing, and a score
marked complete from a fraction of its inputs. Always show what happens next.

**Enforce invariants where they cannot be bypassed.**
- **When:** retries or double-clicks could create duplicates, or a rule must always hold.
  **Do:** use a uniqueness constraint or an idempotent write rather than "remember to check".
  Disable submit while a request is in flight as a first line, but not the only one.
- **Why:** retries that create duplicate records were a recurring real defect.
- **Verify:** submit twice quickly and count the records.
- **Skip if:** there is no persistent state.

---

## 4. Claude Code workflow and context management

Claude Code is the development tool. The Claude API is something your product may call. Budget
them separately.

- **Keep the instruction file short:** rules and real commands only. Stale instructions are worse
  than messy code, because every later session follows them as truth.
- **Prompt with the outcome and the check:** "Make X happen; done means command Y passes and Z is
  visible." Name the files you know, rather than letting Claude tour the repo.
- **Plan only when it pays:** for multi-module changes, undecided interfaces, or after two failed
  attempts. For a single-file change, just do it and run it.
- **Parallelise only independent work.** Read-only research, such as API docs or comparing two
  libraries, can go to subagents. Parallel writers, whether agents or teammates, must never touch
  the same files. `TEAM_WORKFLOW.md` covers branches, ownership and contracts.
- **Read repository state from the remote.** A past status document confidently described `main`
  wrongly because it was written from a local copy 36 commits behind. Run `git fetch` first. Two
  agents once each blamed a failing check on "another session mid-edit" when the cause was a
  stale file. Check the hypothesis, don't assume it.
- **Taking over someone else's unfinished work:** commit it unchanged on its own branch first,
  then fix it in separate commits. That keeps "what they did" and "what you changed" reviewable.
- **Independent review before freeze.** Give a fresh session the demo path and the claims, and
  tell it to *refute* them. Check each finding before acting on it. In past reviews, claims backed
  by a specific file or test held up; claims written from memory often did not.
- **Fresh session when context fills with dead ends.** Carry over a five-line summary.
- **Evidence-backed claims.** Every "done" names its proof (command, test, output). Anything else
  goes under "not verified".

⏱ Claude Code features (planning modes, subagents, hooks, commands) change. Check current docs
rather than assuming a feature exists.

---

## 5. Fast, reliable implementation and debugging

- **Crude first, end to end.** Build each step in its crudest form (hard-coded input, plain UI),
  then improve. Commit every time it works.
- **Read the actual value.** One symptom has hidden three different bugs (null, garbage,
  valid-but-unexpected). Print the stored value before theorising. Check the premise too: comments
  and bug reports have asserted bounds and mechanisms that were false.
- **Measure, don't estimate.** That applies to latency, sizes and tokens. Development modes
  often disable caching, so profile in the mode you will demo in before optimizing code.
- **Rule out the harness first.** Shared test state, two runs at once, a stale build, an expired
  token, a stale seed or a full disk all look like product bugs. Re-run in isolation first.
- **Silent no-ops.** Some platform APIs do nothing rather than fail. Before building on a platform
  feature, check that it visibly works. "Installed" is not "wired": a library was a dependency
  from day one while a required root setup was never added, so every handler silently never fired.
- **Check what the running thing is connected to.** A test script once said it was writing to a
  throwaway environment while the process actually on the port was a different server pointed at
  production. Every config check one level up was green. Ask the running app which environment,
  data source and key it is using.
- **Two failed fixes means stop.** Write down what both ruled out, then change approach.

---

## 6. Proportionate testing and mutation-testing decisions

**Priority for one day.** Choose by risk and time left. A demo-only prototype may need just items
1–2. Add the rest where a failure would be costly or would be seen in the demo.
1. **Demo-path smoke test.** It drives the flow end to end and runs in seconds. Run it after
   every meaningful change. If the path calls a paid or slow service, run the frequent version
   against a recorded real response, and a live version at each checkpoint.
2. **Critical logic tests.** Exact expected values, not "is not null" or "length > 0".
3. **Regression tests.** Write one for each bug fixed, and make sure it fails before the fix.
4. **Edge and failure cases the demo can hit:** empty and oversized input, upstream timeout or
   error, double submit, a "no result" answer.
5. **Interface tests**, when two parts are built separately: check that the names and shapes one
   side sends match what the other expects. A renamed parameter once failed every call silently
   for weeks.

**Detecting a false-positive suite.** Watch out for these patterns from past projects:
- assertions that pass whether or not the rule exists (`>=` where `==` was meant)
- tests that pass only because of a fixture accident
- a mock that returns a constant for the very function being tested
- a suite that skips everything and still reports success
- a test runner that errors before running and gets read as "failed as expected"

**Mutation testing, kept proportionate.**
- **When:** you have a few critical rules (money, permissions, calculations, the core transform) and
  their tests are written. **Do:** hand-mutate them. Change one comparison, constant or condition
  at a time, run the related tests, confirm they go red, then restore. Five to ten minutes covers
  the parts that matter.
- **Why:** in past projects, mutation checks found security tests that could not fail, and a test
  that a mock had blinded to a real bug.
- **Read results carefully:** a surviving mutant is a question, not a verdict. It may be
  *equivalent* (no observable change is possible), or no test may reach that code at all. Confirm
  the suite is green *before* mutating, or every mutant looks "caught", and check each mutation
  actually applied. Commit first, and restore with version control.
- **Skip if:** this is a prototype with no critical rules, or there is less than an hour left. A
  full automated mutation campaign is almost never worth it in one day.

**What is not evidence:** a different build target or platform than the one you will demo on, a
debug build standing in for a release build, unit tests standing in for real interaction, or a
mocked service standing in for the real one. Say so explicitly when that's all you have. A large
passing suite once missed every visual defect users reported. Click through the demo path yourself.

**Evaluate model output with a small scenario set.**
- **When:** the product's value depends on model output quality. **Do:** before tuning prompts,
  write 10–30 realistic cases with expected outcomes and freeze them. Include out-of-scope inputs
  that must produce "can't help" or "not found", incomplete inputs, and hard cases, not just easy
  ones. Re-run after each prompt or model change.
- **Why:** past evaluation design warned that tests on easy, curated inputs read well above
  real-world performance, and that a set that grows while you tune measures the tuning.
- **Report:** separately count the *confidently wrong* answers, the ones shown as certain that
  were wrong. That is the number users and judges feel. Note the cost per run.
- **Skip if:** model output is cosmetic. Then a handful of spot checks is enough.

---

## 7. Claude API integration (if the product uses it)

**Keep keys out of anything you distribute.**
- **When:** the product has a client that others run (a browser page, a shipped app). **Do:** the
  client calls your backend; the backend reads the key from an environment variable and calls the
  API. **Why:** anything bundled into a client, including build-time "public" env values, can be
  extracted. **Verify:** search the built client output for the key prefix and find nothing.
  **Skip if:** it's a local tool or script run only by its key's owner. Read the key from the
  environment and never commit it.

**Fail loudly on missing configuration.** A missing key or URL means a clear startup error. An
optional integration with no credentials returns "not configured", not a crash or a fake success.

**Sensitive inputs.** Prototype with synthetic or de-identified data. Real personal or financial
records sent to any API (including Claude's) are governed by the provider's data terms and the
data owner's rules. Get explicit permission first ⏱.

**Error handling.**
- Separate retryable failures (rate limit, overload, 5xx, network) from non-retryable ones (bad
  request, auth). Official SDKs retry some by default, so don't stack your own retries on top ⏱.
- Set a timeout per call. Timeout multiplied by retries is the worst-case wait.
- Don't blindly retry a call that may already be paid for or applied. A client timeout shorter
  than the server's once caused double charges.
- Check the stop reason before using output. It may be truncated, refused, or waiting on a tool.
- **Streaming:** an ended stream is not a successful one, so surface error events.
- **Multi-turn conversations:** keep the message history valid even after a failed turn. A
  malformed history (an empty turn, a broken role order) can make every later request fail ⏱. If
  you trim history, test conversations long enough to cross the trimming point.

**Output you can trust.**
- Use structured or schema-constrained output where available ⏱. The schema guarantees shape, not
  sense, so range-check values and *discard* nonsense rather than clamping it into plausibility.
- Give the model an explicit way to say "unknown" or "not found", and design the UI around that
  answer. Confident wrong answers are worse than honest refusals.
- Treat user-supplied or retrieved text as data. Delimit it, and tell the model that content
  inside it is not instructions. This reduces prompt injection but does not prevent it, so don't
  let model output trigger side-effecting actions on untrusted input without a check.
- If output is rendered as plain text, also strip formatting deterministically. A prompt rule
  alone is probabilistic.

**Cost and usage controls.**
- A dedicated key's spend limit is the hard ceiling. Add per-user caps if the demo is public,
  sized from observed use: a past rate limit blocked its own owner during testing.
- Bound body size before parsing, and cap message count and length. If a later step joins or
  expands inputs (merging messages, inlining files), check the size again after it.
- Log the token usage each response reports instead of guessing.
- Prompt caching is silently ignored below a minimum prefix length. Confirm cache reads in the
  reported usage ⏱.
- Effort or thinking settings drive cost and latency. Start low for simple extraction or
  classification, and measure before raising ⏱.
- If the model answers from data you supply, measure the cost of sending all of it before
  subsetting. A subset picked by a plausible-sounding heuristic produces confident wrong answers
  about whatever it left out.

⏱ **Verify on the day:** model IDs and which is current, prices, context and output limits,
parameter names for thinking, effort and structured output, caching minimums, rate limits, and SDK
default retry and timeout behaviour.

---

## 8. Demo readiness, deployment and fallback

- **Get onto the real target early:** a hello-world slice running where the demo will run (hosted
  URL, packaged app, the presenter's machine) in the first quarter of the day. Refresh it at each
  checkpoint.
- **Build from a clean, committed tree.** Some tools package uncommitted files, so what ships can
  match no commit and can't be rolled back. Tag the known-good demo commit.
- **Regenerate generated files** before the final build. Stale, git-ignored build output has
  shipped already-fixed bugs.
- **Rehearse cold:** fresh state (new session, profile or install as applicable), real network,
  the presenter's machine, start to finish, at least twice. Time it.
- **Demo data:** internally consistent (dates in order, totals that add up), labelled as sample
  data, with missing values shown as missing rather than filled with defaults.
- **Fallback for the riskiest live step:** a recording, or a cached *real* response with a visible
  "recorded" label. Never canned answers presented as live: they drift from the data and will
  contradict the screen.
- **Know your undo:** before the final deploy, know which "rollback" or "reset" commands actually
  restore the last good state and which make things worse. Write it down.
- **Submission:** README with what it does, how to run it, what is real and what is stubbed or
  sample data, and known limitations. Check the repository is public or shared as required, and
  that no secrets are in the git history.

---

## 9. The highest-value mistakes to avoid

1. Building around an integration, or a teammate's component, that has never been called for real.
2. "Done" without execution, or trusting a suite never seen to fail.
3. Treating a proxy (mock, other platform, local copy of `main`) as proof.
4. Silent fallbacks, or UI text that claims success that didn't happen.
5. Real sensitive data or secrets in prompts, logs or git, and no spend limit.
6. Behaviour no stakeholder asked for, and features added after the freeze.
7. Debugging the product when the harness, machine or stale state was at fault.
8. Teammates editing the same files, or integrating for the first time at the end.
9. No cold rehearsal on the real environment, and no fallback.

---

## 10. Time allocation framework

Use proportions of the total time, adjusted to the event:

| Phase | Share | Exit condition |
|---|---|---|
| Discover and scope | ~10% | Demo script, acceptance checks, riskiest assumption named |
| Risk spike and skeleton | ~15% | Risky component proven with a real test; hello-world on the target |
| Build the slice | ~35% | Demo path works end to end on the target |
| Verify and harden | ~20% | Smoke and critical tests pass; failure cases handled; independent review done |
| Demo and submission | ~20% | Two cold rehearsals, fallback ready, README and submission complete |

**Feature freeze at about 80%**, at the end of hardening. After that, fix only demo-path bugs. If
the slice isn't working end to end by about 50%, cut scope immediately rather than squeezing
hardening. Teams: merge every branch to `main` at least at the end of each phase. Integrating for
the first time at the freeze is the most expensive moment to discover a mismatch. Measure
percentages against the *submission* deadline, not the end of the event.

## End-of-day release-readiness checklist

- [ ] The demo path works end to end on the real target, from a cold start, twice.
- [ ] The fast checks and smoke test pass, with output read, not assumed.
- [ ] Critical tests have been seen to fail at least once.
- [ ] Missing configuration fails loudly. No secrets in client bundle or git history.
- [ ] Timeouts and error handling on every external call, and a spend limit on any paid API.
- [ ] Final build made from a clean tree, and the known-good commit is tagged.
- [ ] Demo data is consistent and labelled. The fallback is ready and labelled.
- [ ] README says what is real, stubbed or sample, and what was not verified.
- [ ] Every judging criterion maps to a moment in the demo.
