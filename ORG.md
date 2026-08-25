# Mjidea Digital Company — Org Chart

Mj (CEO) floats an idea → the company executes end-to-end without waiting for permission loops.

**Operating rule:** Continuous work. Auto-run. Ask only for irreversible/public/legal/spend decisions.

```
CEO (Mj)
 └── COO / Project Manager — Mira Vance
      ├── War Room Director — Kai Ortega
      │    └── Genius Panel (cross-field, always invited)
      ├── Content Division
      ├── SEO & Discoverability
      ├── Growth / Digital Marketing
      ├── Product & Website Engineering
      ├── Design & Brand
      ├── Security & Trust
      ├── Internal Audit & Quality
      ├── Social / Video (phase 2)
      └── Ops / Pipeline Automation
```

## How work starts

1. CEO drops idea in `inbox/` (or `issues/`)
2. CEO says **execute** or runs `./pipeline/execute.sh` — PM opens `war-room/briefs/`
3. Topic routing (`team/TOPIC-ROUTING.md`) picks the expert squad
4. Research with citations → expert war room → **draft in `drafts/pending/`**
5. **Mj approves** (`./pipeline/approve.sh` or “approve \<slug\>”) → `site/src/content/blog/`
6. Cycle continues; `./pipeline/complete-pending.sh` when CEO says complete pending

## Authority matrix

| Action | Auto? |
|--------|-------|
| Research, draft, rewrite, SEO, design tokens, local build | YES |
| Write to `drafts/pending/` | YES on execute |
| Publish to `site/src/content/blog` | **NO** — only after Mj approve |
| Deploy to Cloudflare Pages | ASK / explicit deploy only |
| Spend money / buy domains / paid ads | ASK CEO |
| Delete published posts / legal claims | ASK CEO |

Full roster: `team/ROSTER.md`  
Auto-run rules: `.cursor/rules/mjidea-autorun.mdc`
