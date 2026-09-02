#!/usr/bin/env python3
"""Revise / expand ANY Mjidea writing — pending, published, inbox, or brand-new.

Usage:
  ./pipeline/revise-idea.sh <slug> [--notes "..."] [--notes-file path] [--type columnist]
  ./pipeline/revise-idea.sh --new "Title here" --type columnist [--notes "..."]
  ./pipeline/revise-idea.sh inbox/2026-08-21-trust-isnt-certified.md

Writing types (--type):
  blog_essay | columnist | journalist | social | short_long
  parenting | money | humanity | life | tech | freeform

Behavior:
  - Load source: drafts/pending OR blog OR inbox OR create new
  - Merge CEO revision notes
  - Research scaffold → reports/research/YYYY-MM-DD-<slug>-revise.md
  - Pending only → drafts/pending/<slug>.md (never auto-publish)
  - CEO one-pager + revise job queue
  - Rebuild writing catalog
  - Print: Execute Mjidea revise job <slug>
"""
from __future__ import annotations

import argparse
import re
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PENDING_DIR = ROOT / "drafts" / "pending"
BLOG_DIR = ROOT / "site" / "src" / "content" / "blog"
INBOX_DIR = ROOT / "inbox"
JOBS_DIR = ROOT / "drafts" / "revise-jobs"
RESEARCH_DIR = ROOT / "reports" / "research"
CEO_DIR = ROOT / "reports" / "ceo"
STATUS = ROOT / "team" / "STATUS.md"

WRITING_TYPES = {
    "blog_essay": {
        "label": "Blog essay / philosophy column",
        "voice": "Mayank Jain philosophy column — brand/VOICE.md",
        "structure": "problem → lived stake → behavioral reframe → concrete move → quiet close",
        "category": "philosophy",
        "tags": '["philosophy", "ideas", "humanity"]',
    },
    "columnist": {
        "label": "Columnist / opinion",
        "voice": "Newspaper columnist — sharp claim, scene, turn, residual question",
        "structure": "lede hook → stake → evidence turn → counsel → quiet close",
        "category": "philosophy",
        "tags": '["column", "opinion", "ideas"]',
    },
    "journalist": {
        "label": "Journalist / news-analysis",
        "voice": "News-analysis column — facts first, attribution, then judgment",
        "structure": "what happened → why it matters → competing frames → what to watch",
        "category": "humanity",
        "tags": '["analysis", "journalism", "ideas"]',
    },
    "social": {
        "label": "Social writer (LinkedIn / X / IG)",
        "voice": "Social writer — hook in first line, scannable, no sludge",
        "structure": "hook → 3 beats → CTA; also draft LinkedIn + X thread + IG caption in appendix",
        "category": "growth",
        "tags": '["social", "linkedin", "distribution"]',
    },
    "short_long": {
        "label": "Short-form hook + long-form deep dive",
        "voice": "Hook writer + essayist — 60s punch then full column",
        "structure": "SHORT HOOK (≤120 words) then LONG ESSAY (problem→reframe→move→close)",
        "category": "philosophy",
        "tags": '["short-form", "essay", "ideas"]',
    },
    "parenting": {
        "label": "Parenting column",
        "voice": "Parenting columnist — lived stake, behavioral reframe, no lecture",
        "structure": "problem → lived stake → reframe → concrete move → quiet close",
        "category": "parenting",
        "tags": '["parenting", "child-psychology", "humanity"]',
    },
    "money": {
        "label": "Money / financial life",
        "voice": "Money column — concrete numbers + behavioral alchemy",
        "structure": "money tension → lived stake → reframe → move → quiet close",
        "category": "financial",
        "tags": '["money", "financial", "habits"]',
    },
    "humanity": {
        "label": "Humanity / culture",
        "voice": "Humanity essay — dignity, perception, antifragile culture",
        "structure": "problem → lived stake → reframe → move → quiet close",
        "category": "humanity",
        "tags": '["humanity", "culture", "ideas"]',
    },
    "life": {
        "label": "Life / habits",
        "voice": "Life column — small scenes, honest uncertainty",
        "structure": "problem → lived stake → reframe → move → quiet close",
        "category": "life",
        "tags": '["life", "habits", "humanity"]',
    },
    "tech": {
        "label": "Tech / AI",
        "voice": "Tech column — human judgment over tool worship",
        "structure": "problem → lived stake → reframe → move → quiet close",
        "category": "tech",
        "tags": '["tech", "ai", "product"]',
    },
    "freeform": {
        "label": "Freeform",
        "voice": "User-chosen — default Mayank Jain / brand/VOICE.md",
        "structure": "flexible — still avoid AI sludge",
        "category": "philosophy",
        "tags": '["ideas"]',
    },
}


