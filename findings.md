# Findings

## Competitive Landscape (2026-05-17)

### Key Competitors
- **Local Deep Research (LDR)**: ~7.4K stars, most complete. AES-256 encrypted KB, 30+ strategies, arXiv/PubMed/Semantic Scholar native. Requires RTX 3090-class GPU.
- **GPT Researcher**: Highest autonomy. Docker+Ollama. Web scraping only, no academic DB connectors. 12-min report gen.
- **Perplexica**: Perplexity clone, self-hosted. No native academic sources. SearXNG meta-search only.
- **Elicit**: Commercial. Semantic Scholar DB (125M papers). Systematic review feature. $12-79/mo.
- **ORKG ASK**: Open-source neuro-symbolic. RAG + KG. Mistral 7B. New in 2025.
- **Scite.ai**: Smart citations — classifies as supporting/contrasting. Unique differentiator.

### 研墨 Differentiation
- **Formula verification** — no competitor has this
- **Advisor requirement parsing** — unique to Chinese academic workflow
- **Plugin architecture** — user-extensible, not just configurable
- **All-in-one** — literature + evaluation + formula + writing in one desktop app
- **Local-first with encrypted data** — comparable to LDR but lighter

### Market Gaps We Fill
- AI text humanization for academic writing (de-AI) — no competitor
- Research gap analysis from paper sets — Elicit does question answering but not structured gap detection
- Chinese academic workflow support (导师沟通)
- Multi-source dedup across ArXiv+Semantic Scholar+DBLP

## Architecture Decisions

### Why Tauri over Electron
- Smaller binary (Rust vs Chromium)
- Better performance for local-first app
- Cross-platform without 150MB+ overhead
- Tradeoff: Rust toolchain required

### Why SQLite + ChromaDB over PostgreSQL
- Zero-config for users (no DB setup)
- Single-file database, easy backup
- ChromaDB for vector search without external service
- Tradeoff: concurrent access limitations (mitigated with WAL mode)

### Why Plugin Architecture
- Long-term community growth
- Users can add domain-specific features without forking
- Same interface for built-in and user plugins = dogfooding

### Why Not Microservices
- Single-user local app doesn't need distributed complexity
- Module boundaries enforced by plugin API, not network boundaries
- Easier debugging and deployment

## Technical Debt

- [ ] `latex_to_sympy()` uses sequential `str.replace()` — fragile for complex LaTeX, should use `sympy.parsing.latex`
- [ ] Audit log grows without bound (in-memory list) — needs cap or DB persistence
- [ ] API key stored in plaintext config.json — should use keyring in production
- [ ] ChromaDB Windows file lock issues during testing
- [ ] No connection pooling for SQLite (thread-local only)
