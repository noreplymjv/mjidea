# Mjidea — Agent bootstrap (read this first)

You opened **`mjI/Mjidea`**: a **portable digital company** on disk.  
CEO is **Mj**. Figure out the job from this file — do not wait for hand-holding.

## Immediate map

| Path | Role |
|------|------|
| `START.md` | Human/CEO quick start |
| `HOW-IDEAS-BECOME-BLOGS.md` | Idea → research → approve → live blog |
| `ORG.md` | Company structure |
| `team/ROSTER.md` | Experts |
| `team/TOPIC-ROUTING.md` | Which squad per topic |
| `team/STATUS.md` | Current board |
| `team/war-rooms/` | Protocols (incl. `09-research-citations.md`) |
| `inbox/` | Raw CEO ideas |
| `drafts/pending/` | Waiting CEO approve |
| `site/src/content/blog/` | **Published** essays only |
| `reports/` | Research, SEO, CEO one-pagers |
| `pipeline/*.sh` | execute / approve / reject |

## Standing orders (any agent)

1. On open / first task: skim `team/STATUS.md` + this file.
2. CEO says **execute** / **complete pending** → research with **real internet citations** → write **`drafts/pending/<slug>.md` only**. Never publish from execute.
3. CEO says **approve \<slug\>** → run `./pipeline/approve.sh <slug>` (or equivalent copy into `site/src/content/blog/`).
4. Prefer action over “Should I proceed?”
5. Voice: `brand/VOICE.md`. No invented citations.
6. Dual-write lasting reports under `reports/` (`YYYY-MM-DD-<slug>-<type>.md`).

## CEO phrases

| Phrase | Do |
|--------|-----|
| `execute` / `execute <slug>` | Prep + research + pending draft |
| `complete pending` | Drain inbox / unfinished via pipeline |
| `approve <slug>` | Publish pending → blog |
| `reject <slug>` | Reject pending |

Shell (from this folder):

```bash
./pipeline/execute.sh <slug|inbox-file|all-pending>
./pipeline/approve.sh <slug>
./pipeline/reject.sh <slug> [reason]
```

## Public site meaning

- **Blog** (`/ideas/`) = approved posts from `site/src/content/blog/`
- **Seeds** (`/issues/`) = internal temp prompts — not published blogs

## Tooling note

- **Cursor:** also loads `.cursor/rules/*.mdc` automatically.
- **Any other agent:** this `AGENTS.md` + `START.md` are enough — follow them.
- **Chrome AIs** (Gemini, Perplexity, Claude, Grok…): pack with `./pipeline/pack-for-external.sh <slug>` → see `HOW-EXTERNAL-AGENTS-AND-IMAGES.md` + `prompts/`.
- Local models (Passport `Aihub/`) optional; citations still need web search when available.

## Ask CEO only when

Money/ads, buying domains, legal/defamation risk, deleting public posts, or ambiguous belief that would misrepresent Mj — one precise question, then continue with a stated assumption if no reply.
