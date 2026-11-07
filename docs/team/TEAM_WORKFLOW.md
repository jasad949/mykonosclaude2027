# Team workflow: one GitHub repo, several Claude Code sessions

A practical guide for a team new to building together with Claude Code. It is language- and
framework-neutral. The commands are plain `git` and the GitHub CLI (`gh`). Organizer
instructions override anything here. Items marked ⏱ should be checked against current docs.

## The five rules

1. **One repository, one checkout per person.** Everyone clones to their own laptop. Never run
   two Claude sessions in the same folder: they will overwrite each other.
2. **`main` always runs the demo.** Nobody commits to `main` directly; the only exception is the
   integrator's first skeleton push. Work arrives by pull request at agreed checkpoints. Known-good
   states of `main` are tagged `demo-<n>`. There is no separate demo branch.
3. **Every file has one owner.** You may read anything. Edit only what you own, or what its owner
   has agreed to.
4. **Parts meet at a written contract.** It is agreed early, has an owner, and changes only by
   agreement.
5. **Before trusting what Claude says about the repo, fetch.** Local copies go stale fast.

## 1. Setup (first 30 minutes, in parallel)

While the integrator does the setup below, the product lead talks to organizers and stakeholders
(see `EVENT_BRIEF.md`) and the others install tools and run `gh auth login`.

**The integrator** creates the repository and the skeleton:

```bash
gh auth login                                   # once per laptop
gh repo create <team-repo> --private --clone    # or --public if the event requires it
cd <team-repo>
```

Add the skeleton files:
- `CLAUDE.md`, from `HACKATHON_CLAUDE.md` renamed. Also add `HACKATHON_PLAYBOOK.md`,
  `TEAM_WORKFLOW.md` and `EVENT_BRIEF.md`. Change `CLAUDE.md` only by pull request.
- `.gitignore`, with the lines `.env`, `.env.*` and `CLAUDE.local.md`, plus build output and
  dependency folders.
- `env.example`, listing variable *names* only. The template has no leading dot so the ignore and
  deny rules don't catch it.
- `TEAM.md`, holding the owner table, the contract location and the checkpoint times.
- `.claude/settings.json`, shared Claude Code settings, for example
  `{"permissions": {"deny": ["Read(./.env)", "Read(./.env.*)"]}}` ⏱. This stops Claude's
  file-reading tool. It does not stop a shell command such as `cat .env`, so never ask Claude to
  print secrets either.

```bash
git add -A && git commit -m "Skeleton"
git branch -M main                # make sure the branch is called main
git push -u origin main
```

Invite teammates in the GitHub web UI (Settings → Collaborators), or with
`gh api -X PUT repos/<owner>/<team-repo>/collaborators/<username>`. **Each invitee must accept the
email or GitHub invitation before they can push.** Protecting `main` under Settings may not be
available on a free plan for private repositories ⏱. If not, rule 2 is a team agreement.

**Everyone else**, after accepting the invite:

```bash
gh repo clone <owner>/<team-repo>
cd <team-repo>
cp env.example .env        # fill in your own values; never commit this file
```

Personal Claude preferences go in `CLAUDE.local.md` (gitignored), not in the shared `CLAUDE.md`.

**One laptop, two sessions?** Give each session its own git worktree, for example
`claude --worktree <name>` ⏱ or `git worktree add ../<team-repo>-<name> -b feat/<name>`. Each
worktree is a separate folder on its own branch. A new folder needs its own `.env` and dependency
install.

## 2. Roles and ownership

Pick roles in the first 15 minutes. People can hold more than one. Non-coders have full roles.

| Role | Owns | Good fit for |
|---|---|---|
| Product and stakeholder lead | Problem statement, stakeholder notes, acceptance checks, evaluation scenarios, sample data | Anyone, no coding needed |
| Builder(s) | One component or directory each | People comfortable with Claude Code |
| Integrator | `main`, the contract, shared config and dependencies, the smoke test, merges, tags | The most git-confident person |
| Demo lead | Demo script, slides, fallback recording, the demo API key, submission | Anyone |

Write the owner table in `TEAM.md` by **directory**, for example `ui/`, `api/`, `docs/`. Non-coders
can edit their own directory in the GitHub web editor. When committing, choose **"Create a new
branch … and start a pull request"**, never "Commit directly to main".

## 3. Agree the interface contract early

Before the builders split up, the integrator writes down where the parts meet. That covers request
and response shapes, function signatures, file formats and error cases, plus one real example of
each. Keep it in one file named in `TEAM.md`.

- Each side builds against the example payloads, so nobody waits for anybody.
- Add a tiny contract test that checks both sides agree on names and shapes. In past projects, a
  renamed parameter failed every call silently. A test caught that whole class of bug for good.
- To change the contract: open a pull request, get both sides to approve, and update the example
  and the test in the same commit.

## 4. The everyday loop

