#!/usr/bin/env bash
# CEO idea intake → war-room brief (auto)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IN="${1:-}"
TS="$(date +%Y%m%d-%H%M%S)"

if [[ -z "$IN" ]]; then
  echo "Usage: ./pipeline/ceo-idea.sh <inbox-file.md|-'text'>" >&2
  exit 1
fi

mkdir -p "$ROOT/inbox" "$ROOT/war-room/briefs" "$ROOT/war-room/output"

if [[ "$IN" == -* ]]; then
  RAW="${IN#-}"
  SRC="$ROOT/inbox/${TS}-ceo-note.md"
  printf '# CEO idea\n\n%s\n' "$RAW" > "$SRC"
else
  if [[ ! -f "$IN" ]]; then
    # allow bare filename in inbox/
    if [[ -f "$ROOT/inbox/$IN" ]]; then
      IN="$ROOT/inbox/$IN"
    else
      echo "File not found: $IN" >&2
      exit 1
    fi
  fi
  SRC="$IN"
fi

# slug from filename or first heading
BASE="$(basename "$SRC" .md)"
BASE="$(echo "$BASE" | sed 's/[^a-zA-Z0-9-]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g;s/^-//;s/-$//')"
SLUG="${BASE:-idea-$TS}"
BRIEF="$ROOT/war-room/briefs/${SLUG}.md"

{
  echo "# Brief — $SLUG"
  echo
  echo "- Opened: $(date -Iseconds)"
  echo "- PM: Mira Vance"
  echo "- War Room Director: Kai Ortega"
  echo "- Mode: AUTO-RUN continuous"
  echo
  echo "## CEO raw idea"
  echo
  cat "$SRC"
  echo
  echo "## Staffing (minimum)"
  echo
  echo "- Genius Panel: GP-01…GP-05+"
  echo "- Content: CN-01…CN-05+"
  echo "- SEO: SE-01…SE-05+"
  echo "- Growth: GR-01…GR-05+"
  echo "- Security: SC-01…SC-03+"
  echo "- Audit: AU-01…AU-05 + PM"
  echo
  echo "## Phases checklist"
  echo
  echo "- [ ] 1 Genius reframes"
  echo "- [ ] 2 Angle lock"
  echo "- [ ] 3 Draft"
  echo "- [ ] 4 Humanize"
  echo "- [ ] 5 SEO pack"
  echo "- [ ] 6 Growth pack"
  echo "- [ ] 7 Security"
  echo "- [ ] 8 Audit gate"
  echo "- [ ] 9 Publish to site"
  echo "- [ ] 10 Social stub"
  echo
  echo "## Genius reframes"
  echo
  echo "_(agent fills)_"
  echo
  echo "## Chosen angle"
  echo
  echo "_(agent fills)_"
} > "$BRIEF"

# status bump
STATUS="$ROOT/team/STATUS.md"
{
  echo "# Status Board"
  echo
  echo "Last updated: $(date -Iseconds)"
  echo
  echo "## Mode"
  echo
  echo "**CONTINUOUS / AUTO-RUN**"
  echo
  echo "## Queue"
  echo
  echo "| Slug | Phase | Owner | Status |"
  echo "|------|-------|-------|--------|"
  echo "| $SLUG | Intake→War Room | Kai Ortega | ACTIVE |"
  echo
  echo "## Last shipped"
  echo
  echo "_See published/ and site/src/content/blog/_|"
  echo
  echo "## Blockers needing CEO"
  echo
  echo "_None._"
} > "$STATUS"

echo "Brief ready: $BRIEF"
echo "Next: In Cursor say — Run full Mjidea war room on $BRIEF"
echo "Or: ./pipeline/run-full-cycle.sh $SLUG"
