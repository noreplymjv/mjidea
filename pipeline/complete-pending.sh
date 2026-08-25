#!/usr/bin/env bash
# List unfinished work; optionally run execute prep for each
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/common.sh
source "$ROOT/pipeline/lib/common.sh"

DO_PREP=0
if [[ "${1:-}" == "--execute-prep" ]]; then
  DO_PREP=1
fi

DATE="$(date +%Y-%m-%d)"
TS="$(date -Iseconds)"

mkdir -p "$ROOT/pipeline/.state" "$ROOT/drafts/pending" "$ROOT/reports/ceo"

echo "════════════════════════════════════════════"
echo " Mjidea COMPLETE PENDING — queue"
echo "════════════════════════════════════════════"
echo "Scanned: $TS"
echo

PENDING_LIST=()

# Inbox ideas not yet in drafts/pending or site blog
echo "## Inbox (ready floats)"
shopt -s nullglob
for f in "$ROOT/inbox/"*.md; do
  base="$(basename "$f")"
  [[ "$base" == _* ]] && continue
  [[ "$base" == IMPORT-LOG.md || "$base" == HARVEST-MERGE.md ]] && continue
  slug="$(mjidea_slugify "$base")"
  if [[ -f "$ROOT/site/src/content/blog/${slug}.md" ]]; then
    continue
  fi
  if [[ -f "$ROOT/drafts/approved/${slug}.md" ]]; then
    continue
  fi
  status="inbox"
  if [[ -f "$ROOT/drafts/pending/${slug}.md" ]]; then
    if grep -q "STATUS: SCAFFOLD\|DRAFT SCAFFOLD\|_(agent fills\|AGENT MUST FILL" "$ROOT/drafts/pending/${slug}.md" 2>/dev/null; then
      status="pending-scaffold"
    else
      status="pending-review"
    fi
  fi
  echo "- [$status] $slug  ←  $base"
  PENDING_LIST+=("$f")
done
echo

# Issues mirrors (optional)
echo "## Issues (current/future markdown)"
for dir in "$ROOT/issues/current" "$ROOT/issues/future"; do
  [[ -d "$dir" ]] || continue
  for f in "$dir"/*.md; do
    [[ -f "$f" ]] || continue
    base="$(basename "$f")"
    [[ "$base" == _* || "$base" == README.md ]] && continue
    slug="$(mjidea_slugify "$base")"
    echo "- [issue] $slug  ←  $f"
    PENDING_LIST+=("$f")
  done
done
if [[ -d "$ROOT/site/src/content/issues" ]]; then
  echo "(Site issues collection exists — treat CEO adds as inbox via /issues/ UI; pipeline uses inbox/ + issues/ folders.)"
fi
echo

echo "## Drafts awaiting approval"
for f in "$ROOT/drafts/pending/"*.md; do
  [[ -f "$f" ]] || continue
  slug="$(basename "$f" .md)"
  if grep -q "STATUS: SCAFFOLD\|AGENT MUST FILL" "$f" 2>/dev/null; then
    echo "- [scaffold] $slug"
  else
    echo "- [ready for Mj] $slug"
  fi
done
echo

mapfile -t PENDING_LIST < <(printf '%s\n' "${PENDING_LIST[@]:-}" | awk 'NF && !seen[$0]++')

QUEUE_FILE="$ROOT/pipeline/.state/complete-pending-queue.txt"
{
  echo "# Generated $TS"
  for p in "${PENDING_LIST[@]:-}"; do
    echo "$p"
  done
} > "$QUEUE_FILE"

CEO_NOTE="$ROOT/reports/ceo/${DATE}-complete-pending-queue.md"
{
  echo "# Complete-pending queue"
  echo
  echo "- Generated: $TS"
  echo "- Count: ${#PENDING_LIST[@]}"
  echo
  echo "## Agent instruction"
  echo
  echo "When CEO says **complete my pending ideas/issues/thoughts** or **complete pending**:"
  echo
  echo "1. Read this queue (\`$QUEUE_FILE\`)."
  echo "2. For each item: \`./pipeline/execute.sh <path>\` then run full research + expert war room."
  echo "3. Write publish-ready draft to \`drafts/pending/<slug>.md\` with References."
  echo "4. Dual-write reports under \`reports/\`."
  echo "5. **Do not publish** until \`./pipeline/approve.sh <slug>\`."
  echo
  echo "## Items"
  echo
  for p in "${PENDING_LIST[@]:-}"; do
    echo "- \`$p\`"
  done
} > "$CEO_NOTE"

echo "Queue file: $QUEUE_FILE"
echo "CEO report: $CEO_NOTE"
echo
echo "Agent cue: Complete all pending Mjidea jobs from pipeline/.state/complete-pending-queue.txt"
echo "           Stop at drafts/pending/ — approval-gated publish."
echo

if [[ "$DO_PREP" -eq 1 ]]; then
  echo "Running execute prep for each queued item…"
  for p in "${PENDING_LIST[@]:-}"; do
    echo "----"
    "$ROOT/pipeline/execute.sh" "$p" || true
  done
fi
