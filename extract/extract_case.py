"""Claude extraction: a document's text -> candidate facts for a person to verify.

    python3 extract/extract_case.py DOC.txt --doc "Santa Ana Housing Division Quarterly Report FY2026-27 Q1" \
        --url https://santa-ana.gov/documents/housing-division-quarterly-report-fy-2026-27-q1/ \
        --date 2026-11-03 --out extract/out/q1-27.json
    python3 extract/extract_case.py DOC.txt --doc ... --url ... --date ... --dry-run   # no API call

Input is plain text (copy it out of the PDF). Needs ANTHROPIC_API_KEY in the environment.
Output is NEVER written into data/cases/. Every candidate needs a human to check it before it
is copied into a case file and marked verified in docs/project/evidence.md.

Safety checks on the model's answer:
- every quote must appear verbatim in the document text (whitespace-insensitive), or the fact
  is downgraded to "unknown" with reason "quote_not_found";
- quotes over 15 words are downgraded the same way;
- a conflict between two quotes makes the fact "unknown".
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPT_PATH = HERE / "prompt.md"
MAX_CHARS = 150000  # bounded input; longer documents are cut and flagged
DEFAULT_MODEL = "claude-sonnet-5-5"
TIMEOUT_SECONDS = 120


def normalize(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def build_message(prompt, doc_text):
    return prompt + "\n\n<document>\n" + doc_text + "\n</document>"


def call_claude(message, model):
    import anthropic  # only needed for a live call

    client = anthropic.Anthropic(timeout=TIMEOUT_SECONDS)
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        messages=[{"role": "user", "content": message}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def parse_json(reply):
    # Accept a bare object or one wrapped in a ```json fence.
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    if not match:
        raise ValueError("model reply contained no JSON object")
    return json.loads(match.group(0))


def to_candidates(model_facts, doc_text, doc, url, date):
    """Check each model answer against the document and shape it like a contract Fact."""
    haystack = normalize(doc_text)
    candidates = {}
    for name, f in model_facts.items():
        quote = (f.get("quote") or "").strip()
        conflict = f.get("conflict") or []
        reason = None
        if conflict:
            reason = "sources_conflict"
        elif not f.get("found") or f.get("value") is None:
            reason = "not_found_in_document"
        elif len(quote.split()) > 15:
            reason = "quote_too_long"
        elif not quote or normalize(quote) not in haystack:
            reason = "quote_not_found"

        fact = {"needs_human_check": True, "quote": quote, "conflict": conflict}
        if reason:
            fact.update({"value": None, "status": "unknown", "reason": reason,
                         "model_value": f.get("value")})
        else:
            fact.update({"value": f["value"], "status": "sourced",
                         "source": {"doc": doc, "locator": f.get("locator") or "", "url": url, "date": date}})
            if f.get("as_of"):
                fact["as_of"] = f["as_of"]
        candidates[name] = fact
    return candidates


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text_file", help="plain-text copy of one public document")
    ap.add_argument("--doc", required=True, help="document title, e.g. 'Habitat OC FY2025 audit'")
    ap.add_argument("--url", required=True, help="public URL of the document")
    ap.add_argument("--date", required=True, help="date of the document, YYYY-MM-DD")
    ap.add_argument("--out", help="where to write candidate JSON (default: print)")
    ap.add_argument("--model", default=os.environ.get("CLAUDE_MODEL", DEFAULT_MODEL))
    ap.add_argument("--dry-run", action="store_true", help="build the request, do not call the API")
    args = ap.parse_args()

    if args.out and Path(args.out).resolve().parent.name == "cases":
        sys.exit("Refusing to write into data/cases/: candidates must be checked by a person first.")

    doc_text = Path(args.text_file).read_text(encoding="utf-8", errors="replace")
    truncated = len(doc_text) > MAX_CHARS
    doc_text = doc_text[:MAX_CHARS]
    message = build_message(PROMPT_PATH.read_text(encoding="utf-8"), doc_text)

    if args.dry_run:
        print("Dry run: %d characters of document%s, model %s. No API call made."
              % (len(doc_text), " (TRUNCATED)" if truncated else "", args.model))
        return 0
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Put it in your environment (never in git), or use --dry-run.")

    try:
        reply = call_claude(message, args.model)
        model_facts = parse_json(reply).get("facts", {})
    except Exception as exc:  # network, auth, bad JSON: say so plainly, write nothing
        sys.exit("Extraction failed: %s" % exc)

    result = {
        "about": "CANDIDATE facts extracted by Claude. Not verified. A person must check every quote "
                 "against the document before copying anything into data/cases/.",
        "document": {"doc": args.doc, "url": args.url, "date": args.date, "truncated": truncated},
        "model": args.model,
        "facts": to_candidates(model_facts, doc_text, args.doc, args.url, args.date),
    }
    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        found = sum(1 for f in result["facts"].values() if f["status"] == "sourced")
        print("Wrote %s: %d candidate facts with verified quotes, %d unknown."
              % (args.out, found, len(result["facts"]) - found))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