def slugify(s: str) -> str:
    s = re.sub(r"\.md$", "", s)
    s = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "untitled"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip().strip('"').strip("'")
    body = parts[2].lstrip("\n")
    return meta, body


def format_fm_line(key: str, val: str) -> str:
    if key in ("tags",) or (isinstance(val, str) and val.startswith("[")):
        return f"{key}: {val}"
    if key == "draft":
        return f"{key}: {val}"
    if isinstance(val, str) and (":" in val or '"' in val):
        esc = val.replace('"', '\\"')
        return f'{key}: "{esc}"'
    if isinstance(val, str):
        return f'{key}: "{val}"'
    return f"{key}: {val}"


def dump_frontmatter(meta: dict) -> str:
    order = [
        "title",
        "description",
        "pubDate",
        "author",
        "tags",
        "category",
        "draft",
        "thesis",
        "heroImage",
        "writingType",
    ]
    lines = ["---"]
    seen = set()
    for k in order:
        if k in meta:
            lines.append(format_fm_line(k, meta[k]))
            seen.add(k)
    for k, v in meta.items():
        if k not in seen:
            lines.append(format_fm_line(k, v))
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def resolve_source(slug: str, inbox: Path | None) -> tuple[Path | None, str, str]:
    """Return (source_path|None, source_kind, resolved_slug)."""
    if inbox and inbox.is_file():
        return inbox, "inbox", slugify(inbox.stem)

    # Path-like input
    cand = Path(slug)
    if cand.suffix == ".md" and cand.is_file():
        return cand, "path", slugify(cand.stem)
    if (ROOT / slug).is_file():
        p = ROOT / slug
        return p, "path", slugify(p.stem)

    pending = PENDING_DIR / f"{slug}.md"
    blog = BLOG_DIR / f"{slug}.md"
    if pending.is_file():
        if blog.is_file():
            ptext = pending.read_text(encoding="utf-8", errors="replace")
            # Prefer published if pending is thin execute stub
            if "behavioral alchemy restores meaning" in ptext.lower() or len(ptext) < 800:
                return blog, "blog (pending was stub — using published)", slug
        return pending, "pending", slug
    if blog.is_file():
        return blog, "blog", slug

    hits = list(INBOX_DIR.glob(f"*{slug}*.md")) if INBOX_DIR.is_dir() else []
    hits = [h for h in hits if "TEMPLATE" not in h.name.upper()]
    if hits:
        return hits[0], "inbox", slug

    return None, "missing", slug


def new_piece_scaffold(title: str, wtype: str, notes: str) -> tuple[dict, str]:
    spec = WRITING_TYPES.get(wtype, WRITING_TYPES["freeform"])
    today = date.today().isoformat()
    meta = {
        "title": title,
        "description": f"{spec['label']} draft — pending revise (not published).",
        "pubDate": today,
        "author": "Mayank Jain",
        "tags": spec["tags"],
        "category": spec["category"],
        "draft": "true",
        "thesis": "",
        "writingType": wtype,
    }
    body = f"""# {title}

_(New piece — writing type: **{spec['label']}**)_

Voice: {spec['voice']}
Structure: {spec['structure']}

## Draft

Start here. Add notes in the CEO revision section below or via the Writing Desk.

"""
    if notes.strip():
        body += f"## CEO seed notes\n\n{notes.strip()}\n"
    return meta, body


def append_notes_section(body: str, notes: str, ts: str) -> str:
    if not notes.strip():
        return body
    marker = "## CEO revision notes"
    if marker in body:
        return body.rstrip() + f"\n\n### Update — {ts}\n\n{notes.strip()}\n"
    return body.rstrip() + f"\n\n{marker}\n\n_Added: {ts}_\n\n{notes.strip()}\n"


