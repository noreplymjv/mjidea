# Status Board

Last updated: 2026-09-02

## Mode

**UNIVERSAL WRITING DESK ACTIVE** — revise/expand any topic or genre → `drafts/pending/` only. Omnichannel Thought Engine still on.

## Queue

| Item | Status |
|------|--------|
| Universal Writing Desk / `kids-pushed-to-race-by-parents` (parenting) | PENDING revise → `drafts/pending/kids-pushed-to-race-by-parents.md` (approve to publish) |
| Universal Writing Desk / `smoke-test-blank-column` (columnist) | PENDING smoke `--new` proof → `drafts/pending/smoke-test-blank-column.md` |
| Design lab 12 themes | DONE `/design-lab/` |
| Top 20 × humanity/parenting/financial/life | DONE 80 posts `mj-*` |
| Author byline Mayank Jain | DONE |
| Thought-to-Omnichannel Engine | DONE (`./pipeline/push-thought.sh`) |
| 60-Second Short Video / Reel Storyboards | DONE (`social/packs/*.json`) |
| Multi-Platform Social Packs (LinkedIn, X, IG, YT) | DONE (`social/packs/*.json`) |
| n8n Workflow Blueprint | DONE (`social/n8n_mjidea_omnichannel_workflow.json`) |
| Continuous Scheduler Daemon | DONE (`./pipeline/n8n_scheduler_bridge.py`) |
| Zero-Destruction Safety Protocol | 100% Tested & Preserved (essays intact) |
| Live GitHub Pages | https://noreplymjv.github.io/mjidea/ |
| Workers preview | https://mjidea2.noreplymjv.workers.dev/ |

## Active Commands

- **Push any thought:** `./pipeline/push-thought.sh "<raw thought>"`
- **Approve & Publish:** `./pipeline/approve.sh <slug>`
- **Run Continuous Bridge:** `python3 ./pipeline/n8n_scheduler_bridge.py`

## Universal Writing Desk (ASAP)

- **Open UI:** `mjidea-idea-editor.html` or Workers `/idea-editor.html`
- **Catalog (all pending + all blog + inbox):** `python3 ./pipeline/build-writing-catalog.py`
- **Revise any slug:** `./pipeline/revise-idea.sh <slug> --notes "…" --type columnist`
- **New piece:** `./pipeline/revise-idea.sh --new "Title" --type social`
- **Guide:** `HOW-REVISE-IDEAS.md`
- Publish still requires: `./pipeline/approve.sh <slug>`
