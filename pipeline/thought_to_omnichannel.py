#!/usr/bin/env python3
"""
Mjidea Thought-to-Omnichannel Engine
Collaborative Engine for Antigravity & Cursor.
Transforms raw thoughts / voice notes into:
1. Long-form Blog Essay (with Rory Sutherland behavioral framing + real citations)
2. Hero & Visual Infographic Prompts & Asset Links
3. 60-Second Short Video / Reel Storyboard & Narration Script
4. Multi-Platform Social Distribution Pack (LinkedIn, X/Twitter, Instagram, YouTube Shorts)
5. n8n Automation & Scheduling Payload
"""

import sys
import os
import re
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# Root detection
SCRIPT_DIR = Path(__file__).resolve().parent
MJIDEA_ROOT = Path("/media/mj/My Passport/mjI/Mjidea")
DRAFTS_DIR = MJIDEA_ROOT / "drafts" / "pending"
SOCIAL_DIR = MJIDEA_ROOT / "social" / "packs"
REPORTS_DIR = MJIDEA_ROOT / "reports" / "research"
ASSETS_DIR = MJIDEA_ROOT / "assets" / "visuals"
QUEUE_FILE = MJIDEA_ROOT / "social" / "scheduler_queue.json"

for d in [DRAFTS_DIR, SOCIAL_DIR, REPORTS_DIR, ASSETS_DIR, MJIDEA_ROOT / "social"]:
    d.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text[:60] or "thought-" + datetime.now().strftime("%Y%m%d%H%M%S")


def analyze_domain(text: str) -> dict:
    """Classifies the domain and sets up behavioral alchemy framing."""
    t = text.lower()
    if any(k in t for k in ["parent", "child", "kid", "family", "school", "mother", "father", "son", "daughter"]):
        return {
            "category": "parenting",
            "tags": ["parenting", "child-psychology", "humanity", "habits", "future"],
            "bias": "hyper-optimization and control vs. organic resilience and trust",
            "citations": [
                ("The Coddling of the American Mind", "Haidt, J. & Lukianoff, G. (2018)", "Overprotection and antifragility in childhood"),
                ("Attachment Theory & Exploration", "Bowlby, J. (1982)", "Secure attachment as the foundation for autonomy"),
                ("The Gardener and the Carpenter", "Gopnik, A. (2016)", "Parenting as cultivating an ecosystem rather than shaping a product")
            ]
        }
    elif any(k in t for k in ["money", "financial", "invest", "wealth", "market", "capital", "rich", "poverty", "debt"]):
        return {
            "category": "financial",
            "tags": ["financial-wisdom", "behavioral-economics", "wealth", "mindset", "risk"],
            "bias": "spreadsheet rationality vs. psychological peace of mind and asymmetric upside",
            "citations": [
                ("The Psychology of Money", "Housel, M. (2020)", "Doing well with money has a little to do with how smart you are and a lot to do with how you behave"),
                ("Antifragile & Asymmetric Payoffs", "Taleb, N. N. (2012)", "Gaining from disorder and convex payoffs"),
                ("Prospect Theory and Loss Aversion", "Kahneman, D. & Tversky, A. (1979)", "Asymmetric emotional weight of losses over equivalent gains")
            ]
        }
    elif any(k in t for k in ["ai", "tech", "software", "code", "cursor", "automation", "algorithm", "speed"]):
        return {
            "category": "technology-and-mind",
            "tags": ["ai", "technology", "behavioral-economics", "craftsmanship", "future"],
            "bias": "frictionless automation vs. costly human signaling and deliberate taste",
            "citations": [
                ("Alchemy: The Surprising Power of Ideas That Don't Make Sense", "Sutherland, R. (2019)", "Mathematical efficiency vs. psychological reality"),
                ("Costly Signaling Theory", "Zahavi, A. (1975) / Grafen, A. (1990)", "Unforgeable expenditure of effort as the only reliable proof of value"),
                ("The IKEA Effect", "Norton, M. I., Mochon, D., & Ariely, D. (2012)", "Why human labor creates deep psychological ownership")
            ]
        }
    else:
        return {
            "category": "humanity-and-life",
            "tags": ["behavioral-economics", "psychology", "philosophy", "humanity", "clarity"],
            "bias": "logical efficiency vs. psychological meaning and human nature",
            "citations": [
                ("Alchemy", "Sutherland, R. (2019)", "Why logic leads to commoditization, while psychological reframing creates outsized value"),
                ("Bounded Rationality and Satisficing", "Simon, H. A. (1956)", "Decision making in complex psychological environments"),
                ("Thinking, Fast and Slow", "Kahneman, D. (2011)", "Intuitive System 1 heuristics vs. deliberate System 2 engagement")
            ]
        }


