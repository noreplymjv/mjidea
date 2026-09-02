# CEO one-pager — Universal Writing Desk + kids revise demo

- Date: 2026-09-02
- Mode: REVISE / EXPAND — universal (any topic, any genre)
- Publish gate: **unchanged** — `./pipeline/approve.sh <slug>` only

## What shipped

1. **Writing Desk UI** — Windows-like desk at `mjidea-idea-editor.html` (synced to Workers as `/idea-editor.html`)
   - Left: searchable catalog (pending + published + inbox + New blank)
   - Center: markdown editor
   - Right: notes / Expand pack / Queue job
   - Writing-type dropdown: blog, columnist, journalist, social, short+long, parenting/money/humanity/life/tech, freeform

2. **Catalog** — `python3 ./pipeline/build-writing-catalog.py`
   - Writes `social/writing_catalog.json` (+ `idea_catalog.json` mirror)
   - Full filesystem scan (~600+ items)

3. **Pipeline** — `./pipeline/revise-idea.sh`
   - Any slug / inbox path
   - `--new "Title" --type columnist`
   - Always → `drafts/pending/` only

4. **Docs** — `HOW-REVISE-IDEAS.md`

## Demo — `kids-pushed-to-race-by-parents`

- Openable in Writing Desk (`?slug=kids-pushed-to-race-by-parents`)
- Notes: play deficit, Goodhart in parenting, gardener vs carpenter
- Pending rewrite (Mayank Jain voice) with **real citation URLs**
- Research: `reports/research/2026-09-02-kids-pushed-to-race-by-parents-revise.md`
- Live published post **untouched** until you approve

## Smoke — universal `--new`

- Created `drafts/pending/smoke-test-blank-column.md` via `--new "Smoke test blank column" --type columnist`
- Proves desk/pipeline are not kids-only

## Your commands

```bash
# Open locally
xdg-open "mjidea-idea-editor.html"

# Rebuild catalog
python3 ./pipeline/build-writing-catalog.py

# Revise any writing
./pipeline/revise-idea.sh trust-isnt-certified --type columnist --notes "sharpen lede"
./pipeline/revise-idea.sh --new "Why boredom is a luxury" --type life

# Publish when ready
./pipeline/approve.sh kids-pushed-to-race-by-parents
```

## Hard rule

Revise never writes `site/src/content/blog/`. Approve remains the only publish gate.
