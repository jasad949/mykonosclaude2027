# Status notes

Team-level summary: decisions, checkpoint results, known defects, next priority. **Newest first.**
Owned by the integrator and updated at checkpoints. Day-to-day personal status goes in
`status/<you>.md` (no conflicts that way); tasks are GitHub issues.

## 2026-11-07 10:50 (Jawad): collaboration setup

- GitHub: `main` protected (PR required, 0 approvals, no force-push), squash-only merges, branches
  auto-deleted after merge, wiki off, workflow labels added.
- Added PR template, task issue template, `status/` files, `docs/COLLABORATION.md`, and a
  SessionStart hook that prints repo state into every Claude session. Pipe-tested; it first fires
  in a newly started session.

## 2026-11-07 10:45 (Jawad): knowledge base assembled

**Done**
- Copied the organizers' lane repo (commit `45a05a5`) into this repo unchanged: `docs/`, `lanes/`,
  `templates/`, `LICENSE`.
- Captured the event hub (`docs/event/hub.md`) and summarized all 35 kickoff slides
  (`docs/event/kickoff-slides.md`), including the judges, the lane rules and the video-gates-finals
  rule.
- Merged the organizers' rules into `CLAUDE.md`. Moved our pre-event notes to `docs/team/`.
- Pushed to github.com/jasad949/mykonosclaude2027 as the initial `main`.

**Not decided yet**
- Lane, real user, demo path, stack, roles. See `CLAUDE.md` Project facts and `TEAM.md`.

**Not verified**
- `scripts/smoke_claude_api.sh` success path: no API key on this machine yet.

**Next**
1. Teammates accept the GitHub invite, clone, and read `CLAUDE.md`.
2. Everyone claims API credits on the hub (Org ID from console.anthropic.com).
3. Pick lane + one real user (by 10:45), then fill `CLAUDE.md` Project facts and `TEAM.md` roles.
4. Set the lane on the hub under Edit my team, and fix "still looking for" if the team is complete.

## 2026-11-06 (night before)

**Done**
- Repo skeleton: `.gitignore`, `env.example`, `.claude/settings.json` (denies Claude reading
  `.env`), `TEAM.md` template, Habitat OC background (now `docs/team/habitat-oc-background.md`).
- `scripts/smoke_claude_api.sh`: one real Claude API call (curl + jq). Its failure paths have been
  run: no key → clear error, exit 1; invalid key → `HTTP 401 authentication_error`, exit 1.
