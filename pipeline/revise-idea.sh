#!/usr/bin/env bash
# Universal revise / new writing → drafts/pending only (never auto-publish)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

usage() {
  cat >&2 <<EOF
Usage:
  ./pipeline/revise-idea.sh <slug|inbox-path> [--notes "..."] [--notes-file path] [--type TYPE]
  ./pipeline/revise-idea.sh --new "Title" --type columnist [--notes "..."]

Types:
  blog_essay | columnist | journalist | social | short_long
  parenting | money | humanity | life | tech | freeform

Writes pending + research scaffold + CEO one-pager + revise job.
Does NOT publish. Approve: ./pipeline/approve.sh <slug>

Examples:
  ./pipeline/revise-idea.sh kids-pushed-to-race-by-parents --notes "Add play deficit" --type parenting
  ./pipeline/revise-idea.sh trust-isnt-certified --type columnist
  ./pipeline/revise-idea.sh --new "Why boredom is a luxury" --type life --notes "personal scene"
  ./pipeline/revise-idea.sh inbox/2026-08-21-trust-isnt-certified.md
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

exec python3 "$ROOT/pipeline/revise_idea.py" "$@"