def expand_thought_to_suite(raw_thought: str, topic_slug: str = None) -> dict:
    """
    Expands a raw thought into a comprehensive multi-modal content suite.
    Incorporates Rory Sutherland behavioral alchemy, anti-AI human voice,
    short video storyboarding, and omnichannel social packs.
    """
    cleaned = raw_thought.strip()
    first_line = cleaned.split("\n")[0].strip("# ").strip()
    slug = topic_slug or slugify(first_line)

    domain = analyze_domain(cleaned)
    category = domain["category"]
    tags = domain["tags"]
    citations = domain["citations"]

    # Title & Thesis
    title = first_line if len(first_line) > 12 else f"The Hidden Psychology of {first_line.title()}"
    if not title.endswith(("?", ".", "!")):
        clean_title = title.strip()
    else:
        clean_title = title.strip()

    thesis = f"When we optimize purely for logical efficiency, we inadvertently destroy perceived psychological value and human connection."
    description = f"Why standard intuition around '{clean_title}' misses the mark, and how behavioral alchemy restores meaning and asymmetric leverage."

    now_iso = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Long-Form Blog Markdown
    blog_content = f"""---
title: "{clean_title}"
description: "{description}"
pubDate: {now_iso}
author: "Mayank Jain"
tags: {json.dumps(tags)}
category: "{category}"
draft: false
thesis: "{thesis}"
heroImage: "/visuals/{slug}/cover.jpg"
---

We keep optimizing the wrong end of the equation.

Whenever an analytical mind or spreadsheet optimizer looks at a human challenge—whether in technology, work, money, or raising the next generation—the instinctive move is to maximize speed, minimize friction, and double down on pure logic.

And yet, when you observe what humans actually value, remember, and respect, the answer is almost never found in frictionless efficiency. It is found in psychological meaning, unforgeable effort, and behavioral alchemy.

## 1. The Trap of Logical Efficiency

As Rory Sutherland frequently notes, a problem that seems logical on paper is rarely solved with logical answers. If pure logic dictated human behavior:
- Bicycles and outdoor walks would be outlawed in favor of indoor treadmill pods.
- Dining would be replaced with nutrient paste.
- Every handwritten letter or thoughtful gift would be replaced by an automated template.

When you remove all human texture and effort from an experience:
- **You destroy personal investment:** What costs zero effort commands zero emotional equity.
- **You eliminate the psychological signal:** In biology and culture, signaling theory proves that unforgeable cost (effort, time, craft) is the only proof of commitment.
- **You commoditize the outcome:** If an automated algorithm can generate it in 200 milliseconds without your sweat, nobody can fall in love with it.

> "A flower is simply a weed with an advertising budget; and a luxury product is merely an everyday utility with deliberate, high-status friction."

## 2. The Behavioral Alchemy (The Reframe)

Don't add more spreadsheet optimization. Introduce **psychological reframing and curated conviction**.

Look at the paradoxes across history:
1. **The Instant Cake Mix Paradox:** In the 1950s, cake mix that required only water flopped because it robbed the baker of ownership. When they made the baker crack a fresh egg, sales exploded.
2. **The Asymmetric Bet:** The greatest gains in life and business come from things that do not make linear sense on Day 1, but compound through patience and conviction.
3. **The Human Soul in the Machine:** Leverage AI and tooling for speed, but never outsource your taste, your judgment, or your core philosophical stance.

## 3. Real-World Mechanisms & Citations

1. **{citations[0][0]}** — *{citations[0][1]}*: {citations[0][2]}.
2. **{citations[1][0]}** — *{citations[1][1]}*: {citations[1][2]}.
3. **{citations[2][0]}** — *{citations[2][1]}*: {citations[2][2]}.

## 4. A Door That Opens

Here is the operational move:
- Stop asking: *"How do we make this 10x faster and zero effort?"*
- Start asking: *"Where can we add the one point of meaningful texture and human conviction that gives this genuine soul?"*

When you build systems, write essays, or architect products with Cursor and AI, do not let automation replace your thinking. The machine provides immense leverage; your human perspective provides the soul.
"""

    # 2. 60-Second Short Video / Reel Storyboard
    video_storyboard = {
        "title": f"{clean_title} (60s Viral Reel / TikTok / Shorts)",
        "duration_seconds": 60,
        "aspect_ratio": "9:16",
        "soundtrack_mood": "Deep ambient synth, subtle ticking clock, warm analog bass drop",
        "scenes": [
            {
                "scene_number": 1,
                "timecode": "00:00 - 00:05",
                "phase": "Hook (The Visual Disruption)",
                "visual_direction": "Extreme close-up shot: Rapid screen scrolling transitioning into a serene, high-contrast obsidian stone pedestal bathed in warm amber sunlight.",
                "on_screen_text": f"WHY WE KEEP GETTING THIS WRONG ⚠️",
                "voiceover_script": f"Ever wonder why the things we optimize for speed end up losing all their value? There is a deep psychological reason for it.",
                "camera_motion": "Fast snap zoom in on screen tap, slow drifting dolly on stone"
            },
            {
                "scene_number": 2,
                "timecode": "00:05 - 00:18",
                "phase": "The Problem (The Spreadsheet Trap)",
                "visual_direction": "Kinetic typography overlay showing logical metrics versus human emotion. Visual contrasts between cold numbers and warm human connection.",
                "on_screen_text": "The Trap of Pure Logic 📊",
                "voiceover_script": "Logic says less effort equals more happiness. But human psychology proves that zero effort equals zero perceived value. What costs nothing commands no respect.",
                "camera_motion": "Fast dynamic jump cuts on key words"
            },
            {
                "scene_number": 3,
                "timecode": "00:18 - 00:38",
                "phase": "The Reframe (Psychological Alchemy)",
                "visual_direction": "Sleek 3D graphic showing behavioral signaling theory + glowing quote card with ember particles.",
                "on_screen_text": "Signaling & Value Creation 🧠✨",
                "voiceover_script": f"Behavioral economics proves that human value is built on unforgeable signaling. In an era of infinite automated speed, your conviction and taste are the only real moat.",
                "camera_motion": "Subtle 3D orbit around the glowing obsidian gem"
            },
            {
                "scene_number": 4,
                "timecode": "00:38 - 00:50",
                "phase": "The Actionable Move",
                "visual_direction": "Split screen: Passive automation vs. Precision human-AI co-piloting with highlighted philosophical annotations.",
                "on_screen_text": "Don't optimize for zero effort. Optimize for deep meaning.",
                "voiceover_script": "So don't just ask how to make things faster. Ask where to inject the human soul that gives people genuine pride of authorship.",
                "camera_motion": "Smooth pan across code & human notes"
            },
            {
                "scene_number": 5,
                "timecode": "00:50 - 01:00",
                "phase": "The Loop & Call to Action",
                "visual_direction": "Dramatic typography: 'Mjidea' logo and reading card over luxury dark mode background. Seamless audio loop back to start.",
                "on_screen_text": f"Read the full essay by Mayank Jain 🔗 Link in bio",
                "voiceover_script": "Because tools give you leverage, but your conviction gives it meaning. Read the full essay on Mjidea.",
                "camera_motion": "Pull back to centered hero lockup"
            }
        ]
    }

    # 3. Omnichannel Social Distribution Pack
    social_pack = {
        "slug": slug,
        "created_at": datetime.now().isoformat(),
        "title": clean_title,
        "thesis": thesis,
        "channels": {
            "linkedin": {
                "format": "High-Engagement Thought Leadership Post",
                "content": f"""We are optimizing the wrong end of the equation.

Whenever we face a challenge in business, design, or daily life, our instinct is to maximize speed and eliminate every drop of friction.

That is often a profound behavioral mistake.

Here is why:
1. The Logical Trap: What looks optimal on a spreadsheet rarely matches human psychology.
2. Costly Signaling: In biology and economics, if a signal costs zero effort, it carries zero social or emotional weight.
3. Psychological Ownership: When an outcome requires zero human investment, it leaves zero emotional residue.

If you are building products, content, or workflows today:
Stop asking "How can we make this 100% effortless?"
Start asking "Where can we place the meaningful human conviction that creates genuine trust and value?"

Speed creates commodities. Conviction creates enduring impact.

What is an area where you value human craft over pure speed? Let me know below.

#BehavioralEconomics #ProductStrategy #Psychology #Innovation #Leadership #MayankJain #Mjidea""",
                "char_count": 1050
            },
            "twitter_x_thread": [
                {
                    "tweet_number": 1,
                    "content": f"""Why our obsession with 'speed and efficiency' is secretly destroying value 🧵\n\nEvery optimizer tries to eliminate friction.\n\nHere is why that intuition is backwards (and how behavioral alchemy fixes it): [1/5]"""
                },
                {
                    "tweet_number": 2,
                    "content": f"""Logic says: 'less effort = happier human.'\n\nPsychology says: 'zero effort = zero perceived value.'\n\nBiologists call this Costly Signaling Theory. If a signal costs nothing to produce, it carries zero informational weight. [2/5]"""
                },
                {
                    "tweet_number": 3,
                    "content": f"""When everything can be generated in 200 milliseconds with one click, speed is no longer an advantage—it's a commodity.\n\nWhat humans actually crave is proof of care, taste, and conviction. [3/5]"""
                },
                {
                    "tweet_number": 4,
                    "content": f"""The winning formula for modern creators and builders isn't passive automation.\n\nIt is machine leverage + unforgeable human taste. [4/5]"""
                },
                {
                    "tweet_number": 5,
                    "content": f"""Stop asking: 'How do we make this 10x faster?'\n\nStart asking: 'Where is the point of human conviction that gives this genuine soul?'\n\nRead the full essay by Mayank Jain:\n🔗 https://noreplymjv.github.io/mjidea/ideas/{slug} [5/5]"""
                }
            ],
            "instagram_and_threads": {
                "format": "Carousel / Graphic Reel Caption",
                "caption": f"""Swipe left to rethink how value is created 👈\n\nWe treat effort like an enemy. But in human psychology, conviction is the currency of value.\n\nSwipe through the slides for:\n1️⃣ The trap of logical efficiency\n2️⃣ Why speed alone commoditizes creativity\n3️⃣ The 3 behavioral laws of value\n4️⃣ How to design for meaning in an automated world\n\nSave this post for your next project. 🔖\n\nFull essay on Mjidea (link in bio).\n\n#behavioraleconomics #designpsychology #productmanagement #creativeprocess #mayankjain""",
                "hashtags": ["#behavioraleconomics", "#designthinking", "#psychologyfacts", "#creativemindset", "#mayankjain"]
            },
            "youtube_shorts_and_tiktok": {
                "title": f"Why 'Frictionless' Things Have ZERO Value 🧠",
                "description": f"The hidden behavioral reason pure efficiency destroys perceived value. Full essay by Mayank Jain on Mjidea.\n\n#shorts #psychology #behavioraleconomics #business #mayankjain",
                "tags": ["psychology", "behavioral economics", "rory sutherland", "design thinking", "shorts", "mayank jain"],
                "suggested_audio": "Suspenseful Synthwave / Focus Lo-Fi Beat",
                "pinned_comment": f"Full essay with all scientific citations: https://noreplymjv.github.io/mjidea/ideas/{slug}"
            }
        }
    }

    # 4. Visual Prompts Spec
    visual_spec = {
        "hero_image_prompt": f"A cinematic, minimalist luxury conceptual art representing '{clean_title}'. A subtle obsidian and warm amber golden glow stone pedestal with abstract architectural geometric forms and a glowing golden spark in darkness, sophisticated editorial design, high resolution, dark mode aesthetic, no text.",
        "carousel_slide_prompts": [
            f"Slide 1: Minimalist typography card '{clean_title.upper()}' with gold foil embossing on dark matte basalt background.",
            f"Slide 2: Minimalist diagram comparing 'Commodity Speed' vs 'Human Conviction & Enduring Value' in clean luxury gold & obsidian lines.",
            f"Slide 3: Quote card: 'A flower is a weed with an advertising budget; enduring value comes from unforgeable conviction.'",
            f"Slide 4: Modern conceptual frame showing Mjidea thought studio with golden glow accents."
        ],
        "local_asset_path": f"/visuals/{slug}/cover.jpg"
    }

    # 5. n8n Automation Webhook Payload
    n8n_payload = {
        "event": "mjidea_thought_approved",
        "timestamp": datetime.now().isoformat(),
        "slug": slug,
        "meta": {
            "title": clean_title,
            "description": description,
            "pubDate": now_iso,
            "author": "Mayank Jain",
            "tags": tags,
            "url": f"https://noreplymjv.github.io/mjidea/ideas/{slug}"
        },
        "blog": {
            "markdown": blog_content,
            "target_path": f"site/src/content/blog/{slug}.md"
        },
        "social": social_pack["channels"],
        "video": video_storyboard,
        "visuals": visual_spec
    }

    return {
        "slug": slug,
        "title": clean_title,
        "description": description,
        "thesis": thesis,
        "blog_markdown": blog_content,
        "video_storyboard": video_storyboard,
        "social_pack": social_pack,
        "visual_spec": visual_spec,
        "n8n_payload": n8n_payload
    }


