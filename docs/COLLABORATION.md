# How we work together in this repo (3 people, 3+ Claude sessions)

Short and specific to today. The general version is `docs/team/TEAM_WORKFLOW.md`.

## What's set up on GitHub

- **`main` is protected.** Changes land only through a pull request. No approval is required, so
  you can merge your own PR, but nobody can push straight to `main` or force-push it. (The repo
  admin can bypass this in an emergency.)
- **Squash merge only**, and branches are deleted after merge. Each PR becomes one commit on
  `main`.
- **Issues are the task board.** One issue = one task = one owner = a named set of files.
  Labels: `task`, `in-progress`, `blocked`, `demo-path`, `decision`.
- **PR template** asks what was verified, what wasn't, and which files were touched.
- **SessionStart hook** (`.claude/settings.json` → `scripts/session_start.sh`): every Claude
  session starts by fetching and printing your branch, how far behind `main` you are, open PRs
  and open tasks.

## The four rules that prevent clashes

1. **One person, one area of files.** Before building, we split the code into directories with one
   owner each (see `TEAM.md`). You may read anything; edit only your own area. Two tasks that
   need the same file are one task.
2. **One Claude session per folder.** Two sessions in one checkout overwrite each other. If you
   want two sessions, use a worktree (below).
3. **Small PRs, merged often.** Branch → commit → PR within about an hour. Long-lived branches are
   where conflicts come from.
4. **Shared files have one owner and change in their own PR:** `CLAUDE.md`, `TEAM.md`, `NOTES.md`,
   the interface contract, dependency files, `.claude/settings.json`. Owner: the integrator
   (Jawad, until roles are set). Ask in person before touching them.

## The loop (give these steps to your Claude)

```bash
# start a task
git switch main && git pull --ff-only
git switch -c <you>/<task>                 # e.g. omar/income-limits-table

# work, committing small; then before opening a PR
git fetch origin && git merge origin/main   # bring teammates' work in; fix conflicts in YOUR files
git push -u origin HEAD
gh pr create --fill                        # template fills in; add "Closes #<issue>"

# merge when checks look right (yours or a teammate's PR)
gh pr merge --squash
git switch main && git pull --ff-only      # then start the next task on a NEW branch
```

Never `git push --force`, `git reset --hard origin/...` or delete a branch you didn't create.
If a merge conflict is in someone else's file, stop and ask them.

## Delegation: how work gets handed out

1. Whoever splits work creates issues:
   `gh issue create --title "Income-limits table for OC, dated" --label task --assignee <login>`
   Each issue names the files it touches and what "done" looks like (template provided).
2. The owner moves it: add `in-progress` when starting, `blocked` (with a comment saying on what)
   if stuck, and close it via the PR (`Closes #12`).
3. Your Claude can read the board: `gh issue list`, `gh issue view 12`.
4. Status lives in **your own file**, `status/<you>.md`: what you're on, branch, files touched,
   what's done and verified. Only you edit it, so it never conflicts. `NOTES.md` is the team
   summary the integrator updates at checkpoints.

## Several Claude sessions on one laptop

Each session needs its own folder and branch:

```bash
git worktree add ../mykonos-<task> -b <you>/<task>   # new folder on a new branch
cd ../mykonos-<task> && cp ../mykonosclaude2027/.env . && claude
git worktree remove ../mykonos-<task>                # after its PR is merged
```

Or start Claude with `claude --worktree <name>`, which does the same.

## Checkpoints (times in `TEAM.md`)

At each checkpoint: everyone pushes and opens or updates their PR. The integrator merges them one
at a time, runs the demo path on `main`, and tags it (`git tag demo-<n> && git push origin
demo-<n>`). Everyone then pulls `main` and starts fresh branches. After feature freeze (1:40):
demo-path bug fixes only.

## Recommended code layout (finalize in `TEAM.md` once the stack is chosen)

Split so each person owns one directory and the parts meet at one written contract:

| Directory | Holds | Good owner |
|---|---|---|
| `engine/` | Pure calculation and matching logic plus tests. No UI, no network | Strongest coder |
| `app/` | The interface the user sees and the demo runs on | Second coder or designer |
| `data/` | Cached public data (income limits, rates, programs) with source URL and date on every record | Research / non-coder |
| `docs/project/` | User, decisions, demo script, video script, submission text | Presenter |
| `data/SCHEMA.md` (the contract) | The shape of the data the engine reads, with one real example | Integrator |

`data/` as hand-checked JSON or CSV files lets a non-coder contribute real work through the GitHub
web editor without touching code.

## If things go wrong

- Your Claude talks about files that don't exist, or edits fail: `git fetch`, then
  `git log --oneline HEAD..origin/main`. Tell Claude which files changed and to re-read them.
- Merge conflict: `git status`, keep both sides' intent, ask the other owner if it's their file,
  `git merge --abort` to back out.
- A bad merge on `main`: use the **Revert** button on the merged PR's page. Don't rewrite history.
- `main` broken near the deadline: demo from the last `demo-<n>` tag
  (`git worktree add ../demo-stable demo-<n>`).
