# How Ideas become approved Blogs (with internet facts)

## What you want

1. Drop an **idea** (or pick an **issue seed**)
2. Free AI + war room pulls **real internet sources** (citations)
3. Write a **better, human** draft
4. You **approve** → it becomes a **live blog** on the site
5. Public **Ideas** = approved blogs only · **Issues** = internal temp seeds

## Free AI that can check the internet

| Option | Cost | Internet facts | How you use it |
|--------|------|----------------|----------------|
| **Cursor in this folder** (best fit) | Free tier / your plan | Yes — agent web search | Say **execute \<slug\>** or **complete pending** |
| **Aihub local models** on Passport | Free (your hardware) | Only if agent can search while drafting | Offline draft OK; citations need network session |
| Paid APIs (OpenAI etc.) | Paid | Yes | Not required — Cursor war room is enough |

**Rule:** No invented links. Research packs go in `reports/research/YYYY-MM-DD-<slug>.md`.

## Exact CEO loop

```text
inbox/my-idea.md   →   execute   →   drafts/pending/<slug>.md
                                      + reports/research/...
                         ↓
                   you read + like it
                         ↓
                   approve <slug>   →   site/src/content/blog/<slug>.md
                         ↓
                   rebuild / push   →   live under /ideas/<slug>/
```

### Commands

```bash
cd /path/to/mjI/Mjidea

# 1) Drop idea
cp inbox/_TEMPLATE.md inbox/my-topic.md
# edit my-topic.md

# 2) Prep + tell Cursor to research & draft
./pipeline/execute.sh inbox/my-topic.md
```

In Cursor:

> Execute Mjidea job \<slug\> — web research with citations, human voice, draft to drafts/pending only

Then:

```bash
./pipeline/approve.sh <slug>
# refresh live site (GitHub Pages / Cloudflare) after rebuild
```

Or say: **approve \<slug\>**

## What is temporary vs published

| Place | Status | Public? |
|-------|--------|---------|
| `inbox/` | Raw CEO notes | No |
| `issues/` on site | **Seed queue (temp)** | Visible but labeled internal seeds |
| `drafts/pending/` | Waiting your OK | No |
| `site/src/content/blog/` | **Approved blogs** | Yes → **/ideas/** |
| Cabinet batch essays | Already published library | Yes → **/ideas/** |

When you approve a post, that essay **is** the blog. Seeds stay seeds until executed + approved — they do not replace the library by themselves.

## One sentence for Cursor (copy/paste)

> Take inbox seed \<name\>, research facts from the internet with real citations, run the war room, write a human blog draft to drafts/pending, do not publish until I approve.
