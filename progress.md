# Progress Log

## Session: 2026-05-17

### Initial Build (morning)
- Project scaffolding: pyproject.toml, package.json, directory structure
- Core engine: EventBus, Config, SecurityManager, Storage, LLMRouter, PluginEngine
- 25 core tests passing

### Frontend Shell (midday)
- Workbench + TabBar + SidePanel + pluginRegistry
- ChatWindow, SecurityBadge, Settings components
- TypeScript types + API client
- Vite build successful

### 5 Plugin Backends (afternoon)
- term-advisor: advisor text parsing + auto-planning with timeline
- literature: ArXiv fetcher + feed with interests
- evaluator: 3-dimension project scoring
- formula: LaTeX → SymPy dual-channel verification
- paper-writer: outline generator + BibTeX parser
- 41 tests total

### Plugin Frontends + Wiring (late afternoon)
- All 5 frontend panels with functional UIs
- Plugin auto-loading on startup
- Integration smoke tests
- 43 tests passing → 49 after term-advisor expansion

### Term-Advisor Enhancement
- Auto-planning: phase assignment, dependency ordering, time estimation
- Expansion templates for 7 task types
- Bilingual parser (Chinese + English action keywords)
- Timeline generation

### Literature Redesign
- News-feed layout with interests-based auto-fetch
- Collapsible search, keyword tags, time-ago labels
- NEW badges for recent papers

### Warm Theme Redesign
- Noto Sans SC + Noto Serif SC typography
- Cream background + warm amber accents
- SVG noise texture overlay
- Asymmetric chat bubbles
- Greeting header with time-of-day message
- 14 files changed

### Code Review + Bugfixes (evening)
- 8 blocking + 7 important issues fixed
- Settings→LLMRouter propagation, INSERT before CREATE TABLE, bare except, hash() non-determinism, KeyError in summarizer, duplicate keyword in evaluator, nested brace regex
- EventBus return_exceptions, shared httpx client, WAL mode, HTTP timeout, input validation

### Project Rename
- 科研助手 → 研墨 (YanMo)
- 9 files updated, data dir ~/.yanmo

### Advanced Features (night)
- TaskScheduler with hourly auto-crawl
- WebSocket /api/ws for real-time paper push
- AI dedup: title similarity + arxiv_id + DOI
- Gap analyzer: 10+ dimension heuristic detection with field-specific suggestions
- De-AI: pattern detection + cleaning for academic text
- Frontend: gap analysis button in LiteraturePanel, de-AI section in PaperWriterPanel
- Lifespan-based startup (replaces @app.on_event)

### Desktop App Packaging
- Rust + Tauri CLI installed
- Cross-platform lib.rs (python3 on Unix, python on Windows)
- Multi-res ICO icon (7 sizes)
- Tauri config: deb/rpm for Linux, app for macOS, MSI for Windows
- cargo build successful, yanmo.exe runs

### README + GitHub
- Humanized README (Chinese, no AI vocabulary)
- Clean git history (single orphan commit)
- Pushed to https://github.com/sixtdreanight/Yanmo

## Test Status
- **49 passed, 0 failed, 1 warning** (ChromaDB deprecation, harmless)
- TypeScript: 0 errors
- Vite build: successful
- Cargo build: successful

## File Count
- Python: 34 source files
- TypeScript: 16 source files
- Tests: 15 files
- Total: ~66 source files
