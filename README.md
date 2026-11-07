# [Project name: TBD]

> One sentence: who it is for and what it does. _(TBD once the team picks a lane and user.)_

**Team:** Mykonos 2027
**Members:** Jawad, Omar, Hassan
**Lane:** _TBD_ (1 Find it | 2 Clear it | 3 Fund it | our own direction)
**Built at:** Claude Impact Lab: UCI × SoCal Affordable Housing, November 7, 2026

---

## For teammates: start here

This repo is our single source of truth. It contains the organizers' full lane repo, the event
hub, the kickoff slides, our decisions and our status. You and your Claude don't need the website,
the slides or the organizers' repo separately.

```bash
gh repo clone jasad949/mykonosclaude2027
cd mykonosclaude2027
cp env.example .env        # add your own ANTHROPIC_API_KEY; never commit .env
claude                     # Claude Code reads CLAUDE.md automatically
```

Then read, in order: [`CLAUDE.md`](CLAUDE.md) (rules and map), [`NOTES.md`](NOTES.md) (status),
[`TEAM.md`](TEAM.md) (owners and checkpoints), [`docs/event/`](docs/event/README.md) (hub, slides,
judges). Work on your own branch and open a pull request into `main`
([workflow](docs/team/TEAM_WORKFLOW.md)).

_The sections below follow [`templates/TEAM-README.md`](templates/TEAM-README.md) and get filled in
as we build. Remove this "For teammates" section before submitting if it gets in the judges' way._

---

## The real user

_TBD._ Who is the person? What is hard for them today? Three sentences.

**Before:** _TBD_
**After:** _TBD_

## What we built

_TBD._

**Demo video:** _TBD_
**Live demo:** _TBD (optional)_

## How Claude is used

- How we built it with Claude: _TBD_
- What Claude does inside the tool when it runs, and what a person checks: _TBD_

## Try it

```bash
# exact steps to run it on a laptop: TBD
```

What someone needs installed, and any environment variables (names in [`env.example`](env.example)).
No keys in the repo.

## Sources and assumptions

| Item | Source or assumption | Date checked |
|---|---|---|
| | | |

Every number we made up is labelled ASSUMPTION here and in the tool.

## What is real and what is mocked

| Part | Status |
|---|---|
| | |

## Where it gets things wrong

_TBD._

## Next steps

_TBD._

## Data and privacy

This project uses only public or provided data. It contains no personal information about real
tenants, buyers or residents. It does not file applications or contact any city or person.

## License

MIT, see [LICENSE](LICENSE) (from the organizers' starter repo).

## Repo contents

The organizers' starter material ([github.com/travcjohnson/claude-impact-lab-uci](https://github.com/travcjohnson/claude-impact-lab-uci),
MIT / CC0) is included unchanged under `docs/`, `lanes/` and `templates/`. See
[`docs/event/README.md`](docs/event/README.md) for provenance.
