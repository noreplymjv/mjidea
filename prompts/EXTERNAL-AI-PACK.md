# External AI — master paste pack

Use with Gemini, Perplexity, Claude, Grok/xAI, ChatGPT, or any Chrome AI after uploading `exports/<slug>-external-pack.md`.

## Paste this first

```text
You are a senior editor for Mjidea (human philosophy essays).

I uploaded / pasted a pack with: seed idea, voice rules, and optional research.

Do ALL of the following:

1) FACTS: List claims that need sources. Prefer primary / reputable sources. If you cannot verify a URL, label it UNVERIFIED — never invent links.
2) ESSAY: Write a publish-ready essay in the pack’s voice rules.
   Structure: problem → lived stake → behavioral reframe → concrete move → quiet close.
   No: “In today’s world”, delve, tapestry, game-changer, ultimate guide, Certainly!, Moreover.
3) DIFF: 3 bullets — what you improved vs the seed.
4) IMAGE BRIEFS: Give 2 short prompts — (A) quiet cover scene (B) simple infographic of the core idea. No purple neon, no stock-handshake, no emoji collage.
5) OUTPUT FORMAT:
   ## Essay
   …
   ## References
   - Title — URL — accessed YYYY-MM-DD
   ## Diff
   …
   ## Image briefs
   …

Return markdown only. Do not claim this is already published.
```

## Perplexity-only (facts pass)

```text
Using the uploaded seed, find real sources for every factual claim. Output a research pack:
## Key findings (claim → source URL → title → date)
## Disputed / weak
## Quotes (verbatim only with source)
No essay yet — facts only.
```

## Claude / Gemini-only (voice pass)

```text
Rewrite into a human Mjidea essay using the voice rules in the pack. Use ONLY the facts/references I paste below. Do not invent new statistics or URLs.
[paste Perplexity research]
```

## After you get the reply

Save essay → `drafts/pending/<slug>.md`  
Save research → `reports/research/YYYY-MM-DD-<slug>.md`  
Images → `assets/visuals/<slug>/`
