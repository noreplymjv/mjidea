#!/usr/bin/env bash
# ==============================================================================
# Mjidea Push-Thought Engine
# Transforms any raw thought or voice note into:
# 1. Researched Blog Essay (with Rory Sutherland behavioral framing & citations)
# 2. 60-second Viral Reel / Video Storyboard
# 3. Omnichannel Social Pack (LinkedIn, X/Twitter, Instagram, YouTube Shorts)
# 4. Local / Cloud n8n Webhook & Scheduler Queue
# ==============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_EXEC="python3"

if [[ $# -eq 0 ]]; then
  echo "Usage: ./pipeline/push-thought.sh \"<your raw thought or sentence>\" [options]"
  echo "   or: ./pipeline/push-thought.sh inbox/<file.md>"
  echo ""
  echo "Examples:"
  echo "  ./pipeline/push-thought.sh \"Why patience is the rarest asymmetric advantage in business\""
  echo "  ./pipeline/push-thought.sh inbox/2026-08-21-sell-story-not-commodity.md"
  echo "  ./pipeline/push-thought.sh \"Patience as asymmetric asset\" --webhook"
  exit 1
fi

RAW_INPUT="$1"
shift || true

echo "================================================================="
echo "🧠 Mjidea Thought-to-Omnichannel Engine"
echo "================================================================="

$PYTHON_EXEC "$ROOT/pipeline/thought_to_omnichannel.py" "$RAW_INPUT" "$@"
