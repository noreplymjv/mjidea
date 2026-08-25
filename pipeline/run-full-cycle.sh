#!/usr/bin/env bash
# Marks cycle artifacts and reminds agent to execute all war-room phases.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "Usage: ./pipeline/run-full-cycle.sh <slug>" >&2
  exit 1
fi
BRIEF="$ROOT/war-room/briefs/${SLUG}.md"
OUT="$ROOT/war-room/output"
mkdir -p "$OUT"

if [[ ! -f "$BRIEF" ]]; then
  echo "Missing brief: $BRIEF" >&2
  echo "Run: ./pipeline/ceo-idea.sh inbox/<file>.md" >&2
  exit 1
fi

# Ensure stub artifact files exist so the agent fills them
for ext in draft seo growth security audit; do
  f="$OUT/${SLUG}.${ext}.md"
  if [[ ! -f "$f" ]]; then
    printf '# %s — %s\n\n_(War room filling this…)_ \n' "$SLUG" "$ext" > "$f"
  fi
done

# Social stub
mkdir -p "$ROOT/social/scripts"
if [[ ! -f "$ROOT/social/scripts/${SLUG}.md" ]]; then
  cat > "$ROOT/social/scripts/${SLUG}.md" <<EOF
# Social / Video stub — $SLUG

Phase 2. After blog ships, Video team (VD-01…VD-05) expands:

- 60s spoken essay
- 3 hook variants
- On-screen text beats
- Thumbnail concept
EOF
fi

cat <<EOF
════════════════════════════════════════════
 Mjidea FULL CYCLE — $SLUG
════════════════════════════════════════════
Brief:     $BRIEF
Protocol:  team/war-rooms/PROTOCOL.md
Roster:    team/ROSTER.md
Voice:     brand/VOICE.md

Agent: execute phases 1–10 NOW without asking.
Fill:  $OUT/${SLUG}.*.md
Then:  STOP at drafts/pending — Mj runs ./pipeline/approve.sh $SLUG
       (Do not use publish-draft.sh until approved.)
════════════════════════════════════════════
EOF
