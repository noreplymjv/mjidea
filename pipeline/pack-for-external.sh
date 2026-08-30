#!/usr/bin/env bash
# Pack a seed/pending draft for Chrome AIs or external agents.
# Usage: ./pipeline/pack-for-external.sh <slug>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <slug>"
  echo "Example: $0 trust-isnt-certified"
  exit 1
fi

OUT_DIR="$ROOT/exports"
mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/${SLUG}-external-pack.md"
DATE="$(date +%Y-%m-%d)"

# Resolve source: pending > inbox match > blog
SRC=""
if [[ -f "$ROOT/drafts/pending/${SLUG}.md" ]]; then
  SRC="$ROOT/drafts/pending/${SLUG}.md"
elif ls "$ROOT/inbox/"*"${SLUG}"*.md >/dev/null 2>&1; then
  SRC="$(ls "$ROOT/inbox/"*"${SLUG}"*.md | head -1)"
elif [[ -f "$ROOT/site/src/content/blog/${SLUG}.md" ]]; then
  SRC="$ROOT/site/src/content/blog/${SLUG}.md"
else
  echo "No file found for slug: $SLUG (checked pending, inbox, blog)"
  exit 1
fi

RESEARCH=""
if ls "$ROOT/reports/research/"*"${SLUG}"*.md >/dev/null 2>&1; then
  RESEARCH="$(ls "$ROOT/reports/research/"*"${SLUG}"*.md | tail -1)"
fi

{
  echo "# Mjidea external pack — ${SLUG}"
  echo ""
  echo "- Packed: ${DATE}"
  echo "- Source: \`${SRC#"$ROOT"/}\`"
  echo "- Return improved essay to: \`drafts/pending/${SLUG}.md\`"
  echo "- Do not invent citation URLs"
  echo ""
  echo "---"
  echo ""
  echo "## Voice rules (must follow)"
  echo ""
  cat "$ROOT/brand/VOICE.md"
  echo ""
  echo "---"
  echo ""
  echo "## Master instruction"
  echo ""
  echo "See also \`prompts/EXTERNAL-AI-PACK.md\` in the project."
  echo "Produce: Essay + References + Diff + Image briefs."
  echo ""
  echo "---"
  echo ""
  echo "## Source material"
  echo ""
  cat "$SRC"
  if [[ -n "$RESEARCH" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## Existing research (if any)"
    echo ""
    cat "$RESEARCH"
  fi
  echo ""
  echo "---"
  echo ""
  echo "## Image brief reminder"
  echo ""
  echo "After the essay, give 2 image prompts (cover + infographic). Style guide: \`prompts/IMAGE-INFOGRAPHIC.md\`."
} > "$OUT"

echo "Wrote: $OUT"
echo "Next: upload/paste into Perplexity (facts) then Claude/Gemini (voice), or one strong chat."
echo "Prompts: $ROOT/prompts/EXTERNAL-AI-PACK.md"
