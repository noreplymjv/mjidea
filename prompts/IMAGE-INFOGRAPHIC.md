# Image & infographic prompts (Mjidea)

Generate in Gemini Image, ChatGPT images, Ideogram, Midjourney, etc. Save to `assets/visuals/<slug>/`.

## Always append

```text
Style: quiet editorial illustration, naturalistic light, restrained palette (ink, paper, soft earth or cool grey). Not purple neon, not glassmorphism, not 3D plastic AI look, not stock corporate handshake, no watermarks, no readable fake logos, no walls of tiny text.
Aspect: cover 16:9; infographic 4:5 or square.
```

## A) Cover / hero (one metaphor)

```text
Single quiet scene that expresses: [ONE-SENTENCE THESIS].
One focal metaphor only (e.g. empty stamp pad vs growing plant; stopwatch vs fogged window).
Wide 16:9, cinematic still, human-scale, empty space for an optional title later.
[append Always]
```

## B) Infographic (simple, readable)

```text
Clean editorial infographic for: [THESIS].
Exactly 3 steps or 3 panels, large readable labels in English:
1) [word]
2) [word]
3) [word]
Minimal icons, lots of whitespace, poster layout, not a busy dashboard.
[append Always]
```

## C) Quote card

```text
Typographic quote card on textured paper:
“[SHORT QUOTE FROM ESSAY]”
Small credit line: Mjidea
Elegant serif for quote, plenty of margin.
[append Always]
```

## After generate

1. Download PNG/WebP → `assets/visuals/<slug>/cover.png` (and `infographic-01.png`)
2. Write `notes.txt`: tool + date + prompt used
3. On approve, ask agent: copy into `site/public/visuals/<slug>/` and link from the post if desired
