# 研墨 (YanMo) — Task Plan

## Goal

AI 科研一站式解决方案：本地优先、数据不出门、覆盖科研全流程。

## Status

Current phase: **功能完善与打磨**

## Phases

### Phase 1: Core Engine ✅
- EventBus, Config, SecurityManager, Storage, LLMRouter, PluginEngine
- API Gateway + main.py entry point

### Phase 2: Frontend Core ✅
- Workbench shell, TabBar, SidePanel, pluginRegistry
- ChatWindow, SecurityBadge, Settings
- Warm theme (Noto Sans SC, amber accents, noise texture)

### Phase 3: Built-in Plugins ✅
- 读懂导师 — parse advisor text, auto-planning with timeline
- 追新论文 — multi-source feed (ArXiv+Semantic Scholar+DBLP)
- 审项目 — project evaluation with 3-dimension scoring
- 验公式 — LaTeX verification with dual-channel SymPy cross-validation
- 写论文 — outline generator, BibTeX parser

### Phase 4: Advanced Features ✅
- Multi-source academic crawler
- AI deduplication (title similarity + arxiv_id + DOI)
- Research gap analyzer (10+ dimensions)
- De-AI text detection & cleaning
- Plugin extension system (user-installable)
- TaskScheduler (hourly auto-crawl)
- WebSocket real-time push

### Phase 5: Desktop App ✅
- Tauri wrapper (Windows/Linux/macOS)
- Cross-platform Python launcher
- Platform-specific icons

### Phase 6: Polish & Gaps 🔜
- [ ] Citation relationship graph (Connected Papers-like)
- [ ] Scheduled paper alert notifications
- [ ] Systematic review workflow
- [ ] Paper PDF annotation & notes
- [ ] Knowledge graph visualization for terminology
- [ ] Smart citation classification (supporting/contrasting)

### Phase 7: Distribution
- [ ] PyPI package
- [ ] One-click installer for Windows
- [ ] Homebrew formula for macOS
- [ ] Flatpak for Linux

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| npm cache permission | 1 | Used `--cache` flag with temp directory |
| Tauri notification plugin panic | 1 | Removed plugin, simplified to shell+opener |
| Tauri icon.ico missing | 2 | Generated multi-res ICO via Python |
| Plugin class name mismatch | 1 | Added `Plugin = XxxPlugin` alias to each |
| LiteraturePanel white screen | 1 | Added `?? []` guard on undefined data.papers |
| Workbench IIFE stale registry | 1 | Changed to render-time computation |
| INSERT before CREATE TABLE | 1 | Reordered SQL statements |