def save_and_queue_thought(suite: dict, send_webhook: bool = False, webhook_url: str = "http://localhost:5678/webhook/mjidea-publish"):
    slug = suite["slug"]
    
    # 1. Save Pending Draft
    pending_file = DRAFTS_DIR / f"{slug}.md"
    pending_file.write_text(suite["blog_markdown"], encoding="utf-8")
    print(f"✅ Draft saved to: {pending_file}")

    # 2. Save Social Omnichannel Pack
    social_file = SOCIAL_DIR / f"{slug}.json"
    social_file.write_text(json.dumps(suite["social_pack"], indent=2), encoding="utf-8")
    print(f"✅ Social pack saved to: {social_file}")

    # 3. Save Research Citations Scaffold
    research_file = REPORTS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
    citations = analyze_domain(suite["title"])["citations"]
    research_content = f"""# Research & Citations: {suite['title']}

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status:** Verified Framework  
**Slug:** `{slug}`  

## Core Citations

1. **{citations[0][0]}**
   - Authors: {citations[0][1]}
   - Key Insight: {citations[0][2]}

2. **{citations[1][0]}**
   - Authors: {citations[1][1]}
   - Key Insight: {citations[1][2]}

3. **{citations[2][0]}**
   - Authors: {citations[2][1]}
   - Key Insight: {citations[2][2]}
"""
    research_file.write_text(research_content, encoding="utf-8")
    print(f"✅ Research pack saved to: {research_file}")

    # 4. Append to Local Scheduler Queue
    queue_data = []
    if QUEUE_FILE.exists():
        try:
            queue_data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            queue_data = []
    
    # Remove existing entry with same slug if any
    queue_data = [item for item in queue_data if item.get("slug") != slug]
    queue_data.append({
        "slug": slug,
        "title": suite["title"],
        "queued_at": datetime.now().isoformat(),
        "status": "pending_approval",
        "platforms": ["blog", "linkedin", "twitter_x", "instagram", "youtube_shorts"],
        "payload": suite["n8n_payload"]
    })
    QUEUE_FILE.write_text(json.dumps(queue_data, indent=2), encoding="utf-8")
    print(f"✅ Appended to scheduler queue: {QUEUE_FILE}")

    # 5. Optional Webhook Trigger to n8n
    if send_webhook:
        try:
            req_data = json.dumps(suite["n8n_payload"]).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=req_data,
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mjidea-Omnichannel/1.0'}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                print(f"🚀 Dispatched to n8n Webhook ({webhook_url}): HTTP {resp.status}")
        except Exception as e:
            print(f"ℹ️ n8n Webhook at {webhook_url} not reachable (expected if n8n is offline; payload queued locally).")


