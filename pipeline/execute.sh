#!/usr/bin/env bash
# Execute prep: route topic → research stub → pending draft stub → war-room brief
# Does NOT publish. Agent fills research + draft after this (or in same session).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/common.sh
source "$ROOT/pipeline/lib/common.sh"

TARGET="${1:-}"
DATE="$(date +%Y-%m-%d)"
TS="$(date -Iseconds)"

usage() {
  cat >&2 <<EOF
Usage: ./pipeline/execute.sh <slug|inbox-file|all-pending>

  Prepares one idea (or all pending) for the expert cycle.
  Writes brief, research stub, pending draft stub.
  Does NOT publish — Mj must approve later.

Examples:
  ./pipeline/execute.sh trust-isnt-certified
  ./pipeline/execute.sh inbox/2026-08-21-trust-isnt-certified.md
  ./pipeline/execute.sh all-pending
EOF
  exit 1
}

[[ -z "$TARGET" ]] && usage

mkdir -p \
  "$ROOT/war-room/briefs" "$ROOT/war-room/output" \
  "$ROOT/drafts/pending" "$ROOT/drafts/approved" "$ROOT/drafts/rejected" \
  "$ROOT/reports/research" "$ROOT/reports/ceo" "$ROOT/reports/war-room"

execute_one() {
  local IN="$1"
  local SRC TITLE_HINT RAW TOPIC SQUAD BRIEF RESEARCH PENDING WAR_DRAFT
  # SLUG is intentionally global so STATUS block after execute_one can use it

  if ! mjidea_resolve_source "$ROOT" "$IN"; then
    echo "Could not resolve idea: $IN" >&2
    return 1
  fi

  RAW="$(cat "$SRC")"
  TOPIC="$(mjidea_route_topic "$RAW")"
  SQUAD="$(mjidea_squad_for_topic "$TOPIC")"
  BRIEF="$ROOT/war-room/briefs/${SLUG}.md"
  RESEARCH="$ROOT/reports/research/${DATE}-${SLUG}.md"
  PENDING="$ROOT/drafts/pending/${SLUG}.md"
  WAR_DRAFT="$ROOT/war-room/output/${SLUG}.draft.md"

  # Brief: create if missing; refresh only if still a stub (agent fills)
  if [[ ! -f "$BRIEF" ]] || grep -q "_(agent fills)_" "$BRIEF" 2>/dev/null; then
  {
    echo "# Brief — $SLUG"
    echo
    echo "- Opened / refreshed: $TS"
    echo "- PM: Mira Vance"
    echo "- War Room Director: Kai Ortega"
    echo "- Topic pack: **$TOPIC** (see \`team/TOPIC-ROUTING.md\`)"
    echo "- Mode: EXECUTE → draft pending (NO auto-publish)"
    echo "- Source: \`$SRC\`"
    echo
    echo "## CEO raw idea"
    echo
    cat "$SRC"
    echo
    echo "## Expert squad"
    echo
    echo "$SQUAD"
    echo
    echo "## EXECUTE checklist"
    echo
    echo "- [ ] 0 Research + citations (\`team/war-rooms/09-research-citations.md\`)"
    echo "- [ ] 1 Genius reframes (≥5)"
    echo "- [ ] 2 Angle lock"
    echo "- [ ] 3 Draft (human voice)"
    echo "- [ ] 4 Humanize (Elena Voss)"
    echo "- [ ] 5 SEO pack → \`reports/seo/\`"
    echo "- [ ] 6 Growth pack → \`reports/growth/\`"
    echo "- [ ] 7 Security → \`reports/security/\`"
    echo "- [ ] 8 Audit gate → \`reports/audit/\`"
    echo "- [ ] 9 Write publish-ready draft to \`drafts/pending/${SLUG}.md\`"
    echo "- [ ] 10 **STOP** — wait for Mj: \`./pipeline/approve.sh ${SLUG}\`"
    echo
    echo "## Genius reframes"
    echo
    echo "_(agent fills)_"
    echo
    echo "## Chosen angle"
    echo
    echo "_(agent fills)_"
    echo
    echo "## Status"
    echo
    echo "**PENDING MJ APPROVAL** after draft — do not publish from execute."
  } > "$BRIEF"
  fi

  # Research stub (agent must fill via web search)
  if [[ ! -f "$RESEARCH" ]]; then
    cat > "$RESEARCH" <<EOF
# Research — $SLUG

- Date: $DATE
- Topic pack: $TOPIC
- Status: STUB — agent must web-search and fill

## Search queries used
- _(agent fills)_

## Key findings
1. _(AGENT MUST FILL via web search)_ — Source: [Title](URL) — Accessed: $DATE — Notes: …

## Disputed / weak
- _(agent fills)_

## Quotes worth using (verbatim only if sourced)
- _(none until sourced)_

## AGENT MUST FILL via web search

Do not invent URLs. Prefer primary sources. Every factual claim in the pending draft needs a reference here first.
EOF
  fi

  # Pending draft scaffold — never overwrite non-scaffold drafts
  if [[ ! -f "$PENDING" ]] || grep -q "STATUS: SCAFFOLD" "$PENDING" 2>/dev/null; then
      cat > "$PENDING" <<EOF
---
title: "$TITLE_HINT"
description: ""
pubDate: $DATE
tags: ["$TOPIC"]
draft: true
thesis: ""
status: pending-approval
---

<!-- STATUS: SCAFFOLD — agent replaces with publish-ready prose + References -->

# $TITLE_HINT

_(Draft scaffold. Expert team writes full essay here after research.)_

## References

1. _(AGENT MUST FILL via web search — URL + title + date accessed)_
EOF
  fi

  # War-room draft mirror stub
  if [[ ! -f "$WAR_DRAFT" ]]; then
    printf '# %s — draft (mirror)\n\nSee `drafts/pending/%s.md` — canonical pending file.\n' "$SLUG" "$SLUG" > "$WAR_DRAFT"
  fi

  # Mirror brief into reports/war-room
  cp "$BRIEF" "$ROOT/reports/war-room/${DATE}-${SLUG}-brief.md"

  # Status queue line (append-style rewrite of active section via marker file)
  mkdir -p "$ROOT/pipeline/.state"
  echo "$SLUG|execute-prep|$TOPIC|pending-draft" >> "$ROOT/pipeline/.state/queue.log"

  cat <<EOF

════════════════════════════════════════════
 Mjidea EXECUTE PREP — $SLUG
════════════════════════════════════════════
Topic:     $TOPIC
Brief:     $BRIEF
Research:  $RESEARCH
Pending:   $PENDING
Routing:   team/TOPIC-ROUTING.md
Citations: team/war-rooms/09-research-citations.md

Cursor prompt (paste / say):

  Execute Mjidea job $SLUG

Agent: research (web) → expert war room → write drafts/pending/$SLUG.md
       DO NOT publish. Mj approves with: ./pipeline/approve.sh $SLUG
════════════════════════════════════════════
EOF
}

