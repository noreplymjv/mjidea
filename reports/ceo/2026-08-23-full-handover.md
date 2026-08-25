# Mjidea — Full Handover Report (Fresh-Start Runbook)

**Date:** 2026-08-23  
**Audience:** Mj (CEO), incoming AI agents, future developers  
**Project root:** this repository root  
**Drive:** Western Digital “My Passport” — portable, must work when plugged into any machine  

---

## 1. What this project is

**Mjidea** is a **portable digital publishing company** — not a chatbot, not a WordPress site.

Mj (CEO) drops raw ideas → a standing **war room** of digital experts researches, debates, drafts in a **human voice** → Mj **approves** → essays publish to a fast **Astro static site** → later: social/video (phase 2).

Core philosophy:
- **Human voice, anti-AI sludge** (`brand/VOICE.md`)
- **Behavioral reframes** (Rory Sutherland *method*, not impersonation) via Cabinet Sutherland + Genius Panel
- **Clarity over virality** — but essays should be shareable
- **Approval-gated publish** — execute never auto-publishes without CEO approve
- **Continuous auto-run** — agents do not ping for permission between research/draft steps

---

## 2. Current state snapshot (2026-08-23)

| Item | Status |
|------|--------|
| Project folder on Passport | ✅ this repo (e.g. `mjI/Mjidea`) |
| Digital org + war room | ✅ `ORG.md`, `team/ROSTER.md`, `team/war-rooms/` |
| Execute → pending → approve pipeline | ✅ `pipeline/execute.sh`, `approve.sh`, etc. |
| Topic bank (505 topics) | ✅ `topics/topics-500.json` |
| Essay library in site content | ✅ **507** markdown files in `site/src/content/blog/` |
| Site build (Astro 7) | ✅ Last build: **513 pages** + sitemap (~1m 40s on Passport) |
| Ideas UI (search + categories) | ✅ `/ideas/` with client-side filter |
| Issues pages (current/future seeds) | ✅ `/issues/` |
| Pending CEO-approved draft | ⏳ `drafts/pending/trust-isnt-certified.md` (researched, with citations — **not live**) |
| Inbox ready floats | ⏳ **17** CEO seeds in `inbox/` (see `team/IDEA-BANK.md`) |
| Git repository | ❌ **Not initialized** in project root |
| GitHub repo `mjidea` | ❌ **Not created** (`noreplymjv/mjidea` does not exist yet) |
| Cloudflare Pages deploy | ❌ Not deployed (planned host — see `HOSTING.md`) |
| Local preview `http://127.0.0.1:4321/` | ⚠️ **Often down** — see §12 Troubleshooting |
| GitHub auth (`gh`) | ✅ Logged in as `noreplymjv` via keyring (HTTPS) |
| GitHub SSH | ❌ `Permission denied (publickey)` — use HTTPS + `gh` |

---

## 3. First 60 seconds for a fresh agent

```bash
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"  # Mjidea repo root
cat START.md          # CEO loop
cat AGENTS.md         # Agent entrypoint
cat team/STATUS.md    # Last known queue
cat brand/VOICE.md    # Voice rules (mandatory before writing)
```

**Read these rules (always apply in Cursor):**
- `.cursor/rules/mjidea-autorun.mdc`
- `.cursor/rules/mjidea-execute-approve.mdc`
- `.cursor/rules/cabinet-sutherland.mdc`
- `.cursor/rules/reports-in-project-folder.mdc`
- Global: `~/.cursor/rules/reports-in-project-folder.mdc`

**CEO says → agent does:**

| CEO command | Action |
|-------------|--------|
| `execute` / `execute <slug>` | Full war room + web research + **`drafts/pending/<slug>.md`** only |
| `complete pending` | Process all inbox/issues queue via `./pipeline/complete-pending.sh` |
| `approve <slug>` | Publish pending → `site/src/content/blog/` |
| `reject <slug>` | Move to `drafts/rejected/` |

---

## 4. Directory map (what lives where)

