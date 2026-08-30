# Use Mjidea files with any agent (desktop + Chrome AIs) + images

You keep the **source of truth** on Passport in `Mjidea/`. Other tools (Antigravity / native agents, Gemini, Perplexity, Claude, Grok/xAI, ChatGPT, etc.) are **workers** you paste or upload packs into. Best version still comes back here → `drafts/pending/` → your **approve**.

## One rule

| Stay in Mjidea | Temporary outside |
|----------------|-------------------|
| Inbox, pending, approved blog, citations | Chrome chats, image UIs |
| Final publish | Never “publish” only inside Gemini/Claude |

After an outside tool improves a draft: save the reply as `drafts/pending/<slug>.md` (or paste into Cursor: “merge this into pending”).

---

## A) Desktop / folder agents (Antigravity, Cursor, Claude Code, Copilot…)

1. Point the agent at **`mjI/Mjidea`**
2. They should auto-read **`AGENTS.md`**
3. Say: `execute <slug>` or attach a file from `inbox/` / `drafts/pending/`
4. They research + write pending locally

No special “post” step — the folder **is** the workspace.

---

## B) Online in Chrome (Gemini, Perplexity, Claude, Grok, ChatGPT, Xi/xAI…)

### Fast path — pack then upload/paste

```bash
cd /path/to/mjI/Mjidea
./pipeline/pack-for-external.sh trust-isnt-certified
# → exports/trust-isnt-certified-external-pack.md
```

Then in Chrome:

1. Open the AI tab
2. **Upload** that `.md` (or paste it)
3. Paste the **master instruction** from `prompts/EXTERNAL-AI-PACK.md` (section “Paste this first”)
4. Ask for: improved essay + references + optional image prompts
5. Copy the best essay back into `drafts/pending/<slug>.md`
6. Keep citations in `reports/research/` (fix invented URLs — Perplexity is strongest for live links)

### Which Chrome tool is good for what

| Tool | Best use |
|------|----------|
| **Perplexity** | Fact-check + real links |
| **Claude / Gemini / ChatGPT** | Human rewrite, structure, voice |
| **Grok (xAI)** | Sharp take, counter-arguments |
| **Image tools** (Gemini Image, ChatGPT images, Ideogram, etc.) | Infographic / cover art from `prompts/IMAGE-INFOGRAPHIC.md` |

Run **facts in Perplexity** → **voice rewrite in Claude/Gemini** → merge in Mjidea. That usually beats one chat doing everything.

### Quality gate (ensure “best”)

Outside tool must return:

1. Essay in Mjidea voice (`brand/VOICE.md` is inside the pack)
2. **References** with URL + title + date (or mark “UNVERIFIED”)
3. What it **changed** vs your seed (3 bullets)
4. Risks / weak claims

You (CEO) still **approve** before live Blog.

---

## C) Infographics & related images

1. After the essay exists, run or open `prompts/IMAGE-INFOGRAPHIC.md`
2. Generate 1–3 visuals in any image AI (upload essay summary or paste “Image brief” from the pack script)
3. Save files under:

```text
assets/visuals/<slug>/
  cover.png          # optional post hero
  infographic-01.png
  notes.txt          # which tool + prompt used
```

4. In Cursor/agent: “Attach `assets/visuals/<slug>/` to the pending draft / blog frontmatter when we approve”

Site can later reference images from `site/public/visuals/` on approve (agent copies on approve if you ask).

**Style:** human, quiet, not purple-glow AI sludge. Prefer simple diagram, one metaphor scene, or typographic quote card matching essay thesis — see image prompt file.

---

## D) Suggested combo workflow (best quality)

```text
inbox/*.md
   → pack-for-external.sh
   → Perplexity: facts + links
   → Claude/Gemini: human essay (paste facts)
   → Image AI: cover + 1 infographic
   → save to drafts/pending/ + assets/visuals/
   → approve <slug>
```

Or all-in-Cursor: **execute** (web search) + ask for image prompts → you generate images in Chrome → drop into `assets/visuals/`.

---

## Privacy note

Do not paste secrets, API keys, or private Passport paths into public Chrome AIs. Essay drafts and voice rules are fine if you’re OK with that provider’s training/privacy policy.
