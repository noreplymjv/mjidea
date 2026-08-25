# Audit & PM Gate (≥5 auditors + PM)

Auditors: Helena Orth, Vic Lang, Rae Kim, Pat Okonkwo, Sky Mendel (+ Jordan Ell).  
Gate owner: Mira Vance (PM).

## Pass criteria (all must be YES)

| Gate | Owner | Question |
|------|-------|----------|
| Voice | Rae | Sounds human per VOICE.md? |
| Craft | Helena | Would a careful reader respect this? |
| Process | Vic | War room phases completed with artifacts? |
| SEO | Pat | SEO pack complete and applied to frontmatter? |
| Launch | Sky | Build succeeds; links/slug OK? |
| Ship | Mira | Ship or revise (one round max unless CEO says)? |

## Output `<slug>.audit.md`

```markdown
## Verdict: SHIP | REVISE
## Findings
- ...
## Required fixes (if REVISE)
- ...
## CEO one-pager
- Title:
- Path: /ideas/<slug>
- Angle:
- Distribution move #1:
```

On SHIP: Engineering publishes to `site/src/content/blog/` and Ops updates `team/STATUS.md`.