```
Mjidea/
├── START.md                 ← Quickstart (CEO loop)
├── HANDOVER.md              ← Master handover (long form)
├── AGENTS.md                ← Agent OS entry
├── ORG.md                   ← Org chart + authority matrix
├── HOSTING.md               ← Cloudflare Pages (recommended)
├── .gitignore               ← Ready for git init (node_modules, dist excluded)
│
├── .cursor/rules/           ← Cursor auto-run + execute gate + reports
├── brand/VOICE.md           ← Human voice charter + CEO calibration samples
│
├── inbox/                   ← Raw CEO ideas (_TEMPLATE.md, 17 floats, harvested/)
├── drafts/
│   ├── pending/             ← Awaiting Mj approve (1: trust-isnt-certified)
│   ├── approved/
│   └── rejected/
│
├── war-room/
│   ├── briefs/              ← Active briefs per slug
│   └── output/              ← draft, seo, growth, security, audit per slug
│
├── reports/                 ← ALL audit/research/CEO reports as .md (mandatory)
│   ├── research/ audit/ security/ seo/ growth/ war-room/ ceo/
│   └── README.md
│
├── team/
│   ├── ROSTER.md            ← 50+ digital employees
│   ├── TOPIC-ROUTING.md     ← Topic → expert squad
│   ├── CABINET-SUTHERLAND.md← Web + behavioral library team
│   ├── IDEA-BANK.md         ← 24 curated harvested ideas
│   ├── STATUS.md            ← Status board
│   └── war-rooms/           ← Department playbooks 01–09 + PROTOCOL
│
├── topics/topics-500.json   ← 505 problem/solution topics
├── pipeline/                ← Bash automation (see §6)
├── published/               ← Archive of approved publishes
├── social/scripts/          ← Phase 2 video stubs
│
└── site/                    ← Astro 7 static website
    ├── src/content/blog/    ← 507 published essays (.md)
    ├── src/pages/           ← index, ideas, issues, about
    ├── dist/                ← Build output (gitignored; rebuild locally)
    └── public/_headers      ← Cloudflare security headers
```

---

## 5. The digital company (who does what)

### Executive
- **Mj** — CEO, final approve, philosophy non-negotiables
- **Mira Vance** — PM / COO, queue, ship dates
- **Kai Ortega** — War Room Director
- **Jules Haber** — Chief of Staff, handovers

### Genius Panel (≥5 every session)
Behavioral + leverage + remarkable + antifragile + essay spine + craft + contrarian.  
Playbook: `team/war-rooms/01-genius-panel.md`

### Departments (≥5 experts each when active)
Content · SEO · Growth · Engineering · Design · Security · Audit · Social (phase 2) · Ops

Full roster: `team/ROSTER.md`

### Cabinet Sutherland (library build squad)
Special team for the **505+ essay library** — web architecture, Rory-mode reframes, human voice at scale.  
`team/CABINET-SUTHERLAND.md`

---

## 6. Pipeline scripts (local mini-programs)

All in `pipeline/` — run from project root:

| Script | Purpose |
|--------|---------|
| `ceo-idea.sh <file\|text>` | Raw idea → `war-room/briefs/<slug>.md` |
| `execute.sh <slug\|file\|all-pending>` | Route topic, create research stub + pending scaffold + brief. **Does NOT publish.** |
| `complete-pending.sh` | Queue all unfinished inbox/issues |
| `approve.sh <slug>` | Pending → approved → `site/src/content/blog/` + archive |
| `reject.sh <slug> [reason]` | Pending → rejected |
| `publish-draft.sh <draft.md>` | Lower-level publish (approve.sh wraps this) |
| `run-full-cycle.sh <slug>` | Legacy full war-room cycle initiator |
| `generate-library.js` | Batch-generate essays from `topics/topics-500.json` |
| `lib/common.sh` | Slugify, topic routing helpers |

**Execute flow (mandatory gates):**
1. `./pipeline/execute.sh trust-isnt-certified`
2. Agent runs war room phases per `team/war-rooms/PROTOCOL.md`
3. Web research → `reports/research/YYYY-MM-DD-<slug>.md` (citations required)
4. Draft → `drafts/pending/<slug>.md`
5. Mj reviews
6. `./pipeline/approve.sh trust-isnt-certified` → live on site

---

## 7. Website (Astro 7)

### Stack
- **Astro** ^7.2.4, **@astrojs/sitemap** ^3.7.3
- **Node** ≥22.12.0
- Content collections with Zod schema (`site/src/content.config.ts`)
- Static output — deploy to **Cloudflare Pages** (see `HOSTING.md`)