```bash
git switch main && git pull                 # start from the latest main
git switch -c feat/<short-name>             # your own branch
# ... work with Claude, run things, commit small ...
git add -A && git commit -m "What changed and why"
git fetch origin && git merge --no-edit origin/main   # bring teammates' work in often
git push -u origin feat/<short-name>
gh pr create --fill --base main             # open a pull request
```

**After your pull request is merged**, start the next task on a fresh branch. Don't keep
committing to the old one: a squash merge leaves its history out of step with `main`.

```bash
git switch main && git pull
git branch -D feat/<short-name>             # -D because git can't tell a squashed branch is merged
git switch -c feat/<next-task>
```

- Commit every time something works. Push at least hourly, so your work exists somewhere besides
  your laptop.
- Keep pull requests small and single-purpose. Every description should state what was verified,
  how, and what wasn't.
- Merge `main` into your branch (above) rather than rebasing if you are new to git. Never
  `git push --force` to a shared branch.

## 5. Review and merge

- Someone other than the author reviews each pull request. That can be a teammate, or a fresh
  Claude session asked to *find what is wrong* rather than confirm it.
- The reviewer runs the branch in a **separate folder**, so their own work and Claude session
  aren't disturbed:
  ```bash
  git fetch origin
  git worktree add ../review origin/feat/<their-branch>   # then copy .env, install, run the smoke test
  git worktree remove ../review                           # when done
  ```
- The integrator merges at checkpoints: `gh pr merge <number> --squash --delete-branch`.
- After a merge, run the smoke test on `main` straight away. If it's red, fix it forward within
  minutes, or undo the merge with the **Revert** button on the merged pull request's page. That
  opens a new pull request; merge it.

## 6. Integration checkpoints

Agree fixed times, at least at the end of each phase of the day's plan and more often near the end.
At each one:
1. Everyone pushes and opens or updates their pull request.
2. The integrator merges them one at a time, running the smoke test after each.
3. Everyone runs `git switch main && git pull`, then starts or updates a branch as in §4.
4. If `main` passes the demo path, the integrator tags it (§9).

Integrating for the first time at the end is how teams lose the last two hours.

## 7. Shared dependencies and configuration

- One owner, normally the integrator, for the dependency manifest, lockfile, shared config and
  `CLAUDE.md`.
- Need a new dependency? Ask first, then add it in its own pull request with nothing else in it.
- After pulling a dependency change, re-run the install step before diagnosing anything else.
- New environment variable: add its name to `env.example` in the same pull request, and say so in
  the pull request description.
- Credentials: everyone uses their own key for development, so key values never need to be shared.
  The demo uses one designated key with a spend limit, held by the demo lead. If a value must be
  shared, do it in person, not in the repo, issues or chat.

## 8. When git or Claude are out of date

**Signs Claude's picture of the repo is stale:** it mentions functions or files that no longer
exist, its edits fail to apply, it describes `main` without having fetched, or it "fixes" something
a teammate already fixed.

What to do:
```bash
git fetch origin
git status                                  # where am I, what's uncommitted
git log --oneline HEAD..origin/main         # what teammates merged that I don't have
git diff --stat HEAD...origin/main          # which files they touched
```
Then tell Claude which files changed and ask it to re-read them before continuing. After a big
merge, start a fresh session with a five-line summary rather than carrying a long transcript.

**Merge conflicts:**
1. Run `git status` to list the conflicted files.
2. For each file, keep both intents, not just your side. If it's someone else's file, ask them.
3. Claude can help resolve conflicts, but tell it never to drop the other side's changes without
   checking with you.
4. Run the tests, then `git add <files>` and `git commit --no-edit`.
5. If it's a mess, `git merge --abort` returns you to before the merge.

**Taking over someone's unfinished work:** have them push it to a branch, even if broken, and
commit it there unchanged. Fix it in separate commits so "theirs" and "yours" stay distinguishable.

## 9. A stable demo and recovery

- Whenever `main` passes the demo path, the integrator tags exactly what is on GitHub's `main`:
  ```bash
  git fetch origin
  git tag -a demo-<n> origin/main -m "demo path works"
  git push origin demo-<n>
  ```
- The demo lead keeps a runnable copy of the latest good tag in its own folder:
  `git worktree add ../demo-stable demo-<n>`. Then copy `.env` into it, run the install step, and
  start the app once to prove it works.
- If `main` breaks near the deadline, demo from that folder and keep fixing `main` separately.
- To undo a bad merge on `main`, use the pull request's **Revert** button (§5). Never rewrite
  shared history (`reset --hard`, force-push) on `main`.
- Unsure whether an interrupted push, merge or deploy went through? Check GitHub or the deploy
  target before retrying.

## 10. Minimal handoff note

Use this whenever someone switches tasks, leaves, or hands to another session. Put it in the pull
request description or `TEAM.md`, five lines:

```
Done and verified (how):
Not verified / known broken:
Next step:
Blocked on:
Files touched:
```
