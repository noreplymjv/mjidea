# Mjidea (mji) — Project Audit & Suggestions Report

This document details the architectural, programmatic, and functional audit of the **Mjidea** digital company codebase located at this repository root.

---

## 1. Executive Summary: What is Mjidea?

**Mjidea** is a lightweight, portable, **standing digital company** designed to publish high-quality, human-centric philosophy and product strategy essays. 
Unlike a simple chatbot, it simulates an entire organization structure:
- **CEO (Mj)**: Floats raw ideas in `inbox/`.
- **Project Manager & Director**: Convert ideas to briefs and host multi-agent debates.
- **Specialized Departments**: Genius Panel (Naval, Taleb, Rory Sutherland style), Content, SEO, Growth, Engineering, Design, Security, and Audit.
- **Output**: Structured draft reviews and a clean, fast **Astro static website** prepared for **Cloudflare Pages** hosting.

The project is designed to run automatically (`AUTO-RUN`) under `.cursor/rules/mjidea-autorun.mdc` to avoid constant permission loops.

---

## 2. Technical Audit & Suggestions

### 2.1 Pipeline Bash Scripts (`pipeline/`)

We audited the shell scripts that run the intake, staging, and publishing pipeline.

#### Findings:
1. **Intake (`ceo-idea.sh`)**:
   - Generates slugs cleanly by stripping non-alphanumeric characters, lowercase mapping, and replacing spaces with dashes.
   - Pre-populates the brief (`war-room/briefs/<slug>.md`) with structured templates and updates `team/STATUS.md` dynamically.
2. **Cycle Manager (`run-full-cycle.sh`)**:
   - Generates the empty stub files: `draft.md`, `seo.md`, `growth.md`, `security.md`, and `audit.md` in `war-room/output/`.
   - Populates a social stub script under `social/scripts/`.
3. **Publishing (`publish-draft.sh`)**:
   - Copies the finalized draft directly to `site/src/content/blog/` and creates a dated snapshot in `published/`.

#### Suggestions & Optimizations:
- **Shell Check & Safety**: In `publish-draft.sh`, if the target directories (`site/src/content/blog` or `published`) don't exist, they are created, which is great. However, it lacks checking if the input draft actually has frontmatter formatting. If published raw, Astro's content loader could fail if the frontmatter is improperly structured.
- **Suggestion**: Add a lightweight frontmatter validation check in `publish-draft.sh` before copying to prevent Astro build failures.
- **Auto-run Pipeline Integration**: Consider adding a CLI script `pipeline/run-all-active.sh` that automatically finds any new files in `inbox/` that don't have matching briefs, creates briefs for them, and sets up their stubs in one command.

---

### 2.2 Astro Website & Frontend (`site/`)

We inspected the Astro configuration, pages, layouts, and components.

#### Findings:
1. **Schema Validation (`site/src/content.config.ts`)**:
   - Defines a solid Zod schema requiring `title`, `description`, `pubDate`, and optional `thesis`, `tags`, `draft`, `heroImage`.
2. **Layout (`site/src/layouts/Base.astro`)**:
   - Implements semantic HTML (`<header>`, `<main>`, `<footer>`).
   - Implements a skip-to-content link for accessibility (`class="skip"`).
   - Loads system fonts (`Fraunces`, `Source Serif 4`, `DM Sans`) for high-quality reading typography.
3. **Ideas Search (`site/src/pages/ideas/index.astro`)**:
   - Uses a pure, lightweight vanilla JS search running client-side.
   - Leverages `data-*` attributes (`data-title`, `data-description`, `data-tags`) to search without needing heavy external search libraries.
4. **Issues Views (`site/src/pages/issues/`)**:
   - Pulls data statically from `site/src/data/issues.ts`.

#### Suggestions & Optimizations:
- **Skip Link Anchor**: `Base.astro` has a `<a class="skip" href="#main">` link, but check if there's CSS styling to hide it visually until focused. If not, it will display statically at the top of the page.
- **Search Keyboard Accessibility**: The search input has no `aria-controls` pointing to the search list (`id="idea-list"`). Adding `aria-controls="idea-list"` improves screen reader experiences.
- **Missing Favicon**: `Base.astro` links to `/favicon.svg`. Verify if this asset actually exists in `site/public/favicon.svg`. If missing, it will throw a 404 in the browser console.
- **Static Issue Syncing**: Currently, `site/src/data/issues.ts` is hardcoded. Since the `team/IDEA-BANK.md` contains the canonical status, we should automate the generation or parsing of `issues.ts` from `team/IDEA-BANK.md` so that they never drift out of sync.

---

### 2.3 Security, Privacy & Cloudflare Hosting

We checked `HOSTING.md` and `seo/PRIVACY-AND-COOKIES.md`.

#### Findings:
1. **Hosting Stance**:
   - Cloudflare Pages is chosen for edge deployment, global speed, HTTP/3 support, and a generous free tier.
2. **Privacy Defaults**:
   - Explicitly rejects invasive ad-tech trackers. Recommend Cloudflare Web Analytics or Plausible (privacy-first, no cookie banner required under GDPR if no personal tracking data is collected).

#### Suggestions & Optimizations:
- **Security Headers**: Since Cloudflare Pages is the host, you can set security headers (`Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`) using a `_headers` file in the build output directory (`site/public/_headers`). This prevents clickjacking and XSS.
- **Suggestion**: Create `site/public/_headers` to enforce secure defaults out of the box:
  ```txt
  /*
    X-Frame-Options: DENY
    X-Content-Type-Options: nosniff
    Referrer-Policy: strict-origin-when-cross-origin
    Permissions-Policy: interest-cohort=()
  ```

---

### 2.4 Brand Voice & Content Quality (`brand/VOICE.md`)

We checked the voice parameters.

#### Findings:
1. **Philosophical Tone**:
   - High-density, brevity, and anti-AI human-written feel.
   - Inspired by Naval's brevity, Godin's remarkable positioning, and Rory Sutherland's behavioral alchemy.

#### Suggestions & Optimizations:
- **Proof-Theater Detection**: Instruct the editor agent (`CN-01`) to scan drafts for "AI jargon" (e.g., words like "tapestry", "delve", "testament", "beacon", "in conclusion"). Add a list of banned/flagged words to `brand/VOICE.md` to keep the content strictly natural.

---

## 3. Recommended Implementation Plan for Upgrades

Here is the proposed task list to execute the suggestions:

| Target Component | Task Description | Priority |
|------------------|------------------|----------|
| **Security** | Create [`site/public/_headers`](site/public/_headers) for secure Cloudflare headers | High |
| **Astro Site** | Add accessibility attributes to search box in [`index.astro`](site/src/pages/ideas/index.astro) | Medium |
| **Pipeline** | Enhance [`publish-draft.sh`](pipeline/publish-draft.sh) with a simple frontmatter format verification | Medium |
| **Brand** | Expand [`VOICE.md`](brand/VOICE.md) with a list of banned AI-clichés | Low |

---