### Routes
| URL | Page |
|-----|------|
| `/` | Home — hero, essay count, links |
| `/ideas/` | Full library — search + category chips |
| `/ideas/<slug>/` | Individual essay |
| `/issues/` | Issues hub |
| `/issues/current/` | 8 active seeds + add-idea UI |
| `/issues/future/` | 14 future seeds |
| `/about/` | About Mjidea |

### Content frontmatter (required)
```yaml
title: "..."
description: "..."
pubDate: 2026-08-21
tags: ["trust", "philosophy"]
category: "trust"          # optional but used for filters
draft: false               # true = hidden from build
thesis: "..."              # optional
```

### Build & preview
```bash
cd site
ASTRO_TELEMETRY_DISABLED=1 npm run build          # ~1–2 min on Passport; 513 pages
ASTRO_TELEMETRY_DISABLED=1 ./node_modules/.bin/astro preview --host 127.0.0.1 --port 4321
# Open: http://127.0.0.1:4321/
```

### Deploy (when CEO ready)
```bash
cd site && npm run build
npx wrangler pages deploy dist --project-name=mjidea
```
Set `site` URL in `site/astro.config.mjs` when domain is known.

---

## 8. Content library — two tiers

### Tier A: Cabinet batch library (~505 essays)
- Generated from `topics/topics-500.json` via `pipeline/generate-library.js`
- **15 categories:** attention, loneliness, mental, work, education, trust, climate, housing, ai, health, democracy, family, inequality, community, future
- Structure: problem → stake → behavioral reframe → workable door → close
- Human voice rules applied; **not** deep-researched flagship pieces
- **Regenerate:** edit JSON → `node pipeline/generate-library.js` → rebuild site

### Tier B: War-room / CEO essays (higher quality)
- Hand-processed through full expert cycle
- Examples already live:
  - `attention-is-a-moral-choice`
  - `most-philosophy-dies-of-loneliness`
- Pending (not live): `trust-isnt-certified` in `drafts/pending/` with real citations in `reports/research/2026-08-21-trust-isnt-certified.md`

### Inbox seeds (17 ready to execute)
Top 5 per `team/IDEA-BANK.md`:
1. Trust isn’t certified
2. Perception beats the stopwatch
3. Verify everything
4. Commodity → diamond
5. Local-first is respect

---

## 9. Voice & quality rules (non-negotiable)

File: `brand/VOICE.md`

- Clear opinions, concrete scenes, dry wit when earned
- **Banned:** delve, tapestry, robust, seamless, game-changer, “In today’s world…”, etc.
- Structure: tension → flip → quiet close (not summary paragraph)
- CEO calibration samples from Nature’s Pinch / GetMeBack in VOICE.md — mimic rhythm, don’t paste marketing wholesale

**Research:** every factual claim in execute drafts needs URL + title + date accessed (`team/war-rooms/09-research-citations.md`). Do not invent citations.

---

## 10. Reports convention

**Always write reports as `.md` inside this project** — never chat-only.

| Folder | Use |
|--------|-----|
| `reports/research/` | Citation packs |
| `reports/audit/` | Quality gates |
| `reports/security/` | Security reviews |
| `reports/seo/` | SEO packs |
| `reports/growth/` | Distribution |
| `reports/war-room/` | Briefs, library builds |
| `reports/ceo/` | CEO one-pagers, **this handover** |

Pattern: `YYYY-MM-DD-<slug>-<type>.md`

Dual-write: war-room also writes to `war-room/output/` — mirror important artifacts into `reports/`.

---

## 11. Outstanding work (priority order)

### P0 — Blockers / CEO asked
1. **Create GitHub repo `mjidea` and push**
   ```bash
   cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"  # Mjidea repo root
   git init -b main
   git add -A && git commit -m "Initial commit: Mjidea digital company + 500+ essay library"
   gh repo create mjidea --public --source=. --remote=origin --push
   ```
   Note: 507 markdown files = large first push; `.gitignore` excludes `node_modules/` and `site/dist/`.

2. **Fix local preview** if browser shows `ERR_CONNECTION_REFUSED` on `:4321` (see §12)

