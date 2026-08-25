# War Room Protocol — Mjidea

## Mission

Turn a CEO idea into a shippable, human-sounding, SEO-strong, security-clean, distribution-ready blog package — via adversarial multi-expert debate, not single-model blandness.

## Standing order

- **No permission ping-pong** for research, drafts, rewrites, local builds, SEO packs, security reviews, or staging publishes.
- Ask CEO only for: money, legal risk, irreversible public deletion, or brand-new domain purchase.
- If stuck, Genius Panel proposes 3 asymmetric options; PM picks one and continues.

## Minimum staffing per session

For every CEO idea, summon:

1. **Genius Panel** — at least 5 (GP-01…GP-05 minimum)
2. **Content** — at least 5
3. **SEO** — at least 5
4. **Growth** — at least 5
5. Plus **Security (3+)**, **Audit (3+)**, **PM**, **War Room Director**

Total active voices typically 25–35. They do not all write the post — they pressure-test it.

## Session phases (timed, sequential)

| Phase | Owner | Output file |
|-------|-------|-------------|
| 0 Intake | PM + CoS | `war-room/briefs/<slug>.md` via `./pipeline/execute.sh` |
| 0b Research | Drew + topic lead | `reports/research/YYYY-MM-DD-<slug>.md` — see `09-research-citations.md` |
| 1 Reframe | Genius Panel | section in brief: `## Genius reframes` |
| 2 Angle lock | Content + Growth | `## Chosen angle` |
| 3 Draft | Content squad | `drafts/pending/<slug>.md` + `war-room/output/<slug>.draft.md` |
| 4 Humanize | Editor-in-Chief | same pending file, voice pass |
| 5 SEO pack | SEO squad | `war-room/output/<slug>.seo.md` → `reports/seo/` |
| 6 Growth pack | Growth squad | `war-room/output/<slug>.growth.md` → `reports/growth/` |
| 7 Security | Security | `war-room/output/<slug>.security.md` → `reports/security/` |
| 8 Audit gate | Audit + PM | `war-room/output/<slug>.audit.md` → `reports/audit/` |
| 9 **Mj approve** | CEO | `./pipeline/approve.sh <slug>` |
| 10 Publish | Engineering | `site/src/content/blog/<slug>.md` (only after approve) |
| 11 Social stub | Video (phase 2) | `social/scripts/<slug>.md` |

**Approval gate:** Execute / complete-pending **never** publish. Only `approve.sh` or explicit “approve \<slug\>”.

**Reports mirror:** Research + phases 5–8 + CEO one-pagers land in `reports/<type>/` as `YYYY-MM-DD-<slug>-<type>.md`. See `reports/README.md`.

## Debate rules

1. Each expert must give **one sharp disagreement** or the session is invalid.
2. Genius Panel must include ≥1 **behavioral / irrational leverage** idea (Sutherland-mode).
3. No generic AI cadence: ban “In today’s world…”, “It’s important to note…”, “Delve”, “tapestry”, “landscape”, “robust”, “leverage” as filler.
4. Final draft must pass `brand/VOICE.md`.
5. SEO cannot override truth or voice — it can only sharpen findability.

## How an agent runs this

When CEO says **execute**, **complete pending**, or runs the pipeline scripts:

1. Run `./pipeline/execute.sh <slug|file>` (or `complete-pending.sh` for the queue)
2. Open the brief; staff from `team/TOPIC-ROUTING.md`
3. **Web research + citations** → `reports/research/`
4. Execute war-room phases through audit **without** permission ping-pong
5. Write publish-ready draft to **`drafts/pending/<slug>.md`** (References required)
6. Update `team/STATUS.md` + CEO one-pager in `reports/ceo/`
7. **Stop.** Tell CEO to review pending and run `./pipeline/approve.sh <slug>`

Detailed department playbooks: `team/war-rooms/*.md`
