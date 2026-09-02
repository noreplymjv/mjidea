#!/usr/bin/env python3
"""Build universal writing catalog for Mjidea Idea Editor / Writing Desk.

Scans:
  - drafts/pending/*.md
  - site/src/content/blog/*.md
  - inbox/*.md (seeds)

Writes:
  - social/writing_catalog.json  (canonical, all items)
  - social/idea_catalog.json     (same payload — UI compat)

Does NOT publish. Safe to re-run anytime.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "drafts" / "pending"
BLOG = ROOT / "site" / "src" / "content" / "blog"
INBOX = ROOT / "inbox"
OUT_WRITING = ROOT / "social" / "writing_catalog.json"
OUT_IDEA = ROOT / "social" / "idea_catalog.json"

BLANK_ITEM = {
    "slug": "__new__",
    "title": "＋ New blank piece",
    "description": "Start any genre — essay, column, social pack, freeform.",
    "category": "any",
    "author": "Mayank Jain",
    "status": "new",
    "source": "blank",
    "path": "",
    "writing_type": "freeform",
    "tags": [],
    "pubDate": "",
}


def parse_frontmatter(text: str) -> dict:
    meta: dict = {}
    if not text.startswith("---"):
        return meta
    parts = text.split("---", 2)
    if len(parts) < 3:
        return meta
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        meta[key] = val
    return meta


def parse_tags(raw: str) -> list[str]:
    if not raw:
        return []
    # tags: ["a", "b"] or tags: [a, b]
    inner = raw.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    tags = []
    for part in inner.split(","):
        t = part.strip().strip('"').strip("'")
        if t:
            tags.append(t)
    return tags


def guess_writing_type(meta: dict, status: str) -> str:
    cat = (meta.get("category") or "").lower()
    tags = " ".join(parse_tags(meta.get("tags", ""))).lower()
    blob = f"{cat} {tags} {meta.get('title', '')}".lower()
    if any(k in blob for k in ("linkedin", "twitter", "social", "thread", "caption")):
        return "social"
    if any(k in blob for k in ("news", "journalism", "analysis", "report")):
        return "journalist"
    if any(k in blob for k in ("parenting", "money", "financial", "humanity", "life", "tech", "ai")):
        return "column"
    if status == "inbox":
        return "seed"
    return "blog_essay"


def entry_from_md(path: Path, status: str, source: str) -> dict | None:
    if path.suffix != ".md" or path.name.startswith(".") or path.name == ".gitkeep":
        return None
    if path.name.upper().startswith("TEMPLATE") or "TEMPLATE" in path.name:
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    meta = parse_frontmatter(text)
    slug = path.stem
    # inbox dated files: 2026-08-21-trust-isnt-certified → keep full stem as slug id
    title = meta.get("title")
    if not title:
        # first # heading or slug
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = m.group(1).strip() if m else slug.replace("-", " ").title()
    tags = parse_tags(meta.get("tags", ""))
    item = {
        "slug": slug,
        "title": title,
        "description": meta.get("description", "")[:280],
        "category": meta.get("category") or ("inbox" if status == "inbox" else "philosophy"),
        "author": meta.get("author", "Mayank Jain"),
        "status": status,
        "source": source,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "writing_type": guess_writing_type(meta, status),
        "tags": tags,
        "pubDate": meta.get("pubDate", ""),
    }
    if status == "published":
        # live URL slug often matches filename
        live_slug = slug
        item["live_url"] = f"/ideas/{live_slug}/"
    return item


def build_catalog() -> dict:
    items: list[dict] = [dict(BLANK_ITEM)]
    # Prefer pending over published when same slug — index by slug
    by_slug: dict[str, dict] = {}

    if PENDING.is_dir():
        for path in sorted(PENDING.glob("*.md")):
            e = entry_from_md(path, "pending", "drafts/pending")
            if e:
                # If published twin exists later, mark it
                by_slug[e["slug"]] = e

    if BLOG.is_dir():
        for path in sorted(BLOG.glob("*.md")):
            e = entry_from_md(path, "published", "blog")
            if not e:
                continue
            if e["slug"] in by_slug:
                by_slug[e["slug"]]["published_path"] = e["path"]
                by_slug[e["slug"]]["live_url"] = e.get("live_url")
                # Keep pending as primary status but note published twin
                by_slug[e["slug"]]["has_published"] = True
            else:
                by_slug[e["slug"]] = e

    if INBOX.is_dir():
        for path in sorted(INBOX.glob("*.md")):
            e = entry_from_md(path, "inbox", "inbox")
            if not e:
                continue
            # Use unique key if slug collides
            key = e["slug"]
            if key in by_slug:
                key = f"inbox::{e['slug']}"
                e["slug"] = key
                e["inbox_slug"] = path.stem
            by_slug[key] = e

    items.extend(by_slug.values())

    def sort_key(e: dict):
        if e.get("slug") == "__new__":
            return (0, "")
        status_rank = {"pending": 1, "inbox": 2, "published": 3, "new": 0}.get(e.get("status"), 9)
        return (status_rank, (e.get("title") or "").lower())

    items.sort(key=sort_key)

    counts = {"pending": 0, "published": 0, "inbox": 0, "new": 0}
    for e in items:
        st = e.get("status", "")
        if st in counts:
            counts[st] += 1

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(items),
        "counts": counts,
        "writing_types": [
            "blog_essay",
            "columnist",
            "journalist",
            "social",
            "short_long",
            "parenting",
            "money",
            "humanity",
            "life",
            "tech",
            "freeform",
            "seed",
        ],
        "items": items,
        "notes": (
            "Universal writing desk catalog. Revise always writes to drafts/pending/ "
            "(never auto-publish). Approve gate: ./pipeline/approve.sh <slug>"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build Mjidea universal writing catalog")
    ap.add_argument("-o", "--output", type=Path, default=OUT_WRITING)
    args = ap.parse_args()

    catalog = build_catalog()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    # Compat mirror for older UI paths
    OUT_IDEA.write_text(payload, encoding="utf-8")
    c = catalog["counts"]
    print(
        f"Wrote {args.output} + {OUT_IDEA.name} "
        f"({catalog['count']} items: pending={c['pending']} published={c['published']} inbox={c['inbox']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