### P1 — Quality
3. **Approve** `trust-isnt-certified` when Mj is happy → `./pipeline/approve.sh trust-isnt-certified`
4. **Execute** top inbox seeds through full war room (research + citations)
5. **Polish pass** on top 50 batch essays for virality (deeper, less template feel)

### P2 — Growth & deploy
6. **Cloudflare Pages** deploy + custom domain
7. **RSS feed** + JSON-LD schema on essay pages
8. **Related essays** links on single post view
9. **Social/video** phase 2 from `social/scripts/`

### P3 — Site performance at scale
10. Virtualize search on `/ideas/` (507 DOM items can lag on mobile)
11. Self-host fonts (remove Google Fonts dependency)
12. Dynamic OG images for share cards

---

## 12. Troubleshooting

### `ERR_CONNECTION_REFUSED` on http://127.0.0.1:4321/

**Most likely cause:** Astro preview server is **not running**. Preview is not a daemon — it stops when the terminal/session ends.

**Fast checks:**
```bash
ss -tlnp | grep 4321          # nothing = server down
pgrep -af "astro preview"     # stale zombies possible
curl -I http://127.0.0.1:4321/  # should return HTTP 200
```

**Fix:**
```bash
pkill -f "astro preview" 2>/dev/null || true
cd site
ASTRO_TELEMETRY_DISABLED=1 npm run build    # if dist missing/outdated
ASTRO_TELEMETRY_DISABLED=1 ./node_modules/.bin/astro preview --host 127.0.0.1 --port 4321
```

**Also check:** `site/dist/index.html` must exist (preview serves `dist/`, not source).

### Build slow / hangs on Passport
External USB drive I/O is slow. Builds take ~1–2 minutes. Run with `ASTRO_TELEMETRY_DISABLED=1`. Do not run multiple preview instances.

### `gh` / GitHub push fails
- HTTPS works via `gh` keyring (`noreplymjv`)
- SSH to github.com fails — use `gh repo create` / HTTPS remote, not `git@github.com:`

### Astro telemetry permission error
Set `ASTRO_TELEMETRY_DISABLED=1` for all astro commands.

---

## 13. Related systems on same drive

| Path | Role |
|------|------|
| `Aihub/` (Passport sibling) | Portable AI hub — Ollama, models, dashboard (offline agents) |
| `DELETED-review/` (Passport) | Junk review pile (Mj deletes manually) |

Mjidea can run in Cursor alone; Aihub is optional for local model inference. See `reports/research/2026-08-23-project-handover.md` for Aihub details.

---

## 14. Key file index (bookmark these)

| File | Why |
|------|-----|
| `START.md` | CEO 4-step loop |
| `HANDOVER.md` | Long-form master doc (architecture + roster detail) |
| `reports/ceo/2026-08-23-full-handover.md` | **This report** — current state + gaps |
| `AGENTS.md` | Agent entrypoint |
| `ORG.md` | Authority matrix |
| `team/ROSTER.md` | All digital employees |
| `team/TOPIC-ROUTING.md` | Squad routing |
| `team/war-rooms/PROTOCOL.md` | War room phases |
| `team/war-rooms/09-research-citations.md` | Citation rules |
| `team/IDEA-BANK.md` | 24 curated ideas + top 5 |
| `team/STATUS.md` | Live status board |
| `brand/VOICE.md` | Voice charter |
| `topics/topics-500.json` | 505 topic bank |
| `drafts/pending/trust-isnt-certified.md` | Best pending draft example |
| `HOSTING.md` | Cloudflare deploy |
| `audit_report.md` | Cross-expert project audit |

---

## 15. What “done” looks like for Mjidea v1

- [x] Portable folder on Passport with full org + pipeline
- [x] 500+ human-voice essays on site
- [x] Searchable ideas library with categories
- [x] Execute → pending → approve workflow
- [x] Reports in `reports/` + global Cursor rule
- [ ] GitHub repo `mjidea` pushed
- [ ] Cloudflare Pages live at public URL
- [ ] Top inbox seeds executed with real research
- [ ] `trust-isnt-certified` approved and live
- [ ] Phase 2 social/video pipeline active

---

*Prepared for fresh-start continuity. Update this file and `team/STATUS.md` after major milestones.*
