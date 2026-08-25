#!/usr/bin/env bash
# Reject a pending draft with optional reason
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/common.sh
source "$ROOT/pipeline/lib/common.sh"

SLUG_IN="${1:-}"
REASON="${2:-No reason given}"
DATE="$(date +%Y-%m-%d)"
TS="$(date -Iseconds)"

if [[ -z "$SLUG_IN" ]]; then
  echo "Usage: ./pipeline/reject.sh <slug> [reason]" >&2
  exit 1
fi

SLUG="$(mjidea_slugify "$SLUG_IN")"
PENDING="$ROOT/drafts/pending/${SLUG}.md"
REJECT_DIR="$ROOT/drafts/rejected"
mkdir -p "$REJECT_DIR" "$ROOT/reports/ceo"

if [[ ! -f "$PENDING" ]]; then
  echo "No pending draft: $PENDING" >&2
  exit 1
fi

DEST="$REJECT_DIR/${SLUG}.md"
{
  echo "<!-- REJECTED: $TS -->"
  echo "<!-- Reason: $REASON -->"
  echo
  cat "$PENDING"
} > "$DEST"

rm -f "$PENDING"

{
  echo "# Rejected — $SLUG"
  echo
  echo "- When: $TS"
  echo "- Reason: $REASON"
  echo "- File: \`drafts/rejected/${SLUG}.md\`"
} > "$ROOT/reports/ceo/${DATE}-${SLUG}-rejected.md"

# Soft STATUS note
if [[ -f "$ROOT/team/STATUS.md" ]]; then
  printf '\n## Last rejection\n\n- `%s` — %s (%s)\n' "$SLUG" "$REASON" "$DATE" >> "$ROOT/team/STATUS.md"
fi

echo "Rejected: $DEST"
echo "Reason:   $REASON"
echo "CEO note: $ROOT/reports/ceo/${DATE}-${SLUG}-rejected.md"
