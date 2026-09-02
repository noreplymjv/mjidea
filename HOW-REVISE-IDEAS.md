# How to revise / expand any Mjidea writing (ASAP)

Universal **Writing Desk** — not kids-only. Works for every pending draft, published essay, inbox seed, or brand-new piece in any genre.

## Open the desk

| Where | Path |
|-------|------|
| Passport file | `mjidea-idea-editor.html` |
| Deep link | `mjidea-idea-editor.html?slug=your-slug` |
| Thought Studio | Tab **6. Revise Existing Idea** or header **Revise Idea** |
| Workers (after sync) | `https://mjidea2.noreplymjv.workers.dev/idea-editor.html` |
| Alias | `cf-dist/idea-editor.html`, `site/public/idea-editor.html` |

Catalog JSON: `social/writing_catalog.json` (mirrored as `social/idea_catalog.json`).

Rebuild anytime:

```bash
python3 ./pipeline/build-writing-catalog.py
```

Scans **all** `drafts/pending/*.md`, **all** `site/src/content/blog/*.md`, **all** `inbox/*.md`, plus a **New blank piece** row.

## Writing types

In the UI dropdown (or `--type` on the CLI):

| Type | Use for |
|------|---------|
| `blog_essay` | Philosophy / blog column |
| `columnist` | Opinion column |
| `journalist` | News-analysis |
| `social` | LinkedIn / X / IG pack |
| `short_long` | Hook + deep dive |
| `parenting` / `money` / `humanity` / `life` / `tech` | Category columns |
| `freeform` | Anything else |

## ASAP flow (CEO)

1. Open Writing Desk → search/filter left rail (title, tag, category, pending/published/inbox).
2. Open any item (or **New blank**).
3. Dump notes/facts/instructions in the right panel.
4. Set **Writing type**.
5. **Save notes** (downloads `revise-notes-<slug>.md`) and/or **Expand & rewrite pack** → paste into Cursor/Perplexity.
6. **Queue revise job** → downloads job file for Passport.
7. On Passport, run the shell command below.
8. When the pending draft looks right: `./pipeline/approve.sh <slug>` — **only then** does it hit the live blog.

## Shell — revise any existing writing

```bash
./pipeline/revise-idea.sh <slug> --notes "extra thoughts" --type columnist
./pipeline/revise-idea.sh <slug> --notes-file inbox/my-notes.md --type parenting
./pipeline/revise-idea.sh inbox/2026-08-21-trust-isnt-certified.md --type blog_essay
./pipeline/revise-idea.sh trust-isnt-certified   # loads pending or published
```

## Shell — brand-new piece

```bash
./pipeline/revise-idea.sh --new "Why boredom is a luxury" --type life --notes "airport scene"
./pipeline/revise-idea.sh --new "LinkedIn: quiet compounding" --type social
```

## What the pipeline writes (never auto-publishes)

- `drafts/pending/<slug>.md` — improved / new draft
- `reports/research/YYYY-MM-DD-<slug>-revise.md` — citation scaffold (agent fills real URLs)
- `reports/ceo/YYYY-MM-DD-<slug>-revise.md` — one-pager
- `drafts/revise-jobs/<slug>.md` — queue for Cursor
- refreshes `social/writing_catalog.json`

Published originals under `site/src/content/blog/` stay untouched until **approve**.

## Cursor phrase

After prep, scripts print:

```text
Execute Mjidea revise job <slug>
```

That means: web-research with real citations → rewrite in the chosen voice → leave in `drafts/pending/` → stop.

## Hard rules

- Execute / revise **stops at pending**
- No invented citations (`team/war-rooms/09-research-citations.md`)
- Voice: `brand/VOICE.md`
- Publish: `./pipeline/approve.sh <slug>` or CEO **approve \<slug\>**