def write_research_scaffold(
    slug: str, notes: str, source_kind: str, today: str, wtype: str
) -> Path:
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    path = RESEARCH_DIR / f"{today}-{slug}-revise.md"
    spec = WRITING_TYPES.get(wtype, WRITING_TYPES["freeform"])
    content = f"""# Research — {slug} (revise)

- Date: {today}
- Mode: REVISE / EXPAND (source: {source_kind})
- Writing type: **{wtype}** — {spec['label']}
- Voice: {spec['voice']}
- Structure: {spec['structure']}
- Gate: draft → `drafts/pending/` only — **NO auto-publish**

## Search queries used
- (agent fills based on topic)

## CEO revision notes (to integrate)

{notes.strip() or "_(none — structural polish only)_"}

## Key findings
1. Claim … — Source: [Title](URL) — Accessed: {today} — Notes: …
2. Claim … — Source: [Title](URL) — Accessed: {today} — Notes: …
3. Claim … — Source: [Title](URL) — Accessed: {today} — Notes: …

## Disputed / weak
- …

## Quotes worth using (verbatim only if sourced)
- "…" — Source …

## AGENT MUST FILL via web search
_(If offline or search failed — leave this banner and do not invent URLs.)_
Follow `team/war-rooms/09-research-citations.md`.

## Rewrite brief
Apply writing type **{wtype}**. Ban AI sludge per `brand/VOICE.md`. Author: Mayank Jain when appropriate.
If type=social: also produce LinkedIn / X thread / IG caption in an appendix (still pending only).
If type=short_long: lead with SHORT HOOK then LONG ESSAY.
"""
    path.write_text(content, encoding="utf-8")
    return path


def write_ceo_onepager(
    slug: str,
    today: str,
    source_kind: str,
    research: Path,
    pending: Path,
    job: Path,
    notes: str,
    wtype: str,
) -> Path:
    CEO_DIR.mkdir(parents=True, exist_ok=True)
    path = CEO_DIR / f"{today}-{slug}-revise.md"
    spec = WRITING_TYPES.get(wtype, WRITING_TYPES["freeform"])
    content = f"""# CEO one-pager — revise `{slug}`

- Date: {today}
- Writing type: {wtype} ({spec['label']})
- Source loaded: {source_kind}
- Pending draft: `{pending.relative_to(ROOT)}`
- Research: `{research.relative_to(ROOT)}`
- Job queue: `{job.relative_to(ROOT)}`
- Published original: untouched (approve still required)

## What changed
- Revision notes / new piece scaffold merged into pending
- Research revise scaffold written
- Revise job queued for Cursor / Perplexity

## CEO notes snapshot
{notes.strip() or "_(structural revise only)_"}

## Your next moves
1. Open Writing Desk: `mjidea-idea-editor.html` (or Workers `/idea-editor.html`)
2. Or tell Cursor: **Execute Mjidea revise job {slug}**
3. When happy: `./pipeline/approve.sh {slug}`

## Hard rule
Execute / revise stops at `drafts/pending/`. Never auto-publish.
"""
    path.write_text(content, encoding="utf-8")
    return path


def write_job(
    slug: str, notes: str, today: str, source_label: str, wtype: str
) -> Path:
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    path = JOBS_DIR / f"{slug}.md"
    spec = WRITING_TYPES.get(wtype, WRITING_TYPES["freeform"])
    content = f"""# Revise job — {slug}

- Queued: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
- Source: {source_label}
- Writing type: {wtype} ({spec['label']})
- Target: `drafts/pending/{slug}.md`
- Research: `reports/research/{today}-{slug}-revise.md`

## Status
**QUEUED** — agent must web-research + rewrite in chosen voice, then leave in pending.

## CEO notes
{notes.strip() or "_(none)_"}

## Agent checklist
- [ ] Fill research pack with real URLs (`09-research-citations.md`)
- [ ] Rewrite per type **{wtype}**: {spec['structure']}
- [ ] Voice: {spec['voice']}
- [ ] Save to `drafts/pending/{slug}.md` only
- [ ] Dual-write under `reports/`
- [ ] **STOP** — wait for `./pipeline/approve.sh {slug}`

## Cursor trigger
Execute Mjidea revise job {slug}
"""
    path.write_text(content, encoding="utf-8")
    return path


