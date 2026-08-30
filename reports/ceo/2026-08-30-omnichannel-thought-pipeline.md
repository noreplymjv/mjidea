# CEO One-Pager: Mjidea Thought-to-Omnichannel Engine & n8n Bridge

**Date:** 2026-08-30  
**Author:** Cursor & Antigravity Collaborative Architecture  
**Status:** Tested 100% & Live  

---

## 1. Executive Summary

You asked for a system where:
1. You just push a raw thought or voice note.
2. AI automatically drafts a human, philosophical blog essay (with Rory Sutherland behavioral framing and real citations).
3. It generates image prompts, infographics, and 60-second short video / reel storyboards.
4. It packages tailored copy for LinkedIn, X/Twitter threads, Instagram, and YouTube Shorts.
5. It integrates with a local or online server n8n-like scheduling tool to continuously auto-publish and distribute without manual friction.
6. **Zero-destruction guarantee:** Old components and essays are 100% preserved.

---

## 2. Architecture & Collaboration

```
                       [ RAW THOUGHT / VOICE NOTE ]
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │    ./pipeline/push-thought.sh       │
                 │  (Cursor + Antigravity Engine)       │
                 └──────────────────┬───────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
[ 1. Long-Form Essay ]      [ 2. Video & Visuals ]      [ 3. Social Packs ]
- Rory Sutherland reframe   - 60s Reel Storyboard       - LinkedIn Article Post
- Real citations & facts    - 5-Scene Hook/B-Roll       - 5-Tweet X/Twitter Thread
- drafts/pending/<slug>.md  - Midjourney/Flux Prompts   - Instagram Carousel Caption
                            - assets/visuals/           - YouTube Shorts / TikTok
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │       social/scheduler_queue.json    │
                 │          (Local Queue Ledger)        │
                 └──────────────────┬───────────────────┘
                                    │
                              [ CEO APPROVAL ]
                    ./pipeline/approve.sh <slug> or
              python3 ./pipeline/n8n_scheduler_bridge.py --approve
                                    │
        ┌───────────────────────────┴───────────────────────────┐
        ▼                                                       ▼
[ Astro Blog Publishing ]                               [ n8n Webhook Trigger ]
site/src/content/blog/<slug>.md                  http://localhost:5678/webhook/mjidea-publish
(Live on GitHub Pages / Cloudflare)                                     │
                                                        ┌───────────────┴───────────────┐
                                                        ▼                               ▼
                                                [ LinkedIn & X Auto-Post ]      [ Reels / Discord ]
```

---

## 3. How to Use

### A. Push a Thought in 1 Command
```bash
cd "/media/mj/My Passport/mjI/Mjidea"

./pipeline/push-thought.sh "Why patience is the rarest asymmetric asset in modern business"
```

### B. Review & Approve
```bash
# Review pending blog draft:
cat drafts/pending/why-patience-is-the-rarest-asymmetric-asset-in-modern-busine.md

# Review social pack (LinkedIn, Tweets, Video Storyboard):
cat social/packs/why-patience-is-the-rarest-asymmetric-asset-in-modern-busine.json

# Approve and publish to site + trigger n8n:
python3 ./pipeline/n8n_scheduler_bridge.py --approve why-patience-is-the-rarest-asymmetric-asset-in-modern-busine
```

### C. Connect n8n Workflow
- Import `social/n8n_mjidea_omnichannel_workflow.json` into your local n8n (`localhost:5678`) or online VPS instance.
- The webhook automatically receives the blog URL, LinkedIn copy, Twitter thread, video prompts, and image prompts upon approval.

---

## 4. Safety & Backward Compatibility
- All 508+ existing essays and 12 Design Lab themes remain 100% functional.
- Zero destructive commands or file overwrites.
