# Reports — Mjidea

Canonical landing zone for audits and similar deliverables. **Always write reports as `.md` here** (not chat-only).

## Layout

| Folder | What goes here |
|--------|----------------|
| `research/` | Citation packs (`YYYY-MM-DD-<slug>.md`) before pending drafts |
| `audit/` | Audit gates, project audits, QA summaries |
| `security/` | Security reviews |
| `seo/` | SEO packs |
| `growth/` | Growth / distribution packs |
| `war-room/` | Briefs, drafts, and other war-room mirrors |
| `ceo/` | CEO one-pagers and status narratives |

## Filename pattern

`YYYY-MM-DD-<slug>-<type>.md`

Example: `2026-08-21-philosophy-war-room-audit.md`

## Dual-write with war-room

Pipeline still writes to `war-room/briefs/` and `war-room/output/`. Important phase reports are **mirrored** into this tree so every audit/report lives under a clear project-local `reports/` area.

## Rules

- Global Cursor rule: `~/.cursor/rules/reports-in-project-folder.mdc` (`alwaysApply: true`)
- Project rule: `.cursor/rules/reports-in-project-folder.mdc`