def update_status(slug: str, today: str, wtype: str) -> None:
    if not STATUS.exists():
        return
    text = STATUS.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"Last updated:.*", f"Last updated: {today}", text, count=1)
    row = (
        f"| Universal Writing Desk / `{slug}` ({wtype}) | "
        f"PENDING → `drafts/pending/{slug}.md` (approve to publish) |"
    )
    if f"`{slug}`" in text and "Writing Desk" in text:
        text = re.sub(
            rf"\| Universal Writing Desk / `{re.escape(slug)}`[^|]*\|[^|]*\|",
            row,
            text,
        )
    elif "| Item | Status |" in text:
        text = text.replace(
            "| Item | Status |\n|------|--------|\n",
            f"| Item | Status |\n|------|--------|\n{row}\n",
            1,
        )
    else:
        text += f"\n\n## Revise queue\n\n{row}\n"

    cmd_block = (
        "\n## Universal Writing Desk (ASAP)\n\n"
        "- **Open UI:** `mjidea-idea-editor.html` or Workers `/idea-editor.html`\n"
        "- **Catalog:** `python3 ./pipeline/build-writing-catalog.py`\n"
        "- **Revise any slug:** `./pipeline/revise-idea.sh <slug> --notes \"…\" --type columnist`\n"
        "- **New piece:** `./pipeline/revise-idea.sh --new \"Title\" --type social`\n"
        "- **Guide:** `HOW-REVISE-IDEAS.md`\n"
        "- Publish still requires: `./pipeline/approve.sh <slug>`\n"
    )
    if "## Universal Writing Desk (ASAP)" not in text:
        # Replace older revise section if present
        if "## Revise Ideas (ASAP)" in text:
            text = re.sub(
                r"## Revise Ideas \(ASAP\).*?(?=\n## |\Z)",
                cmd_block.lstrip() + "\n",
                text,
                flags=re.S,
            )
        else:
            text = text.rstrip() + "\n" + cmd_block + "\n"
    STATUS.write_text(text, encoding="utf-8")


def build_pending_draft(
    meta: dict,
    body: str,
    notes: str,
    slug: str,
    source_kind: str,
    today: str,
    wtype: str,
) -> str:
    meta = dict(meta)
    meta.setdefault("author", "Mayank Jain")
    meta["draft"] = "true"
    meta["writingType"] = wtype
    spec = WRITING_TYPES.get(wtype, WRITING_TYPES["freeform"])
    meta.setdefault("category", spec["category"])
    meta.setdefault("tags", spec["tags"])
    if "title" not in meta:
        meta["title"] = slug.replace("-", " ").title()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body2 = append_notes_section(body, notes, ts)
    banner = (
        f"<!-- MJIDEA REVISE — {today} — type:{wtype} — source: {source_kind} — "
        f"NOT published until approve — -->\n"
    )
    agent_todo = (
        "\n\n<!-- AGENT: weave notes into body for this writing type; "
        "refresh citations; remove this comment when READY. -->\n"
    )
    return dump_frontmatter(meta) + banner + body2.rstrip() + agent_todo + "\n"


def append_inbox_notes(slug: str, notes: str) -> Path | None:
    if not notes.strip():
        return None
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = INBOX_DIR / f"{today}-revise-notes-{slug}.md"
    block = f"# Revise notes — {slug}\n\n- Added: {today}\n\n{notes.strip()}\n"
    if path.exists():
        path.write_text(
            path.read_text(encoding="utf-8") + f"\n\n---\n\n{notes.strip()}\n",
            encoding="utf-8",
        )
    else:
        path.write_text(block, encoding="utf-8")
    return path


