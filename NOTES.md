# Status notes

Short running record: completed, known defects, test results, next priority. Newest first.

## 2026-11-06 (night before)

**Done**
- Repo skeleton: `.gitignore`, `env.example`, `.claude/settings.json` (denies Claude reading
  `.env`), `TEAM.md` template, `docs/BACKGROUND.md` (public Habitat OC research).
- `scripts/smoke_claude_api.sh`: one real Claude API call (curl + jq). Its failure paths have been
  run: no key → clear error, exit 1; invalid key → `HTTP 401 authentication_error`, exit 1.

**Not verified**
- The smoke test's success path. There's no API key on this machine yet.

**Next**
1. Get the event API key, put it in `.env`, run `scripts/smoke_claude_api.sh` and see `PASS`.
2. At the event: organizer questions (`docs/EVENT_BRIEF.md`), fill `TEAM.md`, then the Project
   facts in `CLAUDE.md`.
