#!/usr/bin/env bash
# Shared helpers for Mjidea pipeline scripts
# shellcheck disable=SC2034

mjidea_root() {
  cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd
}

mjidea_slugify() {
  local s="$1"
  echo "$s" \
    | sed 's/\.md$//' \
    | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//' \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9-]/-/g; s/--*/-/g; s/^-//; s/-$//'
}

# Score idea text against TOPIC-ROUTING keywords; print topic id
mjidea_route_topic() {
  local text
  text="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
  local best="philosophy"
  local best_score=0

  score_topic() {
    local topic="$1"
    shift
    local score=0
    local kw
    for kw in "$@"; do
      if echo "$text" | grep -qF "$kw"; then
        score=$((score + 1))
      fi
    done
    if [[ $score -gt $best_score ]]; then
      best_score=$score
      best=$topic
    fi
  }

  score_topic trust "trust" "certified" "certificate" "badge" "stamp" "verified" "provenance" "honesty" "label" "organic"
  score_topic privacy "privacy" "local-first" "local first" "cookie" "consent" "surveillance" "track"
  score_topic marketing "marketing" "rory" "perception" "behavioral" "behaviour" "signalling" "placebo" "satnav" "stopwatch" "irrational"
  score_topic product "product" "ux" "interface" "shipping" "roadmap" "feature"
  score_topic ai "ai" "agent" "hallucination" "llm" "self-check" "verify everything" "parallel minds"
  score_topic health "health" "spice" "pinch" "supplement" "wellness" "food" "taste" "nature"
  score_topic seo "seo" "serp" "ranking" "discoverability"
  score_topic growth "growth" "newsletter" "distribution" "viral" "community"
  score_topic security "security" "threat" "csp" "xss" "vulnerability" "headers"
  score_topic philosophy "philosophy" "meaning" "moral" "belief" "essay" "loneliness" "attention" "wisdom"

  echo "$best"
}

mjidea_squad_for_topic() {
  local topic="$1"
  case "$topic" in
    trust)
      cat <<'EOF'
- Genius Panel: GP-01 Rowan Quill, GP-02 Selene Park, GP-03 Theo Marsh, GP-04 Iris Cole, GP-05 Jonah Reed (+ GP-06 Ava Shore)
- Content: CN-01…CN-06 (Drew Fontaine claim-check lead)
- SEO: SE-01…SE-05
- Growth: GR-01…GR-05 (+ GR-02 Eli shareability)
- Security: SC-01 Vera Knox, SC-02 Omar Siddiq, SC-03 Paige Quinn (privacy/trust theater)
- Audit: AU-01 Helena Orth, AU-03 Rae Kim, AU-05 Sky Mendel
- PM: EX-02 Mira Vance · War Room: EX-03 Kai Ortega · CoS: EX-04 Jules Haber
EOF
      ;;
    privacy)
      cat <<'EOF'
- Genius Panel: GP-01…GP-05 (+ GP-04 Iris antifragile lead)
- Content: CN-01…CN-05
- SEO: SE-01…SE-05
- Growth: GR-01…GR-05
- Security: SC-01…SC-05 (Paige SC-03 lead)
- Engineering: EN-01 Alex Ruiz, EN-03 Robin Vale
- Audit: AU-01, AU-03, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    marketing)
      cat <<'EOF'
- Genius Panel: GP-01 Rowan Quill (lead), GP-02, GP-03 Theo Marsh, GP-05, GP-06 Ava Shore
- Content: CN-01…CN-05 (Priya CN-03 narrative)
- SEO: SE-01…SE-05 (+ SE-03 Gia SERP psychology)
- Growth: GR-01…GR-05
- Security: SC-01…SC-03
- Audit: AU-01, AU-03, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    product)
      cat <<'EOF'
- Genius Panel: GP-01…GP-05 (+ GP-03 remarkable)
- Content: CN-01…CN-05
- SEO: SE-01…SE-05
- Growth: GR-01…GR-05
- Design: DS-01…DS-05
- Engineering: EN-01…EN-03
- Security: SC-01…SC-03
- Audit: AU-01, AU-03, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    ai)
      cat <<'EOF'
