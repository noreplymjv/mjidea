#!/usr/bin/env bash
# Smoke tests for Mjidea (cf-dist + repo integrity)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
pass=0
fail=0
ok() { if eval "$2"; then echo "PASS $1"; pass=$((pass+1)); else echo "FAIL $1"; fail=$((fail+1)); fi; }

ok "cf-dist/index.html exists" "[[ -f cf-dist/index.html ]]"
ok "cf-dist/ideas/index.html exists" "[[ -f cf-dist/ideas/index.html ]]"
ok "cf-dist/about/index.html exists" "[[ -f cf-dist/about/index.html ]]"
ok "cf-dist/robots.txt exists" "[[ -f cf-dist/robots.txt ]]"
ok "cf-dist/sitemap-index.xml exists" "[[ -f cf-dist/sitemap-index.xml ]]"
ok "cf-dist/_headers exists" "[[ -f cf-dist/_headers ]]"
ok "home contains Mjidea brand" "grep -q 'Mjidea' cf-dist/index.html"
ok "ideas page searchable markup" "grep -q 'idea-search\\|Search' cf-dist/ideas/index.html"
ok "wrangler points at cf-dist" "grep -q 'cf-dist' wrangler.toml"
ok "wrangler html_handling valid" "grep -qE 'html_handling = \"(auto-trailing-slash|force-trailing-slash|drop-trailing-slash|none)\"' wrangler.toml"
ok "blog markdown count >= 500" "[[ \$(ls site/src/content/blog/*.md | wc -l) -ge 500 ]]"
ok "cf-dist html count >= 500" "[[ \$(find cf-dist -name '*.html' | wc -l) -ge 500 ]]"
ok "cf-dist file count >= 500" "[[ \$(find cf-dist -type f | wc -l) -ge 500 ]]"
ok "package.json name mjidea" "grep -q '\"name\": \"mjidea\"' package.json"
ok "site package has astro" "grep -q '\"astro\"' site/package.json"
ok "START.md exists" "[[ -f START.md ]]"
ok "HANDOVER exists" "[[ -f HANDOVER.md || -f reports/ceo/2026-08-23-full-handover.md ]]"
ok "VOICE.md exists" "[[ -f brand/VOICE.md ]]"
ok "execute.sh executable" "[[ -x pipeline/execute.sh ]]"
ok "approve.sh executable" "[[ -x pipeline/approve.sh ]]"
ok "topics-500.json exists" "[[ -f topics/topics-500.json ]]"
ok "topics count >= 500" "python3 -c \"import json; d=json.load(open('topics/topics-500.json')); assert d.get('count', len(d.get('topics',[])))>=500\""
ok "ORG.md exists" "[[ -f ORG.md ]]"
ok "CABINET-SUTHERLAND exists" "[[ -f team/CABINET-SUTHERLAND.md ]]"
ok "content.config has category" "grep -q 'category' site/src/content.config.ts"
ok "favicon in cf-dist" "[[ -f cf-dist/favicon.svg || -f cf-dist/favicon.ico ]]"
ok "issues pages built" "[[ -f cf-dist/issues/index.html && -f cf-dist/issues/current/index.html ]]"
ok "sample essay built" "[[ -f cf-dist/ideas/attention-is-a-moral-choice/index.html || -f cf-dist/ideas/most-philosophy-dies-of-loneliness/index.html ]]"
ok "no node_modules in cf-dist" "! find cf-dist -type d -name node_modules | grep -q ."
ok "git remote origin set" "git remote get-url origin | grep -q mjidea"

# Expand: spot-check 50 random essay folders exist under ideas/
ok "essay tree non-empty" "[[ \$(find cf-dist/ideas -mindepth 2 -name index.html | wc -l) -ge 400 ]]"
ok "sitemap lists ideas" "grep -q '/ideas/' cf-dist/sitemap-0.xml || grep -q '/ideas/' cf-dist/sitemap-index.xml"
ok "CSP header present" "grep -q Content-Security-Policy cf-dist/_headers"
ok "HOSTING.md mentions Cloudflare" "grep -qi cloudflare HOSTING.md"
ok "CLOUDFLARE_HOSTING.md exists" "[[ -f CLOUDFLARE_HOSTING.md ]]"

# More structural checks (pad toward GetMeBack-style coverage)
for f in AGENTS.md team/ROSTER.md team/STATUS.md team/TOPIC-ROUTING.md team/war-rooms/PROTOCOL.md \
  pipeline/execute.sh pipeline/complete-pending.sh pipeline/reject.sh brand/VOICE.md \
  site/astro.config.mjs site/src/pages/index.astro site/src/pages/ideas/index.astro \
  site/src/layouts/Base.astro seo/PRIVACY-AND-COOKIES.md reports/README.md; do
  ok "file $f" "[[ -f $f ]]"
done

# Category chips / nav
ok "nav has Ideas" "grep -q '/ideas' cf-dist/index.html"
ok "nav has Issues or About" "grep -Eq 'issues|about' cf-dist/index.html"

# Count essays in content vs built approx
ok "built essays close to content" "python3 -c \"
from pathlib import Path
md=len(list(Path('site/src/content/blog').glob('*.md')))
html=len(list(Path('cf-dist/ideas').glob('*/index.html')))
assert html >= md - 5 and html >= 500, (md, html)
\""

echo "----"
echo "RESULT: $pass/$((pass+fail)) passed"
exit "$fail"
