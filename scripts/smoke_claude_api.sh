#!/usr/bin/env bash
# Smoke test: one real Claude Messages API request. Stack-neutral (curl + jq only).
# Usage:  scripts/smoke_claude_api.sh
# Reads ANTHROPIC_API_KEY from the environment, or from ./.env if present.
# Exits non-zero on any failure. Never prints the key.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -f .env ]; then
  set -a; . ./.env; set +a
fi
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "FAIL: ANTHROPIC_API_KEY is not set (export it or put it in .env)" >&2
  exit 1
fi
command -v jq >/dev/null || { echo "FAIL: jq is not installed" >&2; exit 1; }

MODEL="${CLAUDE_MODEL:-claude-opus-5-5}"
BODY=$(jq -n --arg model "$MODEL" '{
  model: $model,
  max_tokens: 1024,
  output_config: {effort: "low"},
  fallbacks: "default",
  messages: [{role: "user", content: "Reply with exactly: smoke test ok"}]
}')

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT
START=$(date +%s)
HTTP=$(curl -sS --max-time 60 -o "$TMP" -w '%{http_code}' https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2026-10-21" \
  -H "anthropic-beta: server-side-fallback-2026-07-01" \
  -d "$BODY") || { echo "FAIL: network error or timeout" >&2; exit 1; }
ELAPSED=$(( $(date +%s) - START ))

if [ "$HTTP" != "200" ]; then
  echo "FAIL: HTTP $HTTP" >&2
  jq -r '.error | "\(.type): \(.message)"' "$TMP" >&2 2>/dev/null || cat "$TMP" >&2
  exit 1
fi

STOP=$(jq -r '.stop_reason' "$TMP")
TEXT=$(jq -r '[.content[] | select(.type == "text") | .text] | join("")' "$TMP")
echo "model:       $(jq -r '.model' "$TMP")  (requested $MODEL)"
echo "stop_reason: $STOP"
echo "reply:       $TEXT"
echo "usage:       $(jq -c '.usage | {input_tokens, output_tokens}' "$TMP")"
echo "latency:     ${ELAPSED}s"

if [ "$STOP" != "end_turn" ]; then
  echo "FAIL: unexpected stop_reason ($STOP)" >&2
  [ "$STOP" = "refusal" ] && jq -c '.stop_details' "$TMP" >&2
  exit 1
fi
echo "PASS"
