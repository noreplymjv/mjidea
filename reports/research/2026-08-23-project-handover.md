# Mjidea (mji) & Portable AI Hub — Project Handover & System Runbook
**Date:** 2026-08-23  
**Audience:** Incoming AI Agents & Systems Administrators  
**Active Project Folder:** `/media/mj/My Passport/mjI/Mjidea`  
**Active AI Hub Folder:** `/media/mj/My Passport/Aihub`  

---

## 1. Executive Overview

This document provides a comprehensive handover runbook for the **Mjidea (mji)** standing digital company and the supporting **Portable AI Hub** environment. 

These two systems are designed to operate together:
1. **Portable AI Hub (`Aihub/`):** Contains the offline model library (117 GB of GGUF/safetensors files), environment activators, custom Python venv, standalone CLI binaries (`ollama`, `hermes`, `agy`), and REST dashboard to serve agents programmatically.
2. **Mjidea (`Mjidea/`):** The digital publishing company repository. It operates via the `.cursor/rules` workflow to write and edit philosophical essays, run multi-agent panels, and publish them via an Astro-based static website.

---

## 2. System Architecture & Components

### 2.1 The Portable AI Hub Directory (`/media/mj/My Passport/Aihub/`)

```
Aihub/
├── activate_portable.sh           # Source this first (sets PATH, OLLAMA_MODELS, HF_HOME, AGY_HOME, venv)
├── Start-AI-Hub.sh                # Main initialization script (launches Ollama + Dashboard)
├── start-quad.sh                  # 4-pane tmux workspace (Hermes, SSH to H2, SSH to H3, agy)
├── LAUNCH.html                    # Offline cross-platform visual guide with copy-paste commands
├── LAUNCH.bat                     # Windows 1-click launcher (WSL initialization, Explorer links)
├── DASHBOARD.html                 # Live web interface for status and download metrics (Port 8765)
├── bin/                           # Stripped Linux x86_64 CLI binaries (ollama, agy, hermes)
├── .venv/                         # Standalone Python 3.12 environment (PyTorch, transformers, flask)
├── models/                        # Curated model files partitioned into 6 tiers (01_ECO to 06_API_ONLY)
├── data/                          # Redirected state caches (Ollama blobs, HF caches, Hermes memory)
├── config/                        # Generated runtime environments (ollama.env)
├── scripts/                       # Core telemetry, download runners, and startup management
└── manifests/                     # Machine deployment profiles and master indices (00_INDEX.json)
```

---

## 3. Environment Variables & Paths (Crucial for Portability)

When `activate_portable.sh` is sourced, the following overrides are exported. **Incoming agents must never hardcode home directories** (like `/home/mj/`) or active drive mounts:

* `PORTABLE_ROOT` — Dynamically resolved using `BASH_SOURCE[0]`. Points to the `Aihub/` root path.
* `PATH` — Prepends `$PORTABLE_ROOT/bin` to path so portable binaries execute first.
* `OLLAMA_MODELS` — Redirected to `$PORTABLE_ROOT/data/ollama`.
* `HF_HOME` & `HUGGINGFACE_HUB_CACHE` — Redirected to `$PORTABLE_ROOT/data/hf_cache/` and `$PORTABLE_ROOT/data/hf_cache/hub/`.
* `HERMES_HOME` & `AGY_HOME` — Redirected to `$PORTABLE_ROOT/data/hermes` and `$PORTABLE_ROOT/data/antigravity`.

---

## 4. Curated Model Library & Routing Logic

Ollama and HuggingFace models are divided into 6 distinct tiers based on **VRAM Headroom Rules** (*Model Weight + 20–30% buffer for KV Cache & Context*).

### 4.1 Tier Specification Matrix
* **`01_ECO` (CPU / 8-16GB RAM):** `phi4-mini` (reasoning), `qwen2.5:3b` (general chat), `qwen2.5-coder:3b` (coding), `gemma3:1b` (chat), `nomic-embed-text` (embeddings), `kokoro-82m` (TTS), `moonshine` (STT), `moondream2` (VLM).
* **`02_MID` (2-6GB VRAM):** `deepseek-r1:7b` (reasoning distill), `qwen2.5-coder:7b` (coding), `llama3.1:8b` (RAG chat), `faster-whisper-large-v3` (STT), `bge-m3` (embeddings), `qwen2.5-vl-3b` (vision).
* **`03_HEAVY` (8-16GB VRAM):** `deepseek-r1:14b` (reasoning), `qwen2.5-coder:14b` (coding), `devstral-small-2-24b` (agentic coding), `gemma-4-26b-a4b-qat` (analysis), `qwen2.5-vl-7b` (vision), `sdxl-turbo` (image).
* **`04_SUPER_HEAVY` (24-32GB VRAM):** `qwq:32b` (reasoning), `qwen2.5-coder:32b` (coding), `qwen2.5:32b` (chat), `qwen2.5-vl-14b` (vision), `wan-2.2` (video), `flux-dev` (image), `ltx-video` (video).
* **`05_SERVER` (48GB+ VRAM):** `llama3.3:70b`, `qwen3.6:72b`, `llama-4-scout-int4`.
* **`06_API_ONLY` (Cloud fallback):** `GLM-5.2` (Z.ai API), `Kimi K2.6` (Moonshot API), `DeepSeek-V4-Pro` / `R2` (DeepSeek API), `MiniMax M3`.

---

## 5. Startup & Operational Runbook

### 5.1 Initial Setup on a New Host
1. Plug in the WD Passport drive.
2. In the terminal, run the master startup script:
   ```bash
   cd "/media/mj/My Passport/Aihub"
   ./Start-AI-Hub.sh
   ```
   *This starts the portable Ollama server (bound to the SSD store) and launches the visual dashboard backend on port 8765.*
3. Open `DASHBOARD.html` in your browser to check download status.

### 5.2 Launching the Workspace (Tmux)
Run:
```bash
./start-quad.sh
```
This spawns a tmux session with four panes:
* **Pane 0 (Top-Left):** Local Hermes agent environment.
* **Pane 1 (Top-Right):** SSH console to H2 (Raspberry Pi).
* **Pane 2 (Bottom-Left):** SSH console to H3 (Antigravity box).
* **Pane 3 (Bottom-Right):** Auxiliary shell (active `agy` workspace).

---

## 6. Handover Instructions for Gated Models
* **HuggingFace Tokens:** Gated models (like Gemma-3/4 and Devstral) require license acceptance on HuggingFace. Create a file named `/media/mj/My Passport/Aihub/manifests/.hf_token` containing your HuggingFace Read token. The dashboard's background download runner will automatically load and export this token during download cycles.

---

## 7. Mjidea Project Pipeline Execution
* **CEO Intake:** Place raw draft markdown ideas under `Mjidea/inbox/`.
* **Auto-run cycles:** The editor panel operates under rules defined in `.cursor/rules/mjidea-autorun.mdc`.
* **Deliverable Reports:** Standard Markdown reports must always dual-write to their respective folders inside `reports/` (e.g. `reports/audit/`, `reports/seo/`, `reports/growth/`). This guideline is enforced globally on this host via `/home/mj/.agents/rules/reports_rule.md`.