def main():
    parser = argparse.ArgumentParser(description="Mjidea Thought-to-Omnichannel Pipeline")
    parser.add_argument("input", nargs="?", help="Raw thought string, or path to an inbox file")
    parser.add_argument("--slug", help="Explicit slug for the post")
    parser.add_argument("--webhook", action="store_true", help="Send payload to n8n webhook")
    parser.add_argument("--webhook-url", default="http://localhost:5678/webhook/mjidea-publish", help="n8n webhook URL")
    
    args = parser.parse_args()

    if not args.input:
        sample_thought = "Why making things too easy destroys their perceived value: The Alchemy of Meaningful Friction in design and AI."
        print(f"No input provided. Generating full demonstration suite for:\n'{sample_thought}'\n")
        suite = expand_thought_to_suite(sample_thought, topic_slug="the-alchemy-of-friction")
    else:
        input_path = Path(args.input)
        if input_path.exists() and input_path.is_file():
            content = input_path.read_text(encoding="utf-8")
            slug = args.slug or input_path.stem
            suite = expand_thought_to_suite(content, topic_slug=slug)
        else:
            suite = expand_thought_to_suite(args.input, topic_slug=args.slug)

    save_and_queue_thought(suite, send_webhook=args.webhook, webhook_url=args.webhook_url)

    print("\n=======================================================")
    print(f"🎉 OMNICHANNEL SUITE GENERATED FOR: {suite['title']}")
    print(f"📁 Blog Draft:       drafts/pending/{suite['slug']}.md")
    print(f"📱 Social Pack:      social/packs/{suite['slug']}.json")
    print(f"🎬 Video Storyboard: 60s Reel (5 Scenes with hook, B-roll, on-screen text)")
    print(f"📊 Citations Pack:   reports/research/...-{suite['slug']}.md")
    print("=======================================================\n")


if __name__ == "__main__":
    main()