def rebuild_catalog() -> None:
    script = ROOT / "pipeline" / "build-writing-catalog.py"
    if script.is_file():
        subprocess.run(["python3", str(script)], check=False, cwd=str(ROOT))
    else:
        legacy = ROOT / "pipeline" / "build_idea_catalog.py"
        if legacy.is_file():
            subprocess.run(["python3", str(legacy)], check=False, cwd=str(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Mjidea universal revise / new writing pipeline (stops at pending)"
    )
    ap.add_argument(
        "slug",
        nargs="?",
        default="",
        help="Slug, inbox path, or omit when using --new",
    )
    ap.add_argument("--new", dest="new_title", default="", help='Create new piece: --new "Title"')
    ap.add_argument(
        "--type",
        dest="wtype",
        default="blog_essay",
        choices=sorted(WRITING_TYPES.keys()),
        help="Writing type / voice mode",
    )
    ap.add_argument("--notes", default="", help="CEO revision notes / new facts")
    ap.add_argument("--notes-file", type=Path, help="Read notes from file")
    ap.add_argument("--inbox", type=Path, help="Optional inbox/source override path")
    ap.add_argument(
        "--save-notes-only",
        action="store_true",
        help="Only append notes to inbox + pending",
    )
    ap.add_argument("--no-catalog", action="store_true", help="Skip catalog rebuild")
    args = ap.parse_args()

    notes = args.notes or ""
    if args.notes_file and args.notes_file.is_file():
        notes = (notes + "\n\n" if notes else "") + args.notes_file.read_text(
            encoding="utf-8"
        )

    today = date.today().isoformat()
    wtype = args.wtype

    if args.new_title:
        title = args.new_title.strip()
        slug = slugify(title)
        source_path = None
        source_kind = "new"
        meta, body = new_piece_scaffold(title, wtype, notes)
        # notes already in body for new — avoid double-append unless more
        notes_for_append = ""
    else:
        if not args.slug:
            ap.error("Provide <slug> or --new \"Title\"")
        raw = args.slug
        # strip inbox:: prefix from catalog
        if raw.startswith("inbox::"):
            raw = raw[len("inbox::") :]
        slug = slugify(Path(raw).stem if str(raw).endswith(".md") else raw)
        source_path, source_kind, slug = resolve_source(raw if "/" in str(raw) else slug, args.inbox)
        if source_path is None:
            raise SystemExit(
                f"No source for '{args.slug}'. Use existing slug or: "
                f'./pipeline/revise-idea.sh --new "Title" --type {wtype}'
            )
        text = source_path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)
        if meta.get("writingType") and args.wtype == "blog_essay":
            # keep existing type unless user overrode from default intentionally —
            # if user passed --type explicitly we already have wtype; for default,
            # prefer stored writingType
            stored = meta.get("writingType")
            if stored in WRITING_TYPES:
                wtype = stored
        notes_for_append = notes

    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    pending_path = PENDING_DIR / f"{slug}.md"

    if args.save_notes_only and pending_path.is_file():
        text = pending_path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)
        append_inbox_notes(slug, notes)
        draft = build_pending_draft(
            meta, body, notes, slug, source_kind, today, wtype
        )
        pending_path.write_text(draft, encoding="utf-8")
        print(f"Saved notes → {pending_path}")
        print(f"Execute Mjidea revise job {slug}")
        return 0

    draft = build_pending_draft(
        meta, body, notes_for_append, slug, source_kind, today, wtype
    )
    pending_path.write_text(draft, encoding="utf-8")

    src_label = (
        str(source_path.relative_to(ROOT))
        if source_path
        else f"(new) {meta.get('title', slug)}"
    )
    research = write_research_scaffold(slug, notes, source_kind, today, wtype)
    job = write_job(slug, notes, today, src_label, wtype)
    ceo = write_ceo_onepager(
        slug, today, source_kind, research, pending_path, job, notes, wtype
    )
    append_inbox_notes(slug, notes)
    update_status(slug, today, wtype)

    if not args.no_catalog:
        rebuild_catalog()

    print("")
    print(f"✓ Type:     {wtype} ({WRITING_TYPES[wtype]['label']})")
    print(f"✓ Source:   {src_label} ({source_kind})")
    print(f"✓ Pending:  {pending_path.relative_to(ROOT)}")
    print(f"✓ Research: {research.relative_to(ROOT)}")
    print(f"✓ CEO:      {ceo.relative_to(ROOT)}")
    print(f"✓ Job:      {job.relative_to(ROOT)}")
    print("")
    print(f"Execute Mjidea revise job {slug}")
    print(f"(Publish later with: ./pipeline/approve.sh {slug})")
    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
