#!/usr/bin/env bash
# Promote an APPROVED draft into Astro content collection.
# Prefer: ./pipeline/approve.sh <slug> (moves pending → approved → site).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DRAFT="${1:-}"
if [[ -z "$DRAFT" || ! -f "$DRAFT" ]]; then
  echo "Usage: ./pipeline/publish-draft.sh war-room/output/<slug>.draft.md" >&2
  echo "Prefer: ./pipeline/approve.sh <slug> (approval-gated path)." >&2
  exit 1
fi

# Soft gate: warn if publishing from pending without approve.sh
case "$DRAFT" in
  *drafts/pending*)
    echo "Refusing: publish from drafts/pending is blocked. Use ./pipeline/approve.sh <slug>" >&2
    exit 1
    ;;
esac

DEST_DIR="$ROOT/site/src/content/blog"
mkdir -p "$DEST_DIR" "$ROOT/published"

BASE="$(basename "$DRAFT" .draft.md)"
BASE="$(basename "$BASE" .md)"
DEST="$DEST_DIR/${BASE}.md"

# Validate frontmatter presence and structure
if ! head -n 1 "$DRAFT" | grep -q "^---$"; then
  echo "Error: Draft is missing starting frontmatter marker '---'" >&2
  exit 1
fi

if ! tail -n +2 "$DRAFT" | grep -n -m 1 "^---$" | grep -q "^[0-9]\+:"; then
  echo "Error: Draft is missing closing frontmatter marker '---'" >&2
  exit 1
fi

if ! head -n 15 "$DRAFT" | grep -q "^title:"; then
  echo "Error: Draft is missing required frontmatter field 'title:'" >&2
  exit 1
fi

cp "$DRAFT" "$DEST"
cp "$DRAFT" "$ROOT/published/$(date +%Y%m%d)-${BASE}.md"

echo "Published to site: $DEST"
echo "Archived: $ROOT/published/$(date +%Y%m%d)-${BASE}.md"
echo "Preview: cd site && npm run preview"
