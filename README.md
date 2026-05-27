**Language:** [English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-Hant.md) | [日本語](README.ja.md)

# Yanmo (研墨)

[![Tests](https://img.shields.io/badge/tests-49%20passed-green)](https://github.com/sixtdreanight/Yanmo/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

**A research assistant that runs on your own machine. Your data stays put.**

Unlike general-purpose AI chat, Yanmo is purpose-built for researchers: deconstruct vague advisor directions, track papers across multiple sources, cross-validate formula derivations, evaluate project proposals objectively, and assist with thesis writing. Five purpose-built tools, each with its own interface — not crammed into a single chat box.

Three core principles: **data stays local, formulas must not be wrong, plugin system for extensibility.** Plus AI-powered dedup, research gap finder, and AI-text humanizer.

Desktop application, not a web app. Runs on Windows, Linux, and macOS.

---

## Installation

Requires Python 3.11+, Node.js 18+, and Ollama.

```bash
pip install -e ".[dev]"
python -m backend.main
```

Backend runs at `127.0.0.1:8000`. Then start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### Desktop App

> **Note (2026-05):** The primary supported frontend is the React Web app (`frontend/`).
> The Tauri desktop shell (`frontend/src-tauri/`) and the Qt frontend (`frontend_qt/`) are
> **deprecated** and will be removed in a future release. Maintaining three frontends is
> unsustainable for a small team. If you rely on the Tauri or Qt frontend, please open an
> issue to discuss migration to the Web frontend.

---

## Features

Five tabs across the top (+ chat panel on the right): Advisor Decoder, Paper Tracker, Project Reviewer, Formula Validator, Thesis Writer.

### Advisor Decoder

Paste your advisor's words. Auto-decomposes into executable tasks with ordering and time estimates. Each task expands to show sub-steps and suggested resources. Advisor data is classified as confidential, forced to local model only.

### Paper Tracker

Set research keywords. Parallel fetches from ArXiv, Semantic Scholar, and DBLP. Papers displayed in a feed with one-click Chinese summaries. Auto-updates every hour in the background.

Triple dedup (title similarity + arxiv_id + DOI) ensures no preprint appears twice. Click "Find Ideas" to analyze the current paper list across 10+ dimensions (theory, efficiency, robustness, fairness, etc.), flagging research gaps sorted by confidence.

### Project Reviewer

Submit a project name and description. Scores on three dimensions — novelty, soundness, methodology — with specific weaknesses and improvement suggestions.

### Formula Validator

Split-pane LaTeX source and rendered preview. Submit for dual-channel validation: basic checks (bracket matching, division by zero, domain) + SymPy symbolic computation. Both channels must pass for a green light. No LLM involved — pure local symbolic computation.

### Thesis Writer

Generates structured outlines with estimated word counts. Supports BibTeX paste-and-parse. Bottom panel has an "AI-text humanizer" tool that detects AI writing traces and auto-cleans.

---

## Plugin System

Plugins live in `~/.yanmo/plugins/`. Load them via Settings → Plugin Manager. Minimum requirement: `plugin.toml` + `plugin.py`. See `plugin_schema/API.md` for the development guide. Supports lifecycle management, hot-load/unload, and event bus.

---

## Architecture

| Component | Description |
|---|---|
| Plugin Engine | Lifecycle management, hot-load/unload, event bus |
| Task Scheduler | Auto-fetch papers hourly |
| WebSocket | Real-time push of paper updates to frontend |
| Security Layer | 3-tier data classification + cloud operation interception + audit logs |
| Storage | SQLite (structured) + ChromaDB (vectors) + local files |

## Data Security

Default: all operations use local Ollama. Cloud API keys are optional — if you don't fill them in, nothing leaves your machine.

- Confidential data is forced local; cloud operations are auto-blocked
- Cloud outbound traffic has audit logs
- Data stored in `~/.yanmo/`, backup anytime

## Tech Stack

| Layer | Stack |
|---|---|
| Backend | Python, FastAPI, SQLite, ChromaDB, SymPy, SciPy |
| Frontend | React 18, TypeScript, Vite, KaTeX |
| Desktop Shell | Tauri (Rust) |
| Fonts | Noto Sans SC, Noto Serif SC |

## Related

- [myBlog](https://github.com/sixtdreanight/myBlog) — Author's blog, more research-related articles

## License

MIT

---

<div align="center">

**Language / 语言 / 言語**

[**English**](README.md) | [**简体中文**](README.zh-CN.md) | [**繁體中文**](README.zh-Hant.md) | [**日本語**](README.ja.md)

</div>