if [[ "$TARGET" == "all-pending" ]]; then
  exec "$ROOT/pipeline/complete-pending.sh" --execute-prep
fi

execute_one "$TARGET"

# Light STATUS bump
STATUS="$ROOT/team/STATUS.md"
{
  echo "# Status Board"
  echo
  echo "Last updated: $TS"
  echo
  echo "## Mode"
  echo
  echo "**EXECUTE → PENDING APPROVAL** (no auto-publish)"
  echo
  echo "## Local site"
  echo
  echo "**http://127.0.0.1:4321/** — \`cd site && ASTRO_TELEMETRY_DISABLED=1 npx astro preview --host 0.0.0.0 --port 4321\`"
  echo
  echo "## Queue"
  echo
  echo "| Slug | Phase | Owner | Status |"
  echo "|------|-------|-------|--------|"
  echo "| $SLUG | Research→Draft | Kai Ortega | ACTIVE — pending Mj approve |"
  echo
  echo "## Approval gate"
  echo
  echo "Publish only via \`./pipeline/approve.sh <slug>\` or CEO saying \`approve <slug>\`."
  echo
  echo "## Last shipped"
  echo
  echo "_See \`site/src/content/blog/\` and \`published/\`_"
  echo
  echo "## Blockers needing CEO"
  echo
  echo "- Review \`drafts/pending/\` and approve or reject."
} > "$STATUS"