- Genius Panel: GP-01…GP-05 (+ GP-07 Nix, GP-02 Selene)
- Content: CN-01…CN-06 (Drew lead on claims)
- SEO: SE-01…SE-05
- Growth: GR-01…GR-05
- Security: SC-01, SC-02 Omar Siddiq, SC-03
- Engineering: EN-04 Jamie Orth
- Audit: AU-01, AU-03, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    health)
      cat <<'EOF'
- Genius Panel: GP-01 Rowan Quill, GP-02…GP-05
- Content: CN-01…CN-06 (no medical claims without cites)
- SEO: SE-01…SE-05
- Growth: GR-01…GR-05 (+ GR-06 Zoe)
- Security: SC-01…SC-03
- Audit: AU-01, AU-03 Rae Kim, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    seo)
      cat <<'EOF'
- Genius Panel: GP-01…GP-05
- Content: CN-01 Elena Voss + CN-02…CN-05
- SEO: SE-01…SE-06 (full)
- Growth: GR-01…GR-05 (+ GR-05 Quinn)
- Security: SC-01…SC-03
- Audit: AU-01, AU-04 Pat Okonkwo, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    growth)
      cat <<'EOF'
- Genius Panel: GP-01…GP-05 (+ GP-03 Theo)
- Content: CN-01…CN-05
- SEO: SE-01…SE-05 (+ SE-02 Owen)
- Growth: GR-01…GR-06
- Security: SC-01…SC-03
- Audit: AU-01, AU-03, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    security)
      cat <<'EOF'
- Genius Panel: GP-01…GP-05
- Content: CN-01…CN-05
- SEO: SE-01…SE-05
- Growth: GR-01…GR-05
- Security: SC-01…SC-06 (full)
- Engineering: EN-02 Casey Ng
- Audit: AU-01, AU-02 Vic Lang, AU-05
- PM: EX-02 · War Room: EX-03 · CoS: EX-04
EOF
      ;;
    *)
      cat <<'EOF'
- Genius Panel: GP-01…GP-05 (+ GP-07 Nix optional)
- Content: CN-01…CN-05 (+ CN-02 Marcus philosopher)
- SEO: SE-01…SE-05
- Growth: GR-01…GR-05
- Security: SC-01…SC-03
- Audit: AU-01, AU-03, AU-05
- PM: EX-02 Mira Vance · War Room: EX-03 Kai Ortega · CoS: EX-04 Jules Haber
EOF
      ;;
  esac
}

mjidea_resolve_source() {
  # Args: root, input (slug|path|all handled elsewhere)
  # Sets: SRC, SLUG, TITLE_HINT
  local ROOT="$1"
  local IN="$2"
  SRC=""
  SLUG=""
  TITLE_HINT=""

  if [[ -z "$IN" ]]; then
    return 1
  fi

  if [[ -f "$IN" ]]; then
    SRC="$IN"
  elif [[ -f "$ROOT/inbox/$IN" ]]; then
    SRC="$ROOT/inbox/$IN"
  elif [[ -f "$ROOT/inbox/${IN}.md" ]]; then
    SRC="$ROOT/inbox/${IN}.md"
  else
    # Find by slug substring in inbox
    local hit
    hit="$(ls -1 "$ROOT/inbox/"*.md 2>/dev/null | grep -i "$IN" | grep -v TEMPLATE | head -1 || true)"
    if [[ -n "$hit" && -f "$hit" ]]; then
      SRC="$hit"
    else
      # Already have brief only?
      if [[ -f "$ROOT/war-room/briefs/${IN}.md" ]]; then
        SLUG="$(mjidea_slugify "$IN")"
        SRC="$ROOT/war-room/briefs/${SLUG}.md"
        TITLE_HINT="$SLUG"
        return 0
      fi
      return 1
    fi
  fi

  local base
  base="$(basename "$SRC" .md)"
  SLUG="$(mjidea_slugify "$base")"
  TITLE_HINT="$(grep -m1 '^# ' "$SRC" 2>/dev/null | sed 's/^# //' || echo "$SLUG")"
  return 0
}
