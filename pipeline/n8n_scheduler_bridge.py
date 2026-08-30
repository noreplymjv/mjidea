#!/usr/bin/env python3
"""
Mjidea Continuous Scheduler & n8n Bridge Daemon
Monitors `social/scheduler_queue.json` and automatically triggers:
1. Approved blog publishing to Astro site (`site/src/content/blog/`)
2. Asset sync to `site/public/visuals/`
3. Dispatch to local or cloud n8n webhook (`http://localhost:5678/webhook/mjidea-publish`)
4. Social distribution logging & status reports
"""

import os
import sys
import json
import time
import shutil
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

MJIDEA_ROOT = Path("/media/mj/My Passport/mjI/Mjidea")
QUEUE_FILE = MJIDEA_ROOT / "social" / "scheduler_queue.json"
SITE_BLOG_DIR = MJIDEA_ROOT / "site" / "src" / "content" / "blog"
SITE_VISUALS_DIR = MJIDEA_ROOT / "site" / "public" / "visuals"
LOG_FILE = MJIDEA_ROOT / "social" / "scheduler.log"

SITE_BLOG_DIR.mkdir(parents=True, exist_ok=True)
SITE_VISUALS_DIR.mkdir(parents=True, exist_ok=True)


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def publish_item(item: dict, n8n_url: str = "http://localhost:5678/webhook/mjidea-publish") -> bool:
    slug = item.get("slug")
    payload = item.get("payload", {})
    blog_data = payload.get("blog", {})
    markdown = blog_data.get("markdown")
    
    if not slug or not markdown:
        log(f"⚠️ Skipping invalid item: {slug}")
        return False

    log(f"🚀 Processing approved thought: {slug} - '{item.get('title')}'")

    # 1. Write Blog Post to Astro
    target_blog_file = SITE_BLOG_DIR / f"{slug}.md"
    target_blog_file.write_text(markdown, encoding="utf-8")
    log(f"📄 Published Blog to Astro: {target_blog_file}")

    # 2. Copy Visual Assets if available
    src_visuals = MJIDEA_ROOT / "assets" / "visuals" / slug
    if src_visuals.exists():
        dest_visuals = SITE_VISUALS_DIR / slug
        dest_visuals.mkdir(parents=True, exist_ok=True)
        for f in src_visuals.glob("*.*"):
            shutil.copy2(f, dest_visuals / f.name)
        log(f"🖼️ Mirrored visuals to public web directory: {dest_visuals}")

    # 3. Trigger n8n Webhook
    webhook_sent = False
    try:
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            n8n_url,
            data=req_data,
            headers={"Content-Type": "application/json", "User-Agent": "Mjidea-Scheduler/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            log(f"⚡ n8n Webhook triggered successfully (HTTP {resp.status})")
            webhook_sent = True
    except Exception as e:
        log(f"ℹ️ n8n Webhook at {n8n_url} not active or skipped ({e}). Handled via local engine.")

    # 4. Mark as Published
    item["status"] = "published"
    item["published_at"] = datetime.now().isoformat()
    item["n8n_dispatched"] = webhook_sent
    return True


def run_cycle(once: bool = False, n8n_url: str = "http://localhost:5678/webhook/mjidea-publish"):
    if not QUEUE_FILE.exists():
        log("No queue file found. Standing by.")
        return

    try:
        queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        log(f"Error reading queue: {e}")
        return

    modified = False
    for item in queue:
        # Check if item is marked approved
        if item.get("status") == "approved":
            success = publish_item(item, n8n_url=n8n_url)
            if success:
                modified = True

    if modified:
        QUEUE_FILE.write_text(json.dumps(queue, indent=2), encoding="utf-8")
        log("💾 Queue ledger updated.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mjidea Continuous Scheduler Bridge")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit")
    parser.add_argument("--interval", type=int, default=15, help="Interval in seconds between checks")
    parser.add_argument("--n8n-url", default="http://localhost:5678/webhook/mjidea-publish", help="n8n Webhook URL")
    parser.add_argument("--approve", help="Approve a specific slug in queue and publish immediately")

    args = parser.parse_args()

    log("=== Mjidea Scheduler & n8n Bridge Started ===")

    if args.approve:
        if QUEUE_FILE.exists():
            queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
            for item in queue:
                if item.get("slug") == args.approve:
                    item["status"] = "approved"
                    log(f"✅ Approved slug '{args.approve}' in queue.")
            QUEUE_FILE.write_text(json.dumps(queue, indent=2), encoding="utf-8")
            run_cycle(once=True, n8n_url=args.n8n_url)
            return

    if args.once:
        run_cycle(once=True, n8n_url=args.n8n_url)
        return

    try:
        while True:
            run_cycle(once=False, n8n_url=args.n8n_url)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        log("=== Scheduler Bridge Stopped by User ===")


if __name__ == "__main__":
    main()
