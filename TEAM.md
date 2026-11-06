# Team

Fill this in during the first 15 minutes (see `docs/TEAM_WORKFLOW.md` §2). Change by pull request.

## People and roles

| Name | GitHub | Role(s) | Owns (directories / files) |
|---|---|---|---|
| | | Product and stakeholder lead | `docs/stakeholders/`, acceptance checks, sample data |
| | | Integrator | `main`, contract, shared config, dependencies, smoke test, tags |
| | | Builder | _TBD_ |
| | | Builder | _TBD_ |
| | | Demo lead | demo script, slides, fallback recording, submission |

## Interface contract

- File: _TBD_ (one file, owned by the integrator, with one real example per payload)
- Contract test: _TBD_

## Checkpoints (fill once the submission deadline D is known)

Shares from `docs/EVENT_BRIEF.md`: discover ~10%, spike + skeleton ~15%, build ~35%,
harden ~20% (freeze at the end), demo prep ~20%. Subtract lunch and talks first.

| Checkpoint | Time | Done when |
|---|---|---|
| Scope agreed | | Problem, user, demo path and acceptance checks written in `CLAUDE.md` |
| Spike + skeleton | | Riskiest assumption proven; skeleton runs end to end; tag `demo-0` |
| Slice working | | Demo path works on synthetic data; tag `demo-1` |
| Feature freeze | | Only demo-path bug fixes after this; tag `demo-2` |
| Rehearsed + submitted | | Two cold-start rehearsals, fallback recorded, submission sent before D |
