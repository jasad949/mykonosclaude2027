#!/usr/bin/env bash
# SessionStart hook (wired in .claude/settings.json). Prints fresh repo state into every
# teammate's Claude session so nobody works from a stale checkout. Read-only: it fetches but
# never merges, pulls or switches branches.
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0

if ! git fetch -q origin 2>/dev/null; then
  echo "(git fetch failed, maybe offline: the state below may be stale)"
fi

branch=$(git branch --show-current)
echo "== Repo state at session start ($(date '+%H:%M')) =="
echo "Branch: ${branch:-detached HEAD}"
git status -sb | head -1
echo "Commits on origin/main not in this checkout: $(git rev-list --count HEAD..origin/main 2>/dev/null || echo '?')"
git log --format='  %h %an: %s' HEAD..origin/main 2>/dev/null | head -10
echo "Uncommitted files here: $(git status --porcelain | wc -l | tr -d ' ')"
if [ "$branch" = "main" ]; then
  echo "NOTE: on main. Before editing: git pull --ff-only && git switch -c <you>/<task>"
fi
if command -v gh >/dev/null 2>&1; then
  echo "Open pull requests:"
  gh pr list --limit 10 --json number,title,author,headRefName \
    --template '{{range .}}  #{{.number}} {{.title}} ({{.author.login}}, {{.headRefName}}){{"\n"}}{{end}}' 2>/dev/null \
    || echo "  (gh could not list PRs)"
  echo "Open tasks (issues):"
  gh issue list --limit 15 --json number,title,assignees \
    --template '{{range .}}  #{{.number}} {{.title}}{{range .assignees}} @{{.login}}{{end}}{{"\n"}}{{end}}' 2>/dev/null \
    || echo "  (gh could not list issues)"
fi
echo "Next: read NOTES.md and status/*.md before starting work."
