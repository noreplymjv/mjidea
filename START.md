# START — Mjidea Digital Company

Portable path: `/media/mj/My Passport/mjI/Mjidea`

## CEO loop (simple)

1. **Put the idea** in `inbox/` (or `issues/current|future/`)
2. **Execute** — `./pipeline/execute.sh <slug|file|all-pending>` **or** say **execute** / **complete pending**
3. **Review** `drafts/pending/<slug>.md` (team researched + drafted; not live yet)
4. **Approve** — `./pipeline/approve.sh <slug>` **or** say **approve \<slug\>** → publishes to `site/src/content/blog/`

Reject: `./pipeline/reject.sh <slug> "reason"`

## What you have

A **standing digital company** (not a single chatbot):

- Topic routing picks the best expert squad (`team/TOPIC-ROUTING.md`)
- Genius Panel + Content / SEO / Growth / Security / Audit
- **Internet research with citations** (`team/war-rooms/09-research-citations.md`)
- **Approval-gated publish** — execute never auto-publishes
- Astro site ready for Cloudflare Pages when you choose to deploy

## Commands

```bash
cd "/media/mj/My Passport/mjI/Mjidea"

# Prep one idea (brief + research stub + pending scaffold)
./pipeline/execute.sh trust-isnt-certified

# List / queue everything unfinished
./pipeline/complete-pending.sh

# After you like the pending draft:
./pipeline/approve.sh trust-isnt-certified
```

In Cursor:

> Execute Mjidea job trust-isnt-certified  
> Complete pending  
> Approve trust-isnt-certified

## Preview site

```bash
cd site && ASTRO_TELEMETRY_DISABLED=1 npm run build
ASTRO_TELEMETRY_DISABLED=1 ./node_modules/.bin/astro preview --host 127.0.0.1 --port 4321
```

**Local URL:** http://127.0.0.1:4321/

Pages: `/` · `/ideas/` (500+ essays, search + categories) · `/issues/` · `/about/`

**Cabinet Sutherland library:** `team/CABINET-SUTHERLAND.md` · `topics/topics-500.json` · regenerate via `node pipeline/generate-library.js`

## Deploy

**Cloudflare Pages + GitHub** — see `CLOUDFLARE_HOSTING.md` (same connect-to-Git style as GetMeBack).

Expected live URL after connect: **https://mjidea.pages.dev**


## Reports

Research packs, audits, security, SEO, growth, CEO one-pagers → `reports/` (see `reports/README.md`).

## Fresh agent?

Read **`reports/ceo/2026-08-23-full-handover.md`** — full snapshot, gaps, troubleshooting.

## Key files

| File | Why |
|------|-----|
| `reports/ceo/2026-08-23-full-handover.md` | Fresh-start handover |
| `ORG.md` | Company chart |
| `team/ROSTER.md` | Digital employees |
| `team/TOPIC-ROUTING.md` | Topic → expert squad |
| `team/war-rooms/PROTOCOL.md` | How the war room ships |
| `team/war-rooms/09-research-citations.md` | Citations required |
| `drafts/pending/` | Awaiting your approve |
| `pipeline/` | execute / complete-pending / approve / reject |
| `brand/VOICE.md` | Anti-AI human voice |
| `AGENTS.md` | Agent entrypoint |
