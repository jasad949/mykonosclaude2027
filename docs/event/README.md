# Event material: where everything came from

This repo is the team's single source of truth for the Claude Impact Lab (UCI × SoCal Affordable
Housing, Nov 7, 2026). Teammates and their Claude sessions should not need the website, the slides
or the organizers' repo separately: everything is here.

## Sources and how they map into this repo

| Source | Captured | Where it lives here |
|---|---|---|
| Organizers' lane repo, github.com/travcjohnson/claude-impact-lab-uci, commit `45a05a5` | Nov 7, ~10:25 AM PT | Copied unchanged at the repo root: `docs/*.md`, `docs/*.pdf`, `lanes/`, `templates/`, `LICENSE`. Its `README.md` and `CLAUDE.md` are kept verbatim as [`upstream-README.md`](upstream-README.md) and [`upstream-CLAUDE.md`](upstream-CLAUDE.md); their rules are merged into the root `CLAUDE.md` |
| Event hub, claudesocal.com/uci-impact-lab | Nov 7, ~10:20 AM PT | [`hub.md`](hub.md) |
| Kickoff slides (35 slides) | Nov 7 | PDF at [`docs/kickoff-slides.pdf`](../kickoff-slides.pdf) (same file as the organizers' copy); summary at [`kickoff-slides.md`](kickoff-slides.md) |
| Our pre-event prep (Nov 5–6) | Nov 6 | [`docs/team/`](../team/). Written before the lanes were revealed: where it disagrees with the event material, the event material wins |

## Precedence

1. Organizer instructions given at the event (in person, WhatsApp, the hub)
2. The organizers' material: the brief, lane pages, ground rules, judging, submission
3. Our project decisions in the root `CLAUDE.md` (lane, user, demo path)
4. Our general notes in `docs/team/`

## Refreshing from the organizers

The organizers may push updates to their repo during the day. To check:

```bash
git ls-remote https://github.com/travcjohnson/claude-impact-lab-uci HEAD
```

If the hash is no longer `45a05a5...`, one person clones it, copies the changed files in (keeping
`README.md` and `CLAUDE.md` in this folder as `upstream-*.md`), updates the commit hash above, and
opens a pull request.
