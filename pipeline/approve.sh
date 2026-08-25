#!/usr/bin/env bash
# Approve pending draft → publish to site blog + reports mirror
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/common.sh
source "$ROOT/pipeline/lib/common.sh"

SLUG_IN="${1:-}"
DATE="$(date +%Y-%m-%d)"
TS="$(date -Iseconds)"

if [[ -z "$SLUG_IN" ]]; then
  echo "Usage: ./pipeline/approve.sh <slug>" >&2
  echo "Moves drafts/pending → drafts/approved, publishes to site/src/content/blog/" >&2
  exit 1
fi

SLUG="$(mjidea_slugify "$SLUG_IN")"
PENDING="$ROOT/drafts/pending/${SLUG}.md"
APPROVED_DIR="$ROOT/drafts/approved"
REJECTED_CHECK="$ROOT/drafts/rejected/${SLUG}.md"
DEST_DIR="$ROOT/site/src/content/blog"
WAR_DRAFT="$ROOT/war-room/output/${SLUG}.draft.md"

mkdir -p "$APPROVED_DIR" "$DEST_DIR" "$ROOT/published" "$ROOT/reports/ceo" "$ROOT/reports/war-room"

if [[ ! -f "$PENDING" ]]; then
  # Fallback: war-room draft if pending missing
  if [[ -f "$WAR_DRAFT" ]]; then
    echo "No pending file; using war-room draft: $WAR_DRAFT" >&2
    PENDING="$WAR_DRAFT"
  else
    echo "Missing pending draft: $ROOT/drafts/pending/${SLUG}.md" >&2
    exit 1
  fi
fi

if grep -q "STATUS: SCAFFOLD\|AGENT MUST FILL via web search" "$PENDING" 2>/dev/null; then
  echo "Refusing approve: draft still looks like a scaffold / unfilled research." >&2
  echo "Fill drafts/pending/${SLUG}.md first." >&2
  exit 1
fi

# Ensure frontmatter
if ! head -n 1 "$PENDING" | grep -q "^---$"; then
  echo "Error: Draft missing frontmatter ---" >&2
  exit 1
fi
if ! head -n 20 "$PENDING" | grep -q "^title:"; then
  echo "Error: Draft missing title: in frontmatter" >&2
  exit 1
fi

# Normalize draft:false for publish
TMP="$(mktemp)"
awk '
  BEGIN { in_fm=0; done_fm=0 }
  NR==1 && $0=="---" { in_fm=1; print; next }
  in_fm && $0=="---" {
    if (!seen_draft) print "draft: false"
    in_fm=0; done_fm=1; print; next
  }
  in_fm && /^draft:/ { print "draft: false"; seen_draft=1; next }
  in_fm && /^status:/ { print "status: published"; next }
  { print }
' "$PENDING" > "$TMP"

APPROVED="$APPROVED_DIR/${SLUG}.md"
cp "$TMP" "$APPROVED"
DEST="$DEST_DIR/${SLUG}.md"
cp "$TMP" "$DEST"
cp "$TMP" "$ROOT/published/${DATE}-${SLUG}.md"
cp "$TMP" "$WAR_DRAFT"
rm -f "$TMP"

# Remove from pending
if [[ -f "$ROOT/drafts/pending/${SLUG}.md" ]]; then
  rm -f "$ROOT/drafts/pending/${SLUG}.md"
fi

# Dual-write CEO + war-room publish note
{
  echo "# Approved & published — $SLUG"
  echo
  echo "- Approved: $TS"
  echo "- Site: \`site/src/content/blog/${SLUG}.md\`"
  echo "- Approved archive: \`drafts/approved/${SLUG}.md\`"
  echo "- Published copy: \`published/${DATE}-${SLUG}.md\`"
} > "$ROOT/reports/ceo/${DATE}-${SLUG}-approved.md"
cp "$DEST" "$ROOT/reports/war-room/${DATE}-${SLUG}-published.md"

# STATUS
{
  echo "# Status Board"
  echo
  echo "Last updated: $TS"
  echo
  echo "## Mode"
  echo
  echo "**CONTINUOUS / APPROVAL-GATED PUBLISH**"
  echo
  echo "## Local site"
  echo
  echo "**http://127.0.0.1:4321/** — rebuild/preview after publish to see new post"
  echo
  echo "## Queue"
  echo
  echo "| Slug | Phase | Owner | Status |"
  echo "|------|-------|-------|--------|"
  echo "| $SLUG | Published | Engineering | SHIPPED (Mj approved) |"
  echo
  echo "## Last shipped"
  echo
  echo "- \`$SLUG\` (approved $DATE)"
  echo
  echo "## Blockers needing CEO"
  echo
  echo "_None for this slug._"
} > "$ROOT/team/STATUS.md"

echo "Approved:  $APPROVED"
echo "Published: $DEST"
echo "CEO note:  $ROOT/reports/ceo/${DATE}-${SLUG}-approved.md"
echo "Preview:   http://127.0.0.1:4321/ideas/ (rebuild if needed)"
