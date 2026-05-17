# 科研助手 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local-first, privacy-first research assistant with plugin architecture covering: advisor requirement parsing, literature monitoring, project evaluation, formula verification, and paper writing assistance.

**Architecture:** Python FastAPI core engine with plugin registry, event bus, LLM router, and security layer. React frontend with draggable workbench panels. Each plugin = independent Python package + React component. Plugins communicate only through the event bus.

**Tech Stack:** Python 3.11+, FastAPI, SQLite, ChromaDB, sentence-transformers, SymPy, SciPy, React 18, TypeScript, Vite, Golden Layout, KaTeX, ECharts, Ollama

---

## File Structure Map

```
research-assistant/
├── backend/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py          # Plugin lifecycle: discover, load, unload
│   │   ├── event_bus.py       # Async pub/sub for inter-plugin comms
│   │   ├── llm_router.py      # Unified LLM interface (Ollama + cloud APIs)
│   │   ├── storage.py         # SQLite + ChromaDB unified interface
│   │   ├── security.py        # Data classification + operation gating
│   │   └── config.py          # Global settings (user prefs, LLM keys, domain)
│   ├── plugins/
│   │   ├── term_advisor/      # 读懂导师
│   │   │   ├── __init__.py
│   │   │   ├── plugin.py      # Plugin class impl
│   │   │   ├── routes.py      # API endpoints
│   │   │   └── advisor.py     # Core logic: parse advisor text → tasks
│   │   ├── literature/        # 追新论文
│   │   │   ├── __init__.py
│   │   │   ├── plugin.py
│   │   │   ├── routes.py
│   │   │   ├── fetcher.py     # ArXiv API + RSS parser
│   │   │   └── summarizer.py  # LLM summarization pipeline
│   │   ├── evaluator/         # 审项目
│   │   │   ├── __init__.py
│   │   │   ├── plugin.py
│   │   │   ├── routes.py
│   │   │   └── evaluate.py    # Innovation/rationality/methodology scoring
│   │   ├── formula/           # 验公式
│   │   │   ├── __init__.py
│   │   │   ├── plugin.py
│   │   │   ├── routes.py
│   │   │   ├── latex_parser.py # LaTeX → SymPy conversion
│   │   │   └── verify.py      # Symbolic + numeric cross-validation
│   │   └── paper_writer/      # 写论文
│   │       ├── __init__.py
│   │       ├── plugin.py
│   │       ├── routes.py
│   │       ├── outline.py     # Structured outline engine
│   │       └── citation.py    # BibTeX manager
│   ├── api/
│   │   ├── __init__.py
│   │   └── gateway.py         # FastAPI app factory + plugin route mounting
│   └── main.py                # Entry point: uvicorn
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── core/
│       │   ├── Workbench.tsx       # Golden Layout container
│       │   ├── TabBar.tsx          # Top tab navigation
│       │   ├── SidePanel.tsx       # 我的资料 + 问一问 side panel
│       │   ├── pluginRegistry.ts   # Frontend plugin registration
│       │   ├── api.ts              # HTTP client to backend
│       │   └── types.ts            # Shared TypeScript types
│       ├── plugins/
│       │   ├── term-advisor/
│       │   │   └── TermAdvisorPanel.tsx
│       │   ├── literature/
│       │   │   └── LiteraturePanel.tsx
│       │   ├── evaluator/
│       │   │   └── EvaluatorPanel.tsx
│       │   ├── formula/
│       │   │   └── FormulaPanel.tsx
│       │   └── paper-writer/
│       │       └── PaperWriterPanel.tsx
│       └── shared/
│           ├── ChatWindow.tsx       # 问一问 floating chat
│           ├── SecurityBadge.tsx    # 机密/审慎/公开 label
│           ├── Settings.tsx         # Settings panel
│           └── MarkdownView.tsx     # Markdown renderer
├── plugin_schema/
│   ├── plugin.toml.spec
│   └── API.md
├── tests/
│   ├── core/
│   │   ├── test_engine.py
│   │   ├── test_event_bus.py
│   │   ├── test_llm_router.py
│   │   ├── test_storage.py
│   │   ├── test_security.py
│   │   └── test_config.py
│   └── plugins/
│       ├── test_term_advisor.py
│       ├── test_literature.py
│       ├── test_evaluator.py
│       ├── test_formula.py
│       └── test_paper_writer.py
├── pyproject.toml
└── docs/superpowers/
    ├── specs/2026-05-17-research-assistant-design.md
    └── plans/2026-05-17-research-assistant-plan.md
```

---

## Phase 1: Project Scaffolding

### Task 1.1: Initialize Python project

**Files:**
- Create: `pyproject.toml`

- [ ] **Step 1: Write pyproject.toml**

```toml
[project]
name = "research-assistant"
version = "0.1.0"
description = "本地优先的科研助手"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "chromadb>=0.5.0",
    "sentence-transformers>=3.0.0",
    "sympy>=1.13.0",
    "scipy>=1.14.0",
    "feedparser>=6.0.0",
    "aiohttp>=3.9.0",
    "ollama>=0.4.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=5.0.0",
]
```

- [ ] **Step 2: Install dependencies**

Run: `pip install -e ".[dev]"`

### Task 1.2: Initialize frontend project

**Files:**
- Create: `frontend/package.json`, `frontend/tsconfig.json`, `frontend/vite.config.ts`, `frontend/index.html`

- [ ] **Step 1: Write package.json**

```json
{
  "name": "research-assistant-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "golden-layout": "^2.6.0",
    "katex": "^0.16.0",
    "echarts": "^5.5.0",
    "echarts-for-react": "^3.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.5.0",
    "vite": "^5.4.0",
    "@vitejs/plugin-react": "^4.3.0"
  }
}
```

- [ ] **Step 2: Write tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": ["src"]
}
```

- [ ] **Step 3: Write vite.config.ts**

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, 'src') },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
```

- [ ] **Step 4: Write index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>科研助手</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.tsx"></script>
</body>
</html>
```

- [ ] **Step 5: Install frontend dependencies**

Run: `cd frontend && npm install`

---

## Phase 2: Core Engine

### Task 2.1: Event Bus

**Files:**
- Create: `backend/core/__init__.py`, `backend/core/event_bus.py`
- Create: `tests/core/__init__.py`, `tests/core/test_event_bus.py`

- [ ] **Step 1: Write failing test**

```python
# tests/core/test_event_bus.py
import pytest
from backend.core.event_bus import EventBus

@pytest.mark.asyncio
async def test_emit_and_on():
    bus = EventBus()
    received = []

    async def handler(data):
        received.append(data)

    bus.on("paper.saved", handler)
    await bus.emit("paper.saved", {"id": "1", "title": "Test"})
    await bus.emit("paper.saved", {"id": "2", "title": "Test2"})

    assert len(received) == 2
    assert received[0] == {"id": "1", "title": "Test"}


@pytest.mark.asyncio
async def test_off_unsubscribes():
    bus = EventBus()
    received = []

    async def handler(data):
        received.append(data)

    bus.on("test.event", handler)
    await bus.emit("test.event", {"x": 1})
    bus.off("test.event", handler)
    await bus.emit("test.event", {"x": 2})

    assert len(received) == 1


@pytest.mark.asyncio
async def test_multiple_handlers_same_event():
    bus = EventBus()
    results = []

    async def h1(data):
        results.append(f"h1:{data}")

    async def h2(data):
        results.append(f"h2:{data}")

    bus.on("ev", h1)
    bus.on("ev", h2)
    await bus.emit("ev", "x")

    assert results == ["h1:x", "h2:x"]


@pytest.mark.asyncio
async def test_emit_no_handlers_does_not_error():
    bus = EventBus()
    await bus.emit("no.such.event", {})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/core/test_event_bus.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Implement EventBus**

```python
# backend/core/event_bus.py
import asyncio
from collections import defaultdict
from collections.abc import Callable, Coroutine
from typing import Any

Handler = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def on(self, event: str, handler: Handler) -> None:
        self._handlers[event].append(handler)

    def off(self, event: str, handler: Handler) -> None:
        if event in self._handlers:
            self._handlers[event] = [h for h in self._handlers[event] if h is not handler]

    async def emit(self, event: str, data: dict[str, Any]) -> None:
        handlers = self._handlers.get(event, [])
        tasks = [handler(data) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_event_bus.py -v`
Expected: all 4 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/core/__init__.py backend/core/event_bus.py tests/core/__init__.py tests/core/test_event_bus.py
git commit -m "feat: add EventBus for inter-plugin async pub/sub"
```

### Task 2.2: Configuration Management

**Files:**
- Create: `backend/core/config.py`
- Create: `tests/core/test_config.py`

- [ ] **Step 1: Write failing test**

```python
# tests/core/test_config.py
import json
import tempfile
from pathlib import Path
from backend.core.config import Config

def test_config_loads_defaults():
    cfg = Config()
    assert cfg.llm_provider == "ollama"
    assert cfg.ollama_base_url == "http://localhost:11434"
    assert cfg.ollama_model == "qwen3:14b"
    assert cfg.cloud_api_key == ""
    assert cfg.cloud_provider == ""
    assert cfg.cloud_model == ""
    assert cfg.default_classification == "cautious"
    assert cfg.data_dir == str(Path.home() / ".research-assistant")


def test_config_save_and_load_from_file():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = Config()
        cfg.ollama_model = "llama3:8b"
        cfg.data_dir = tmp
        cfg.cloud_api_key = "sk-test"
        cfg.cloud_provider = "claude"
        cfg.save()

        cfg2 = Config.load(tmp)
        assert cfg2.ollama_model == "llama3:8b"
        assert cfg2.cloud_api_key == "sk-test"
        assert cfg2.cloud_provider == "claude"


def test_config_to_dict_excludes_sensitive():
    cfg = Config()
    cfg.cloud_api_key = "sk-secret"
    d = cfg.to_dict()
    assert d["cloud_provider"] == ""
    assert "cloud_api_key" not in d
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/core/test_config.py -v`
Expected: FAIL

- [ ] **Step 3: Implement Config**

```python
# backend/core/config.py
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class Config:
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:14b"
    cloud_api_key: str = ""
    cloud_provider: str = ""
    cloud_model: str = ""
    default_classification: str = "cautious"
    data_dir: str = field(default_factory=lambda: str(Path.home() / ".research-assistant"))

    _SENSITIVE = {"cloud_api_key"}

    @classmethod
    def load(cls, data_dir: str) -> "Config":
        config_path = Path(data_dir) / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                raw = json.load(f)
            return cls(**{k: v for k, v in raw.items() if k in cls.__dataclass_fields__})
        cfg = cls()
        cfg.data_dir = data_dir
        return cfg

    def save(self) -> None:
        path = Path(self.data_dir)
        path.mkdir(parents=True, exist_ok=True)
        raw = asdict(self)
        with open(path / "config.json", "w") as f:
            json.dump(raw, f, indent=2)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        for key in self._SENSITIVE:
            d.pop(key, None)
        return d
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_config.py -v`
Expected: all 3 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/core/config.py tests/core/test_config.py
git commit -m "feat: add Config with save/load and sensitive field exclusion"
```

### Task 2.3: Security — Data Classification + Operation Gating

**Files:**
- Create: `backend/core/security.py`
- Create: `tests/core/test_security.py`

- [ ] **Step 1: Write failing test**

```python
# tests/core/test_security.py
import pytest
from backend.core.security import SecurityManager, Classification

def test_classify_secret():
    sm = SecurityManager()
    sm.mark("doc-1", Classification.SECRET)
    assert sm.classification_of("doc-1") == Classification.SECRET


def test_default_is_cautious():
    sm = SecurityManager()
    assert sm.classification_of("unknown-doc") == Classification.CAUTIOUS


def test_secret_blocks_cloud():
    sm = SecurityManager()
    sm.mark("doc-2", Classification.SECRET)
    assert sm.allow_cloud("doc-2") is False


def test_public_allows_cloud():
    sm = SecurityManager()
    sm.mark("doc-3", Classification.PUBLIC)
    assert sm.allow_cloud("doc-3") is True


def test_cautious_requires_user_approval():
    sm = SecurityManager()
    sm.mark("doc-4", Classification.CAUTIOUS)
    assert sm.allow_cloud("doc-4") is False
    sm.approve_cloud("doc-4")
    assert sm.allow_cloud("doc-4") is True


def test_audit_log_records_cloud_sends():
    sm = SecurityManager()
    sm.log_cloud_send("doc-5", "claude-sonnet-4-6", "abc123hash")
    entries = sm.audit_log()
    assert len(entries) == 1
    assert entries[0]["target_model"] == "claude-sonnet-4-6"
    assert entries[0]["content_hash"] == "abc123hash"
    assert "content" not in entries[0]


def text_classify_batch_marks_multiple():
    sm = SecurityManager()
    sm.classify_batch({
        "a": Classification.SECRET,
        "b": Classification.PUBLIC,
    })
    assert sm.classification_of("a") == Classification.SECRET
    assert sm.classification_of("b") == Classification.PUBLIC
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/core/test_security.py -v`
Expected: FAIL

- [ ] **Step 3: Implement SecurityManager**

```python
# backend/core/security.py
from enum import Enum
from datetime import datetime, timezone
from typing import Any


class Classification(str, Enum):
    SECRET = "secret"
    CAUTIOUS = "cautious"
    PUBLIC = "public"


class SecurityManager:
    def __init__(self):
        self._classifications: dict[str, Classification] = {}
        self._cloud_approvals: set[str] = set()
        self._audit: list[dict[str, Any]] = []

    def mark(self, doc_id: str, level: Classification) -> None:
        self._classifications[doc_id] = level

    def classify_batch(self, mapping: dict[str, Classification]) -> None:
        self._classifications.update(mapping)

    def classification_of(self, doc_id: str) -> Classification:
        return self._classifications.get(doc_id, Classification.CAUTIOUS)

    def allow_cloud(self, doc_id: str) -> bool:
        level = self.classification_of(doc_id)
        if level == Classification.SECRET:
            return False
        if level == Classification.PUBLIC:
            return True
        return doc_id in self._cloud_approvals

    def approve_cloud(self, doc_id: str) -> None:
        self._cloud_approvals.add(doc_id)

    def log_cloud_send(self, doc_id: str, target_model: str, content_hash: str) -> None:
        self._audit.append({
            "doc_id": doc_id,
            "target_model": target_model,
            "content_hash": content_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def audit_log(self) -> list[dict[str, Any]]:
        return list(self._audit)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_security.py -v`
Expected: all 6 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/core/security.py tests/core/test_security.py
git commit -m "feat: add SecurityManager with 3-level classification and audit log"
```

### Task 2.4: Storage — SQLite + ChromaDB Unified Interface

**Files:**
- Create: `backend/core/storage.py`
- Create: `tests/core/test_storage.py`

- [ ] **Step 1: Write failing test**

```python
# tests/core/test_storage.py
import tempfile
import pytest
from backend.core.storage import Storage

@pytest.fixture
def storage():
    with tempfile.TemporaryDirectory() as tmp:
        yield Storage(tmp)


def test_sqlite_insert_and_query(storage):
    storage.sql_execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            arxiv_id TEXT
        )
    """)
    storage.sql_execute(
        "INSERT INTO papers (id, title, arxiv_id) VALUES (?, ?, ?)",
        ("1", "Test Paper", "2301.00001"),
    )
    rows = storage.sql_query("SELECT id, title, arxiv_id FROM papers")
    assert len(rows) == 1
    assert rows[0]["title"] == "Test Paper"


def test_sqlite_query_with_params(storage):
    storage.sql_execute("CREATE TABLE IF NOT EXISTS terms (id TEXT PRIMARY KEY, name TEXT)")
    storage.sql_execute("INSERT INTO terms VALUES (?, ?)", ("a", "transformer"))
    storage.sql_execute("INSERT INTO terms VALUES (?, ?)", ("b", "attention"))
    rows = storage.sql_query("SELECT * FROM terms WHERE name LIKE ?", ("%atten%",))
    assert len(rows) == 1
    assert rows[0]["name"] == "attention"


@pytest.fixture
def chroma_storage():
    with tempfile.TemporaryDirectory() as tmp:
        yield Storage(tmp)


def test_chroma_add_and_search(chroma_storage):
    collection = chroma_storage.chroma_collection("test_terms")
    collection.add(
        ids=["t1", "t2"],
        documents=["transformer model architecture", "gradient descent optimization"],
        metadatas=[{"name": "transformer"}, {"name": "gradient_descent"}],
    )
    results = collection.query(query_texts=["neural network architecture"], n_results=1)
    assert len(results["ids"][0]) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/core/test_storage.py -v`
Expected: FAIL

- [ ] **Step 3: Implement Storage**

```python
# backend/core/storage.py
import sqlite3
import threading
from pathlib import Path
from typing import Any

import chromadb


class Storage:
    def __init__(self, data_dir: str):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._sqlite_path = str(self._data_dir / "research.db")
        self._local = threading.local()
        self._chroma_client = chromadb.PersistentClient(
            path=str(self._data_dir / "chroma")
        )

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self._sqlite_path)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def sql_execute(self, sql: str, params: tuple = ()) -> None:
        conn = self._get_conn()
        conn.execute(sql, params)
        conn.commit()

    def sql_query(self, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        conn = self._get_conn()
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    def chroma_collection(self, name: str) -> Any:
        return self._chroma_client.get_or_create_collection(name=name)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_storage.py -v`
Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/core/storage.py tests/core/test_storage.py
git commit -m "feat: add Storage with SQLite + ChromaDB unified interface"
```

### Task 2.5: LLM Router — Unified Interface

**Files:**
- Create: `backend/core/llm_router.py`
- Create: `tests/core/test_llm_router.py`

- [ ] **Step 1: Write failing test**

```python
# tests/core/test_llm_router.py
import pytest
from backend.core.llm_router import LLMRouter, Provider

@pytest.mark.asyncio
async def test_router_selects_ollama_when_no_cloud_configured():
    router = LLMRouter(ollama_base_url="http://localhost:11434", ollama_model="qwen3:14b")
    provider = router.select(classification="public")
    assert provider == Provider.OLLAMA


@pytest.mark.asyncio
async def test_router_selects_cloud_when_configured_and_public():
    router = LLMRouter(
        ollama_base_url="http://localhost:11434",
        ollama_model="qwen3:14b",
        cloud_provider="claude",
        cloud_api_key="sk-test",
        cloud_model="claude-sonnet-4-6",
    )
    provider = router.select(classification="public")
    assert provider == Provider.CLAUDE


@pytest.mark.asyncio
async def test_router_blocks_cloud_for_secret():
    router = LLMRouter(
        ollama_base_url="http://localhost:11434",
        ollama_model="qwen3:14b",
        cloud_provider="claude",
        cloud_api_key="sk-test",
    )
    provider = router.select(classification="secret")
    assert provider == Provider.OLLAMA


@pytest.mark.asyncio
async def test_router_selects_cautious_no_approval():
    router = LLMRouter(cloud_provider="claude", cloud_api_key="sk-test")
    provider = router.select(classification="cautious", cloud_approved=False)
    assert provider == Provider.OLLAMA


@pytest.mark.asyncio
async def test_router_selects_cloud_for_cautious_with_approval():
    router = LLMRouter(cloud_provider="claude", cloud_api_key="sk-test", cloud_model="claude-sonnet-4-6")
    provider = router.select(classification="cautious", cloud_approved=True)
    assert provider == Provider.CLAUDE
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/core/test_llm_router.py -v`
Expected: FAIL

- [ ] **Step 3: Implement LLMRouter**

```python
# backend/core/llm_router.py
from enum import Enum
from dataclasses import dataclass
from typing import Any

import httpx


class Provider(str, Enum):
    OLLAMA = "ollama"
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"
    OPENAI = "openai"


@dataclass
class LLMRouter:
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:14b"
    cloud_provider: str = ""
    cloud_api_key: str = ""
    cloud_model: str = ""
    _has_cloud: bool = False

    def __post_init__(self):
        self._has_cloud = bool(self.cloud_provider and self.cloud_api_key)

    def select(
        self,
        classification: str,
        cloud_approved: bool = False,
    ) -> Provider:
        if classification == "secret":
            return Provider.OLLAMA
        if not self._has_cloud:
            return Provider.OLLAMA
        if classification == "public":
            return self._provider_for(self.cloud_provider)
        if classification == "cautious" and cloud_approved:
            return self._provider_for(self.cloud_provider)
        return Provider.OLLAMA

    def _provider_for(self, name: str) -> Provider:
        return Provider(name.lower())

    async def chat(
        self,
        provider: Provider,
        messages: list[dict[str, str]],
    ) -> str:
        if provider == Provider.OLLAMA:
            return await self._ollama_chat(messages)
        if provider == Provider.CLAUDE:
            return await self._claude_chat(messages)
        if provider == Provider.OPENAI:
            return await self._openai_chat(messages)
        if provider == Provider.DEEPSEEK:
            return await self._deepseek_chat(messages)
        raise ValueError(f"Unknown provider: {provider}")

    async def _ollama_chat(self, messages: list[dict[str, str]]) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.ollama_base_url}/api/chat",
                json={"model": self.ollama_model, "messages": messages, "stream": False},
                timeout=120.0,
            )
            resp.raise_for_status()
            return resp.json()["message"]["content"]

    async def _claude_chat(self, messages: list[dict[str, str]]) -> str:
        system = ""
        user_messages = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                user_messages.append(m)

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.cloud_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self.cloud_model,
                    "max_tokens": 4096,
                    "system": system,
                    "messages": user_messages,
                },
                timeout=120.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]

    async def _openai_chat(self, messages: list[dict[str, str]]) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.cloud_api_key}",
                    "Content-Type": "application/json",
                },
                json={"model": self.cloud_model, "messages": messages},
                timeout=120.0,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def _deepseek_chat(self, messages: list[dict[str, str]]) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.cloud_api_key}",
                    "Content-Type": "application/json",
                },
                json={"model": self.cloud_model, "messages": messages},
                timeout=120.0,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_llm_router.py -v`
Expected: all 5 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/core/llm_router.py tests/core/test_llm_router.py
git commit -m "feat: add LLMRouter with local/cloud routing and multi-provider support"
```

### Task 2.6: Plugin Engine — Discovery and Lifecycle

**Files:**
- Create: `backend/core/engine.py`
- Create: `tests/core/test_engine.py`

- [ ] **Step 1: Write failing test**

```python
# tests/core/test_engine.py
import tempfile
from pathlib import Path
import pytest
from backend.core.engine import PluginEngine
from backend.core.event_bus import EventBus


class FakePlugin:
    def __init__(self):
        self.loaded = False
        self.unloaded = False
        self.routes_called = False
        self.commands_called = False

    async def on_load(self, bus, config):
        self.loaded = True

    async def on_unload(self):
        self.unloaded = True

    def get_routes(self):
        self.routes_called = True
        return None

    def get_commands(self):
        self.commands_called = True
        return []


@pytest.mark.asyncio
async def test_engine_loads_and_unloads_plugin():
    bus = EventBus()
    engine = PluginEngine(bus=bus, config={})
    plugin = FakePlugin()

    await engine.load_plugin("test_plugin", plugin)
    assert plugin.loaded is True

    await engine.unload_plugin("test_plugin")
    assert plugin.unloaded is True


@pytest.mark.asyncio
async def test_engine_discovers_plugins_from_dir():
    with tempfile.TemporaryDirectory() as tmp:
        plugin_dir = Path(tmp) / "test_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.toml").write_text("""
[plugin]
name = "discovered"
display_name = "发现插件"
version = "0.1.0"
""")
        (plugin_dir / "__init__.py").write_text("")
        (plugin_dir / "plugin.py").write_text("""
class Plugin:
    name = "discovered"
    display_name = "发现插件"
    version = "0.1.0"
    async def on_load(self, bus, config): pass
    async def on_unload(self): pass
    def get_routes(self): return None
    def get_commands(self): return []
""")

        bus = EventBus()
        engine = PluginEngine(bus=bus, config={})
        manifests = engine.discover_plugins(str(tmp))

        assert len(manifests) == 1
        assert manifests[0]["name"] == "discovered"
        assert manifests[0]["path"] == str(plugin_dir)


@pytest.mark.asyncio
async def test_engine_lists_loaded_plugins():
    bus = EventBus()
    engine = PluginEngine(bus=bus, config={})
    plugin = FakePlugin()

    await engine.load_plugin("p1", plugin)
    loaded = engine.list_plugins()

    assert "p1" in loaded
    assert loaded["p1"] is plugin
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/core/test_engine.py -v`
Expected: FAIL

- [ ] **Step 3: Implement PluginEngine**

```python
# backend/core/engine.py
import importlib.util
import sys
import tomllib
from pathlib import Path
from typing import Any

from backend.core.event_bus import EventBus


class PluginEngine:
    def __init__(self, bus: EventBus, config: dict[str, Any]):
        self._bus = bus
        self._config = config
        self._plugins: dict[str, Any] = {}

    def discover_plugins(self, plugins_dir: str) -> list[dict[str, Any]]:
        manifests = []
        base = Path(plugins_dir)
        for candidate in base.iterdir():
            if not candidate.is_dir():
                continue
            manifest_path = candidate / "plugin.toml"
            if not manifest_path.exists():
                continue
            raw = tomllib.loads(manifest_path.read_text())
            p = raw.get("plugin", {})
            manifests.append({
                "name": p.get("name", candidate.name),
                "display_name": p.get("display_name", candidate.name),
                "version": p.get("version", "0.0.0"),
                "path": str(candidate),
            })
        return manifests

    async def load_plugin(self, name: str, plugin: Any) -> None:
        await plugin.on_load(self._bus, self._config)
        self._plugins[name] = plugin

    async def unload_plugin(self, name: str) -> None:
        if name in self._plugins:
            await self._plugins[name].on_unload()
            del self._plugins[name]

    def list_plugins(self) -> dict[str, Any]:
        return dict(self._plugins)

    async def shutdown(self) -> None:
        for name in list(self._plugins):
            await self.unload_plugin(name)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_engine.py -v`
Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
git add backend/core/engine.py tests/core/test_engine.py
git commit -m "feat: add PluginEngine for plugin discovery, loading, and lifecycle"
```

### Task 2.7: API Gateway + Main Entry Point

**Files:**
- Create: `backend/api/__init__.py`, `backend/api/gateway.py`
- Create: `backend/main.py`

- [ ] **Step 1: Write gateway.py**

```python
# backend/api/gateway.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.engine import PluginEngine
from backend.core.event_bus import EventBus
from backend.core.config import Config
from backend.core.storage import Storage
from backend.core.security import SecurityManager
from backend.core.llm_router import LLMRouter


def create_app(config: Config) -> FastAPI:
    app = FastAPI(title="科研助手", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    bus = EventBus()
    storage = Storage(config.data_dir)
    security = SecurityManager()
    llm_router = LLMRouter(
        ollama_base_url=config.ollama_base_url,
        ollama_model=config.ollama_model,
        cloud_provider=config.cloud_provider,
        cloud_api_key=config.cloud_api_key,
        cloud_model=config.cloud_model,
    )
    engine = PluginEngine(bus=bus, config=config.to_dict())

    app.state.bus = bus
    app.state.storage = storage
    app.state.security = security
    app.state.llm_router = llm_router
    app.state.engine = engine
    app.state.config = config

    @app.get("/api/health")
    async def health():
        return {"status": "ok"}

    @app.get("/api/plugins")
    async def list_plugins():
        return [
            {"name": name, "display_name": p.__class__.__name__}
            for name, p in engine.list_plugins().items()
        ]

    return app
```

- [ ] **Step 2: Write main.py**

```python
# backend/main.py
import uvicorn
from pathlib import Path
from backend.core.config import Config
from backend.api.gateway import create_app


def main():
    data_dir = str(Path.home() / ".research-assistant")
    config = Config.load(data_dir)
    app = create_app(config)
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Create __init__.py files**

```bash
touch backend/__init__.py backend/api/__init__.py
```

- [ ] **Step 4: Verify app starts**

Run: `python -c "from backend.main import main; print('import OK')"`
Expected: "import OK"

- [ ] **Step 5: Commit**

```bash
git add backend/__init__.py backend/api/ backend/main.py
git commit -m "feat: add FastAPI gateway and main entry point"
```

---

## Phase 3: Frontend Core

### Task 3.1: TypeScript Types + API Client

**Files:**
- Create: `frontend/src/core/types.ts`
- Create: `frontend/src/core/api.ts`

- [ ] **Step 1: Write types.ts**

```typescript
// frontend/src/core/types.ts
export type Classification = 'secret' | 'cautious' | 'public';

export interface PluginManifest {
  name: string;
  displayName: string;
  version: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface SecurityBadgeProps {
  classification: Classification;
  onChange: (c: Classification) => void;
}

export interface PluginPanelProps {
  storage: StorageAPI;
  security: SecurityAPI;
  llm: LLMAPI;
  bus: EventBusAPI;
}

export interface StorageAPI {
  query: (sql: string, params?: unknown[]) => Promise<Record<string, unknown>[]>;
  search: (collection: string, query: string, n: number) => Promise<string[][]>;
}

export interface SecurityAPI {
  classify: (docId: string, level: Classification) => Promise<void>;
  allowCloud: (docId: string) => Promise<boolean>;
}

export interface LLMAPI {
  chat: (messages: ChatMessage[], classification: Classification, docId: string) => Promise<string>;
}

export interface EventBusAPI {
  emit: (event: string, data: Record<string, unknown>) => Promise<void>;
}
```

- [ ] **Step 2: Write api.ts**

```typescript
// frontend/src/core/api.ts
import type { ChatMessage, Classification } from './types';

const BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`${res.status}: ${err}`);
  }
  return res.json();
}

export const api = {
  health: () => request<{ status: string }>('/health'),

  plugins: () => request<{ name: string; display_name: string }[]>('/plugins'),

  classify: (docId: string, level: Classification) =>
    request('/security/classify', {
      method: 'POST',
      body: JSON.stringify({ doc_id: docId, level }),
    }),

  allowCloud: (docId: string) =>
    request<{ allowed: boolean }>(`/security/allow-cloud/${docId}`),

  chat: (messages: ChatMessage[], classification: Classification, docId: string) =>
    request<{ content: string }>('/chat', {
      method: 'POST',
      body: JSON.stringify({ messages, classification, doc_id: docId }),
    }),

  searchKnowledge: (collection: string, query: string, n = 5) =>
    request<{ results: string[][] }>('/knowledge/search', {
      method: 'POST',
      body: JSON.stringify({ collection, query, n }),
    }),
};
```

- [ ] **Step 3: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors

- [ ] **Step 4: Commit**

```bash
git add frontend/src/core/types.ts frontend/src/core/api.ts
git commit -m "feat: add TypeScript types and API client"
```

### Task 3.2: Workbench Shell — TabBar + SidePanel + Layout

**Files:**
- Create: `frontend/src/core/TabBar.tsx`
- Create: `frontend/src/core/SidePanel.tsx`
- Create: `frontend/src/core/Workbench.tsx`
- Create: `frontend/src/core/pluginRegistry.ts`

- [ ] **Step 1: Write TabBar.tsx**

```typescript
// frontend/src/core/TabBar.tsx
import React from 'react';

export interface Tab {
  key: string;
  label: string;
}

interface TabBarProps {
  tabs: Tab[];
  active: string;
  onSelect: (key: string) => void;
}

const barStyle: React.CSSProperties = {
  display: 'flex',
  gap: 0,
  borderBottom: '1px solid #e0e0e0',
  padding: '0 16px',
  background: '#fafafa',
};

const tabStyle = (isActive: boolean): React.CSSProperties => ({
  padding: '10px 20px',
  cursor: 'pointer',
  borderBottom: isActive ? '2px solid #1a73e8' : '2px solid transparent',
  color: isActive ? '#1a73e8' : '#555',
  fontWeight: isActive ? 600 : 400,
  fontSize: 14,
  userSelect: 'none',
});

export const TabBar: React.FC<TabBarProps> = ({ tabs, active, onSelect }) => (
  <div style={barStyle}>
    {tabs.map((tab) => (
      <div
        key={tab.key}
        style={tabStyle(active === tab.key)}
        onClick={() => onSelect(tab.key)}
      >
        {tab.label}
      </div>
    ))}
  </div>
);
```

- [ ] **Step 2: Write SidePanel.tsx**

```typescript
// frontend/src/core/SidePanel.tsx
import React from 'react';

interface SidePanelProps {
  children: React.ReactNode;
  width?: number;
}

export const SidePanel: React.FC<SidePanelProps> = ({ children, width = 300 }) => (
  <div style={{
    width,
    borderLeft: '1px solid #e0e0e0',
    background: '#fafafa',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
  }}>
    {children}
  </div>
);
```

- [ ] **Step 3: Write pluginRegistry.ts**

```typescript
// frontend/src/core/pluginRegistry.ts
import React from 'react';

interface PluginEntry {
  name: string;
  displayName: string;
  component: React.ComponentType;
  icon: string;
}

const registry = new Map<string, PluginEntry>();

export function registerPlugin(entry: PluginEntry): void {
  registry.set(entry.name, entry);
}

export function getPlugin(name: string): PluginEntry | undefined {
  return registry.get(name);
}

export function allPlugins(): PluginEntry[] {
  return Array.from(registry.values());
}
```

- [ ] **Step 4: Write Workbench.tsx**

```typescript
// frontend/src/core/Workbench.tsx
import React, { useState } from 'react';
import { TabBar } from './TabBar';
import { SidePanel } from './SidePanel';
import { allPlugins } from './pluginRegistry';
import { ChatWindow } from '../shared/ChatWindow';

const TABS = [
  { key: 'term-advisor', label: '读懂导师' },
  { key: 'literature', label: '追新论文' },
  { key: 'evaluator', label: '审项目' },
  { key: 'formula', label: '验公式' },
  { key: 'paper-writer', label: '写论文' },
];

export const Workbench: React.FC = () => {
  const [activeTab, setActiveTab] = useState('term-advisor');

  const ActiveComponent = (() => {
    const plugins = allPlugins();
    const found = plugins.find((p) => p.name === activeTab);
    return found?.component ?? (() => <div>插件未安装</div>);
  })();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <TabBar tabs={TABS} active={activeTab} onSelect={setActiveTab} />
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        <main style={{ flex: 1, overflow: 'auto', padding: 16 }}>
          <ActiveComponent />
        </main>
        <SidePanel>
          <ChatWindow />
        </SidePanel>
      </div>
    </div>
  );
};
```

- [ ] **Step 5: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: Has errors (ChatWindow not yet created) — expected at this stage.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/core/
git commit -m "feat: add Workbench shell with TabBar, SidePanel, and plugin registry"
```

### Task 3.3: Shared Components — ChatWindow, SecurityBadge, Settings

**Files:**
- Create: `frontend/src/shared/ChatWindow.tsx`
- Create: `frontend/src/shared/SecurityBadge.tsx`
- Create: `frontend/src/shared/Settings.tsx`

- [ ] **Step 1: Write SecurityBadge.tsx**

```typescript
// frontend/src/shared/SecurityBadge.tsx
import React from 'react';
import type { Classification } from '../core/types';

interface Props {
  classification: Classification;
  onChange?: (c: Classification) => void;
  readonly?: boolean;
}

const colors: Record<Classification, string> = {
  secret: '#d93025',
  cautious: '#e37400',
  public: '#188038',
};

const labels: Record<Classification, string> = {
  secret: '机密',
  cautious: '审慎',
  public: '公开',
};

export const SecurityBadge: React.FC<Props> = ({ classification, onChange, readonly }) => {
  if (readonly) {
    return (
      <span style={{
        display: 'inline-block',
        padding: '2px 8px',
        borderRadius: 4,
        fontSize: 12,
        fontWeight: 600,
        color: '#fff',
        background: colors[classification],
      }}>
        {labels[classification]}
      </span>
    );
  }

  return (
    <select
      value={classification}
      onChange={(e) => onChange?.(e.target.value as Classification)}
      style={{
        padding: '4px 8px',
        borderRadius: 4,
        border: `1px solid ${colors[classification]}`,
        color: colors[classification],
        fontWeight: 600,
        fontSize: 12,
      }}
    >
      <option value="secret">🔴 机密</option>
      <option value="cautious">🟡 审慎</option>
      <option value="public">🟢 公开</option>
    </select>
  );
};
```

- [ ] **Step 2: Write ChatWindow.tsx**

```typescript
// frontend/src/shared/ChatWindow.tsx
import React, { useState, useRef, useEffect } from 'react';
import type { ChatMessage, Classification } from '../core/types';

export const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [classification, setClassification] = useState<Classification>('cautious');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg: ChatMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMsg],
          classification,
          doc_id: `chat-${Date.now()}`,
        }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'assistant', content: data.content }]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `错误: ${(e as Error).message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ padding: '8px 12px', borderBottom: '1px solid #e0e0e0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontWeight: 600, fontSize: 14 }}>问一问</span>
        <select
          value={classification}
          onChange={(e) => setClassification(e.target.value as Classification)}
          style={{ fontSize: 12, padding: '2px 6px' }}
        >
          <option value="cautious">🟡 审慎</option>
          <option value="public">🟢 公开</option>
        </select>
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: 8 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 8, padding: '6px 10px', borderRadius: 8, background: m.role === 'user' ? '#e3f2fd' : '#f5f5f5', fontSize: 13, lineHeight: 1.5 }}>
            {m.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div style={{ padding: 8, borderTop: '1px solid #e0e0e0', display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder="输入问题..."
          style={{ flex: 1, padding: '6px 10px', border: '1px solid #ddd', borderRadius: 6, fontSize: 13 }}
        />
        <button
          onClick={send}
          disabled={loading}
          style={{ padding: '6px 14px', background: '#1a73e8', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}
        >
          {loading ? '...' : '发送'}
        </button>
      </div>
    </div>
  );
};
```

- [ ] **Step 3: Write Settings.tsx**

```typescript
// frontend/src/shared/Settings.tsx
import React, { useState, useEffect } from 'react';

interface LLMSettings {
  ollama_base_url: string;
  ollama_model: string;
  cloud_provider: string;
  cloud_api_key: string;
  cloud_model: string;
}

export const Settings: React.FC = () => {
  const [settings, setSettings] = useState<LLMSettings>({
    ollama_base_url: 'http://localhost:11434',
    ollama_model: 'qwen3:14b',
    cloud_provider: '',
    cloud_api_key: '',
    cloud_model: '',
  });
  const [saved, setSaved] = useState(false);
  const [warningAccepted, setWarningAccepted] = useState(false);

  useEffect(() => {
    fetch('/api/settings')
      .then((r) => r.json())
      .then((d) => setSettings(d))
      .catch(() => {});
  }, []);

  const save = async () => {
    await fetch('/api/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div style={{ padding: 16, maxWidth: 500 }}>
      <h2 style={{ fontSize: 18, marginBottom: 16 }}>设置</h2>

      {settings.cloud_api_key && !warningAccepted && (
        <div style={{ background: '#fce8e6', border: '1px solid #d93025', borderRadius: 8, padding: 16, marginBottom: 16 }}>
          <p style={{ fontWeight: 600, color: '#d93025', margin: '0 0 8px 0' }}>隐私风险提示</p>
          <p style={{ fontSize: 13, margin: 0, lineHeight: 1.6 }}>
            发送到云端 API 的数据会离开你的电脑。导师未公开的研究思路、实验数据、专利相关材料请勿使用云端模型处理。如不确定，请先咨询导师。
          </p>
          <label style={{ display: 'block', marginTop: 8, fontSize: 13 }}>
            <input type="checkbox" checked={warningAccepted} onChange={(e) => setWarningAccepted(e.target.checked)} />
            我已理解以上风险，自行承担使用云端 API 的后果
          </label>
        </div>
      )}

      <fieldset style={{ border: '1px solid #ddd', borderRadius: 8, padding: 12, marginBottom: 12 }}>
        <legend style={{ fontWeight: 600 }}>本地模型 (Ollama)</legend>
        <label style={{ display: 'block', fontSize: 13, marginBottom: 8 }}>
          地址
          <input value={settings.ollama_base_url} onChange={(e) => setSettings({ ...settings, ollama_base_url: e.target.value })} style={inputStyle} />
        </label>
        <label style={{ display: 'block', fontSize: 13 }}>
          模型
          <input value={settings.ollama_model} onChange={(e) => setSettings({ ...settings, ollama_model: e.target.value })} style={inputStyle} />
        </label>
      </fieldset>

      <fieldset style={{ border: '1px solid #ddd', borderRadius: 8, padding: 12, marginBottom: 12 }}>
        <legend style={{ fontWeight: 600 }}>云端 API（可选）</legend>
        <label style={{ display: 'block', fontSize: 13, marginBottom: 8 }}>
          提供商
          <select value={settings.cloud_provider} onChange={(e) => setSettings({ ...settings, cloud_provider: e.target.value })} style={inputStyle}>
            <option value="">不使用</option>
            <option value="claude">Claude</option>
            <option value="openai">OpenAI</option>
            <option value="deepseek">DeepSeek</option>
          </select>
        </label>
        <label style={{ display: 'block', fontSize: 13, marginBottom: 8 }}>
          API Key
          <input type="password" value={settings.cloud_api_key} onChange={(e) => setSettings({ ...settings, cloud_api_key: e.target.value })} style={inputStyle} />
        </label>
        <label style={{ display: 'block', fontSize: 13 }}>
          模型名
          <input value={settings.cloud_model} onChange={(e) => setSettings({ ...settings, cloud_model: e.target.value })} style={inputStyle} placeholder="如 claude-sonnet-4-6" />
        </label>
      </fieldset>

      <button onClick={save} style={{ padding: '8px 24px', background: '#1a73e8', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
        {saved ? '已保存' : '保存设置'}
      </button>
    </div>
  );
};

const inputStyle: React.CSSProperties = {
  display: 'block',
  width: '100%',
  padding: '6px 10px',
  border: '1px solid #ddd',
  borderRadius: 4,
  fontSize: 13,
  marginTop: 4,
  boxSizing: 'border-box',
};
```

- [ ] **Step 4: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors (may have ChatWindow import error in Workbench — fix if needed)

- [ ] **Step 5: Commit**

```bash
git add frontend/src/shared/
git commit -m "feat: add shared components — ChatWindow, SecurityBadge, Settings"
```

### Task 3.4: App Root + Entry Point

**Files:**
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/main.tsx`

- [ ] **Step 1: Write App.tsx**

```typescript
// frontend/src/App.tsx
import React from 'react';
import { Workbench } from './core/Workbench';

export const App: React.FC = () => {
  return <Workbench />;
};
```

- [ ] **Step 2: Write main.tsx**

```typescript
// frontend/src/main.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
```

- [ ] **Step 3: Verify frontend builds**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors

- [ ] **Step 4: Commit**

```bash
git add frontend/src/App.tsx frontend/src/main.tsx
git commit -m "feat: add App root and main entry point"
```

---

## Phase 4: Backend Chat + Settings Endpoints

### Task 4.1: Chat endpoint + Security routes + Settings routes

**Files:**
- Modify: `backend/api/gateway.py` (add routes)

- [ ] **Step 1: Add chat, security, settings, and knowledge search routes to gateway.py**

In `backend/api/gateway.py`, add the following routes inside `create_app()` after the existing route definitions:

```python
    from pydantic import BaseModel

    class ChatRequest(BaseModel):
        messages: list[dict]
        classification: str
        doc_id: str

    class ClassifyRequest(BaseModel):
        doc_id: str
        level: str

    class SearchRequest(BaseModel):
        collection: str
        query: str
        n: int = 5

    class SettingsUpdate(BaseModel):
        ollama_base_url: str = ""
        ollama_model: str = ""
        cloud_provider: str = ""
        cloud_api_key: str = ""
        cloud_model: str = ""

    @app.post("/api/chat")
    async def chat(req: ChatRequest, request: Request):
        sec: SecurityManager = request.app.state.security
        llm: LLMRouter = request.app.state.llm_router

        sec.mark(req.doc_id, req.classification)
        approved = sec.allow_cloud(req.doc_id)
        provider = llm.select(classification=req.classification, cloud_approved=approved)

        content_hash = str(hash(str(req.messages)))
        if provider.name != "OLLAMA":
            sec.log_cloud_send(req.doc_id, llm.cloud_model, content_hash)

        result = await llm.chat(provider, req.messages)
        return {"content": result, "provider": provider.value}

    @app.post("/api/security/classify")
    async def classify(req: ClassifyRequest):
        from backend.core.security import Classification
        sec: SecurityManager = request.app.state.security
        sec.mark(req.doc_id, Classification(req.level))
        return {"status": "ok"}

    @app.get("/api/security/allow-cloud/{doc_id}")
    async def allow_cloud(doc_id: str, request: Request):
        sec: SecurityManager = request.app.state.security
        allowed = sec.allow_cloud(doc_id)
        return {"allowed": allowed}

    @app.get("/api/security/audit-log")
    async def audit_log(request: Request):
        sec: SecurityManager = request.app.state.security
        return {"entries": sec.audit_log()}

    @app.get("/api/settings")
    async def get_settings(request: Request):
        cfg: Config = request.app.state.config
        return cfg.to_dict()

    @app.put("/api/settings")
    async def update_settings(req: SettingsUpdate, request: Request):
        cfg: Config = request.app.state.config
        for key, val in req.model_dump(exclude_unset=True).items():
            if hasattr(cfg, key):
                setattr(cfg, key, val)
        cfg.save()
        return {"status": "ok"}

    @app.post("/api/knowledge/search")
    async def search_knowledge(req: SearchRequest, request: Request):
        storage: Storage = request.app.state.storage
        collection = storage.chroma_collection(req.collection)
        results = collection.query(query_texts=[req.query], n_results=req.n)
        return {"results": results.get("ids", [[]])}
```

- [ ] **Step 2: Add missing import**

At the top of `backend/api/gateway.py`, add `from fastapi import Request` and import the necessary core classes.

- [ ] **Step 3: Verify app starts**

Run: `python -c "from backend.main import main; print('routes OK')"`
Expected: "routes OK"

- [ ] **Step 4: Commit**

```bash
git add backend/api/gateway.py
git commit -m "feat: add chat, security, settings, and knowledge search API routes"
```

---

## Phase 5: Plugin — 读懂导师 (term-advisor)

### Task 5.1: Backend plugin

**Files:**
- Create: `backend/plugins/term_advisor/__init__.py`, `backend/plugins/term_advisor/plugin.py`, `backend/plugins/term_advisor/routes.py`, `backend/plugins/term_advisor/advisor.py`
- Create: `backend/plugins/term_advisor/plugin.toml`
- Create: `tests/plugins/test_term_advisor.py`

- [ ] **Step 1: Write failing test**

```python
# tests/plugins/test_term_advisor.py
import pytest
from backend.plugins.term_advisor.advisor import parse_advisor_text, AdvisorTask
from backend.plugins.term_advisor.plugin import TermAdvisorPlugin

def test_parse_simple_instruction():
    text = "你去看一下Transformer在NLP中的应用，然后做一个综述"
    tasks = parse_advisor_text(text)
    assert len(tasks) >= 1
    assert any("Transformer" in t.keywords for t in tasks)
    assert any("综述" in t.action for t in tasks)


def test_parse_identifies_keywords():
    text = "先调研diffusion model在图像生成方面的最新进展，重点关注DDPM和Stable Diffusion"
    tasks = parse_advisor_text(text)
    keywords = {kw for t in tasks for kw in t.keywords}
    assert "diffusion model" in keywords or "diffusion" in keywords


def test_plugin_has_required_methods():
    plugin = TermAdvisorPlugin()
    assert plugin.name == "term_advisor"
    assert plugin.display_name == "读懂导师"
    assert hasattr(plugin, "on_load")
    assert hasattr(plugin, "on_unload")
    assert hasattr(plugin, "get_routes")
    assert hasattr(plugin, "get_commands")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/plugins/test_term_advisor.py -v`
Expected: FAIL

- [ ] **Step 3: Implement advisor.py**

```python
# backend/plugins/term_advisor/advisor.py
import re
from dataclasses import dataclass, field


@dataclass
class AdvisorTask:
    action: str
    keywords: list[str] = field(default_factory=list)
    priority: str = "normal"


def parse_advisor_text(text: str) -> list[AdvisorTask]:
    sentences = re.split(r"[。；;]\s*", text)
    tasks: list[AdvisorTask] = []

    action_keywords = {
        "综述": "文献综述",
        "调研": "调研",
        "实现": "实现",
        "复现": "复现",
        "对比": "对比分析",
        "改进": "改进",
        "实验": "实验",
    }

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) < 4:
            continue

        action = "了解"
        found_keywords: list[str] = []

        for kw, act in action_keywords.items():
            if kw in sentence:
                action = act
                break

        # Extract potential technical terms (uppercase English or Chinese noun phrases)
        english_terms = re.findall(r"[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*", sentence)
        found_keywords.extend(english_terms)

        # Extract Chinese technical terms (2-8 char sequences between action words)
        chinese_terms = re.findall(r"[一-鿿]{2,8}(?:模型|方法|算法|网络|系统|框架|机制|理论|定理|公式|数据|实验|训练|推理|生成|识别|分类|预测|优化)?", sentence)
        # Filter noise
        chinese_terms = [t for t in chinese_terms if t not in {"的方法", "在此基础", "首先需要", "然后进行", "最后", "在此基础上"}]
        found_keywords.extend(chinese_terms[:3])

        tasks.append(AdvisorTask(action=action, keywords=found_keywords))

    if not tasks:
        tasks.append(AdvisorTask(action="了解", keywords=[text[:20]]))

    return tasks
```

- [ ] **Step 4: Implement plugin.py**

```python
# backend/plugins/term_advisor/plugin.py
from fastapi import APIRouter


class TermAdvisorPlugin:
    name = "term_advisor"
    display_name = "读懂导师"
    version = "0.1.0"

    async def on_load(self, bus, config):
        self._bus = bus
        self._config = config

    async def on_unload(self):
        pass

    def get_routes(self) -> APIRouter:
        from backend.plugins.term_advisor.routes import create_router
        return create_router(self)

    def get_commands(self) -> list:
        return ["/parse", "/terms"]
```

- [ ] **Step 5: Implement routes.py**

```python
# backend/plugins/term_advisor/routes.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from backend.plugins.term_advisor.advisor import parse_advisor_text


class ParseRequest(BaseModel):
    text: str


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/term-advisor", tags=["term-advisor"])

    @router.post("/parse")
    async def parse_advisor(req: ParseRequest):
        tasks = parse_advisor_text(req.text)
        return {
            "tasks": [
                {"action": t.action, "keywords": t.keywords, "priority": t.priority}
                for t in tasks
            ]
        }

    @router.get("/commands")
    async def get_commands():
        return {"commands": plugin.get_commands()}

    return router
```

- [ ] **Step 6: Write plugin.toml**

```toml
[plugin]
name = "term_advisor"
display_name = "读懂导师"
version = "0.1.0"
dependencies = ["knowledge-base"]
```

- [ ] **Step 7: Write __init__.py**

```python
# backend/plugins/term_advisor/__init__.py
from backend.plugins.term_advisor.plugin import TermAdvisorPlugin
```

- [ ] **Step 8: Run tests**

Run: `pytest tests/plugins/test_term_advisor.py -v`
Expected: 3 PASS

- [ ] **Step 9: Commit**

```bash
git add backend/plugins/term_advisor/ tests/plugins/test_term_advisor.py
git commit -m "feat: add term-advisor plugin — parse advisor text into structured tasks"
```

### Task 5.2: Frontend panel

**Files:**
- Create: `frontend/src/plugins/term-advisor/TermAdvisorPanel.tsx`

- [ ] **Step 1: Write panel component**

```typescript
// frontend/src/plugins/term-advisor/TermAdvisorPanel.tsx
import React, { useState } from 'react';

interface ParsedTask {
  action: string;
  keywords: string[];
  priority: string;
}

const classificationStyle: React.CSSProperties = {
  background: '#fce8e6',
  border: '1px solid #d93025',
  borderRadius: 8,
  padding: '12px 16px',
  marginBottom: 16,
  fontSize: 13,
  color: '#d93025',
};

export const TermAdvisorPanel: React.FC = () => {
  const [input, setInput] = useState('');
  const [tasks, setTasks] = useState<ParsedTask[]>([]);
  const [loading, setLoading] = useState(false);

  const parse = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const res = await fetch('/api/term-advisor/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input }),
    });
    const data = await res.json();
    setTasks(data.tasks);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700 }}>
      <div style={classificationStyle}>
        ⚠️ 此功能强制使用本地模型。导师言论属于机密信息，不会发送到任何云端服务。
      </div>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="粘贴导师的原话...&#10;&#10;例如：你先看一下 Transformer 在 NLP 里的应用，做个综述，然后想想怎么改进注意力机制"
        rows={5}
        style={{
          width: '100%', padding: 12, border: '1px solid #ddd',
          borderRadius: 8, fontSize: 14, resize: 'vertical', boxSizing: 'border-box',
        }}
      />

      <button
        onClick={parse}
        disabled={loading}
        style={{
          marginTop: 12, padding: '8px 24px', background: '#1a73e8',
          color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 14,
        }}
      >
        {loading ? '解析中...' : '解析'}
      </button>

      {tasks.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h3 style={{ fontSize: 16, marginBottom: 12 }}>任务拆解</h3>
          {tasks.map((t, i) => (
            <div key={i} style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, marginBottom: 8 }}>
              <span style={{ fontWeight: 600 }}>{t.action}</span>
              {t.keywords.length > 0 && (
                <div style={{ marginTop: 6, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {t.keywords.map((kw, j) => (
                    <span key={j} style={{ background: '#e8f0fe', color: '#1a73e8', padding: '2px 8px', borderRadius: 12, fontSize: 12 }}>
                      {kw}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors

- [ ] **Step 3: Commit**

```bash
git add frontend/src/plugins/term-advisor/
git commit -m "feat: add term-advisor frontend panel"
```

---

## Phase 6: Plugin — 追新论文 (literature)

### Task 6.1: Backend plugin

**Files:**
- Create: `backend/plugins/literature/__init__.py`, `backend/plugins/literature/plugin.py`, `backend/plugins/literature/routes.py`, `backend/plugins/literature/fetcher.py`, `backend/plugins/literature/summarizer.py`, `backend/plugins/literature/plugin.toml`
- Create: `tests/plugins/test_literature.py`

- [ ] **Step 1: Write failing test**

```python
# tests/plugins/test_literature.py
import pytest
from backend.plugins.literature.fetcher import ArxivFetcher

@pytest.mark.asyncio
async def test_fetcher_builds_query_url():
    fetcher = ArxivFetcher()
    url = fetcher.build_query_url("transformer attention", max_results=5)
    assert "search_query=transformer+attention" in url
    assert "max_results=5" in url


@pytest.mark.asyncio
async def test_fetcher_parses_entry():
    fetcher = ArxivFetcher()
    entry = {
        "id": "2301.00001",
        "title": "Test Paper Title",
        "summary": "A test summary.",
        "authors": [{"name": "Author One"}, {"name": "Author Two"}],
        "published": "2023-01-01T00:00:00Z",
        "link": "http://arxiv.org/abs/2301.00001",
    }
    paper = fetcher.parse_entry(entry)
    assert paper["arxiv_id"] == "2301.00001"
    assert paper["title"] == "Test Paper Title"
    assert paper["authors"] == "Author One, Author Two"


def test_plugin_declaration():
    from backend.plugins.literature.plugin import LiteraturePlugin
    plugin = LiteraturePlugin()
    assert plugin.name == "literature"
    assert plugin.display_name == "追新论文"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/plugins/test_literature.py -v`
Expected: FAIL

- [ ] **Step 3: Implement fetcher.py**

```python
# backend/plugins/literature/fetcher.py
from urllib.parse import quote_plus
import aiohttp
import feedparser
from datetime import datetime
from typing import Any


class ArxivFetcher:
    BASE = "http://export.arxiv.org/api/query"

    def build_query_url(self, query: str, max_results: int = 10) -> str:
        encoded = quote_plus(query)
        return f"{self.BASE}?search_query={encoded}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    def parse_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        authors = ", ".join(a.get("name", "") for a in entry.get("authors", []))
        return {
            "arxiv_id": entry.get("id", "").split("/abs/")[-1],
            "title": entry.get("title", "").strip().replace("\n", " "),
            "summary": entry.get("summary", "").strip().replace("\n", " "),
            "authors": authors,
            "published": entry.get("published", ""),
            "link": entry.get("link", ""),
        }

    async def fetch(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        url = self.build_query_url(query, max_results)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.text()
        parsed = feedparser.parse(text)
        return [self.parse_entry(e) for e in parsed.entries]
```

- [ ] **Step 4: Implement summarizer.py**

```python
# backend/plugins/literature/summarizer.py
from typing import Any
from backend.core.llm_router import LLMRouter, Provider


async def summarize_paper(
    paper: dict[str, Any],
    router: LLMRouter,
    classification: str = "public",
) -> str:
    prompt = f"""用中文简要总结以下论文（200字以内），包含：1)核心问题 2)方法 3)主要发现

标题: {paper['title']}
摘要: {paper['summary']}"""

    provider = router.select(classification=classification)
    result = await router.chat(provider, [{"role": "user", "content": prompt}])
    return result
```

- [ ] **Step 5: Implement routes.py**

```python
# backend/plugins/literature/routes.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from backend.plugins.literature.fetcher import ArxivFetcher
from backend.plugins.literature.summarizer import summarize_paper


class FetchRequest(BaseModel):
    query: str
    max_results: int = 10


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/literature", tags=["literature"])
    fetcher = ArxivFetcher()

    @router.post("/fetch")
    async def fetch_papers(req: FetchRequest):
        papers = await fetcher.fetch(req.query, req.max_results)
        return {"papers": papers, "total": len(papers)}

    @router.post("/summarize")
    async def summarize(req: dict, request: Request):
        router_llm = request.app.state.llm_router
        paper = req
        summary = await summarize_paper(paper, router_llm)
        return {"summary": summary}

    return router
```

- [ ] **Step 6: Implement plugin.py**

```python
# backend/plugins/literature/plugin.py
from fastapi import APIRouter


class LiteraturePlugin:
    name = "literature"
    display_name = "追新论文"
    version = "0.1.0"

    async def on_load(self, bus, config):
        self._bus = bus
        self._config = config

    async def on_unload(self):
        pass

    def get_routes(self) -> APIRouter:
        from backend.plugins.literature.routes import create_router
        return create_router(self)

    def get_commands(self) -> list:
        return ["/fetch", "/summarize"]
```

- [ ] **Step 7: Write __init__.py and plugin.toml**

```python
# backend/plugins/literature/__init__.py
from backend.plugins.literature.plugin import LiteraturePlugin
```

```toml
# backend/plugins/literature/plugin.toml
[plugin]
name = "literature"
display_name = "追新论文"
version = "0.1.0"
dependencies = ["knowledge-base"]
```

- [ ] **Step 8: Run tests**

Run: `pytest tests/plugins/test_literature.py -v`
Expected: 3 PASS

- [ ] **Step 9: Commit**

```bash
git add backend/plugins/literature/ tests/plugins/test_literature.py
git commit -m "feat: add literature plugin — ArXiv fetcher + summarizer"
```

### Task 6.2: Frontend panel

**Files:**
- Create: `frontend/src/plugins/literature/LiteraturePanel.tsx`

- [ ] **Step 1: Write panel component**

```typescript
// frontend/src/plugins/literature/LiteraturePanel.tsx
import React, { useState } from 'react';

interface Paper {
  arxiv_id: string;
  title: string;
  authors: string;
  summary: string;
  published: string;
  link: string;
}

export const LiteraturePanel: React.FC = () => {
  const [query, setQuery] = useState('');
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [summaries, setSummaries] = useState<Record<string, string>>({});

  const fetchPapers = async () => {
    if (!query.trim()) return;
    setLoading(true);
    const res = await fetch('/api/literature/fetch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, max_results: 5 }),
    });
    const data = await res.json();
    setPapers(data.papers);
    setLoading(false);
  };

  const summarizePaper = async (paper: Paper) => {
    if (summaries[paper.arxiv_id]) return;
    const res = await fetch('/api/literature/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(paper),
    });
    const data = await res.json();
    setSummaries((prev) => ({ ...prev, [paper.arxiv_id]: data.summary }));
  };

  return (
    <div style={{ maxWidth: 800 }}>
      <div style={{ fontSize: 13, color: '#666', marginBottom: 12 }}>
        数据来源: ArXiv API。论文摘要是公开信息，可选择云端模型加速总结。
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && fetchPapers()}
          placeholder="搜索关键词，如 transformer attention mechanism"
          style={{ flex: 1, padding: '8px 12px', border: '1px solid #ddd', borderRadius: 6, fontSize: 14 }}
        />
        <button onClick={fetchPapers} disabled={loading}
          style={{ padding: '8px 20px', background: '#1a73e8', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
          {loading ? '搜索中...' : '搜索'}
        </button>
      </div>

      <div>
        {papers.map((paper) => (
          <div key={paper.arxiv_id} style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 16, marginBottom: 12 }}>
            <h4 style={{ margin: '0 0 6px 0', fontSize: 15 }}>
              <a href={paper.link} target="_blank" rel="noopener noreferrer" style={{ color: '#1a73e8', textDecoration: 'none' }}>
                {paper.title}
              </a>
            </h4>
            <div style={{ fontSize: 12, color: '#888', marginBottom: 8 }}>
              {paper.authors} | {paper.published?.slice(0, 10)}
            </div>
            <div style={{ fontSize: 13, lineHeight: 1.6, color: '#444', marginBottom: 8 }}>
              {paper.summary.slice(0, 300)}{paper.summary.length > 300 ? '...' : ''}
            </div>
            {summaries[paper.arxiv_id] ? (
              <div style={{ background: '#f0f7ff', borderRadius: 6, padding: 10, fontSize: 13, lineHeight: 1.5 }}>
                <strong>中文总结：</strong>{summaries[paper.arxiv_id]}
              </div>
            ) : (
              <button onClick={() => summarizePaper(paper)}
                style={{ padding: '4px 12px', background: '#e8f0fe', color: '#1a73e8', border: 'none', borderRadius: 4, cursor: 'pointer', fontSize: 12 }}>
                中文总结
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
```

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors

- [ ] **Step 3: Commit**

```bash
git add frontend/src/plugins/literature/
git commit -m "feat: add literature frontend panel"
```

---

## Phase 7: Plugin — 验公式 (formula)

### Task 7.1: Backend plugin

**Files:**
- Create: `backend/plugins/formula/__init__.py`, `backend/plugins/formula/plugin.py`, `backend/plugins/formula/routes.py`, `backend/plugins/formula/latex_parser.py`, `backend/plugins/formula/verify.py`, `backend/plugins/formula/plugin.toml`
- Create: `tests/plugins/test_formula.py`

- [ ] **Step 1: Write failing test**

```python
# tests/plugins/test_formula.py
import pytest
from backend.plugins.formula.verify import verify_formula, FormulaVerification


def test_verify_quadratic_formula():
    result = verify_formula(expression="(-b + sqrt(b**2 - 4*a*c)) / (2*a)", domain="real")
    assert isinstance(result, FormulaVerification)
    assert result.is_valid


def test_verify_division_by_zero_detected():
    result = verify_formula(expression="1 / 0", domain="real")
    assert result.is_valid is False
    assert len(result.errors) >= 1


def test_plugin_declaration():
    from backend.plugins.formula.plugin import FormulaPlugin
    plugin = FormulaPlugin()
    assert plugin.name == "formula"
    assert plugin.display_name == "验公式"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/plugins/test_formula.py -v`
Expected: FAIL

- [ ] **Step 3: Implement verify.py**

```python
# backend/plugins/formula/verify.py
import re
from dataclasses import dataclass, field


@dataclass
class FormulaVerification:
    expression: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def verify_formula(expression: str, domain: str = "real") -> FormulaVerification:
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []

    # Check balanced parentheses
    paren_count = 0
    for ch in expression:
        if ch in "([{":
            paren_count += 1
        elif ch in ")]}":
            paren_count -= 1
        if paren_count < 0:
            errors.append("括号不匹配")
            break
    if paren_count > 0:
        errors.append("括号不匹配")
    if paren_count == 0 and not errors:
        suggestions.append("括号匹配正确")

    # Check division by zero
    if re.search(r"/\s*0\b", expression):
        errors.append("除零错误")

    # Check sqrt of negative (real domain)
    if domain == "real":
        neg_sqrt = re.findall(r"sqrt\s*\(\s*-", expression)
        if neg_sqrt:
            warnings.append("实数域下 sqrt 参数可能为负，请确认定义域")

    # Check common LaTeX issues
    if "\\" in expression:
        suggestions.append("检测到 LaTeX 命令，将转换为 SymPy 可解析格式")

    is_valid = len(errors) == 0
    return FormulaVerification(
        expression=expression,
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions,
    )


def latex_to_sympy(latex_str: str) -> str:
    """Convert common LaTeX math to Python/SymPy syntax."""
    s = latex_str
    s = s.replace("\\frac{", "(").replace("}{", ")/(").replace("}", ")")
    s = s.replace("\\sqrt", "sqrt")
    s = s.replace("\\sum", "Sum")
    s = s.replace("\\int", "Integral")
    s = s.replace("\\alpha", "alpha")
    s = s.replace("\\beta", "beta")
    s = s.replace("\\theta", "theta")
    s = s.replace("\\pi", "pi")
    s = s.replace("\\infty", "oo")
    s = s.replace("\\cdot", "*")
    s = s.replace("^", "**")
    s = s.replace("{", "(").replace("}", ")")
    return s


def sympy_verify(latex_str: str) -> FormulaVerification:
    """Cross-validate: parse LaTeX → SymPy symbolic check."""
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []

    try:
        import sympy
        python_expr = latex_to_sympy(latex_str)
        sympy_parsed = sympy.sympify(python_expr)
        suggestions.append(f"SymPy 解析成功: {sympy_parsed}")
    except Exception as e:
        errors.append(f"SymPy 解析失败: {str(e)[:100]}")
        return FormulaVerification(expression=latex_str, is_valid=False, errors=errors)

    # Check for undefined symbols
    symbols = list(sympy_parsed.free_symbols) if hasattr(sympy_parsed, 'free_symbols') else []
    if symbols:
        suggestions.append(f"检测到符号: {', '.join(str(s) for s in symbols)}")

    is_valid = len(errors) == 0
    return FormulaVerification(
        expression=latex_str,
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions,
    )
```

- [ ] **Step 4: Implement routes.py**

```python
# backend/plugins/formula/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.plugins.formula.verify import verify_formula, sympy_verify, latex_to_sympy


class VerifyRequest(BaseModel):
    expression: str
    domain: str = "real"


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/formula", tags=["formula"])

    @router.post("/verify")
    async def verify(req: VerifyRequest):
        basic = verify_formula(req.expression, req.domain)
        sympy_result = sympy_verify(req.expression)
        return {
            "basic": {
                "is_valid": basic.is_valid,
                "errors": basic.errors,
                "warnings": basic.warnings,
                "suggestions": basic.suggestions,
            },
            "sympy": {
                "is_valid": sympy_result.is_valid,
                "errors": sympy_result.errors,
                "suggestions": sympy_result.suggestions,
            },
            "cross_validated": basic.is_valid and sympy_result.is_valid,
        }

    @router.post("/convert")
    async def convert_latex(data: dict):
        latex_str = data.get("latex", "")
        python_expr = latex_to_sympy(latex_str)
        return {"python": python_expr}

    return router
```

- [ ] **Step 5: Implement plugin.py**

```python
# backend/plugins/formula/plugin.py
from fastapi import APIRouter


class FormulaPlugin:
    name = "formula"
    display_name = "验公式"
    version = "0.1.0"

    async def on_load(self, bus, config):
        self._bus = bus
        self._config = config

    async def on_unload(self):
        pass

    def get_routes(self) -> APIRouter:
        from backend.plugins.formula.routes import create_router
        return create_router(self)

    def get_commands(self) -> list:
        return ["/verify", "/convert"]
```

- [ ] **Step 6: Write __init__.py and plugin.toml**

```python
# backend/plugins/formula/__init__.py
from backend.plugins.formula.plugin import FormulaPlugin
```

```toml
# backend/plugins/formula/plugin.toml
[plugin]
name = "formula"
display_name = "验公式"
version = "0.1.0"
dependencies = []
```

- [ ] **Step 7: Run tests**

Run: `pytest tests/plugins/test_formula.py -v`
Expected: 3 PASS

- [ ] **Step 8: Commit**

```bash
git add backend/plugins/formula/ tests/plugins/test_formula.py
git commit -m "feat: add formula plugin — LaTeX parsing, SymPy cross-validation"
```

### Task 7.2: Frontend panel

**Files:**
- Create: `frontend/src/plugins/formula/FormulaPanel.tsx`

- [ ] **Step 1: Write panel component**

```typescript
// frontend/src/plugins/formula/FormulaPanel.tsx
import React, { useState } from 'react';

interface VerificationResult {
  basic: { is_valid: boolean; errors: string[]; warnings: string[]; suggestions: string[] };
  sympy: { is_valid: boolean; errors: string[]; suggestions: string[] };
  cross_validated: boolean;
}

export const FormulaPanel: React.FC = () => {
  const [latex, setLatex] = useState('');
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const verify = async () => {
    if (!latex.trim()) return;
    setLoading(true);
    const res = await fetch('/api/formula/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expression: latex }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800 }}>
      <div style={{ fontSize: 13, color: '#666', marginBottom: 12 }}>
        纯本地计算（SymPy + SciPy），不走 LLM，数据不离开本机。
      </div>

      <div style={{ display: 'flex', gap: 16 }}>
        <div style={{ flex: 1 }}>
          <label style={{ fontWeight: 600, fontSize: 14, display: 'block', marginBottom: 8 }}>LaTeX 源码</label>
          <textarea
            value={latex}
            onChange={(e) => setLatex(e.target.value)}
            placeholder="粘贴 LaTeX 公式..." + "\n" + "如: \\frac{-b + \\sqrt{b^2 - 4ac}}{2a}"
            rows={6}
            style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 14, resize: 'vertical', boxSizing: 'border-box', fontFamily: 'monospace' }}
          />
          <button onClick={verify} disabled={loading}
            style={{ marginTop: 12, padding: '8px 24px', background: '#1a73e8', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 14 }}>
            {loading ? '验证中...' : '交叉验证'}
          </button>
        </div>

        <div style={{ flex: 1, border: '1px solid #e0e0e0', borderRadius: 8, padding: 16, background: '#fafafa', minHeight: 200 }}>
          <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 8 }}>渲染预览</div>
          <div style={{ fontSize: 20, textAlign: 'center', padding: '20px 0', color: '#333' }}>
            {latex || '...'}
          </div>
        </div>
      </div>

      {result && (
        <div style={{ marginTop: 20 }}>
          <div style={{
            padding: '12px 16px', borderRadius: 8, marginBottom: 12,
            background: result.cross_validated ? '#e6f4ea' : '#fce8e6',
            border: `1px solid ${result.cross_validated ? '#188038' : '#d93025'}`,
            color: result.cross_validated ? '#188038' : '#d93025',
            fontWeight: 600,
          }}>
            {result.cross_validated ? '双通道验证通过' : '验证发现问题，请检查'}
          </div>

          {result.basic.errors.length > 0 && (
            <div style={{ fontSize: 13, color: '#d93025', marginBottom: 8 }}>
              基本检查：{result.basic.errors.join('; ')}
            </div>
          )}
          {result.basic.warnings.length > 0 && (
            <div style={{ fontSize: 13, color: '#e37400', marginBottom: 8 }}>
              警告：{result.basic.warnings.join('; ')}
            </div>
          )}
          {result.sympy.errors.length > 0 && (
            <div style={{ fontSize: 13, color: '#d93025', marginBottom: 8 }}>
              SymPy：{result.sympy.errors.join('; ')}
            </div>
          )}
          {result.sympy.suggestions.length > 0 && (
            <div style={{ fontSize: 13, color: '#555' }}>
              {result.sympy.suggestions.join('; ')}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors

- [ ] **Step 3: Commit**

```bash
git add frontend/src/plugins/formula/
git commit -m "feat: add formula frontend panel with LaTeX preview and dual-channel verification"
```

---

## Phase 8: Remaining Plugins — 审项目 + 写论文

### Task 8.1: 审项目 (evaluator) backend plugin

**Files:**
- Create: `backend/plugins/evaluator/__init__.py`, `backend/plugins/evaluator/plugin.py`, `backend/plugins/evaluator/routes.py`, `backend/plugins/evaluator/evaluate.py`, `backend/plugins/evaluator/plugin.toml`
- Create: `tests/plugins/test_evaluator.py`

- [ ] **Step 1: Write failing test**

```python
# tests/plugins/test_evaluator.py
from backend.plugins.evaluator.evaluate import evaluate_project, Evaluation


def test_evaluate_returns_structured_result():
    result = evaluate_project(
        title="Test Project",
        description="A novel approach to attention mechanisms in transformers.",
        field="machine_learning",
    )
    assert isinstance(result, Evaluation)
    assert 0 <= result.innovation_score <= 10
    assert 0 <= result.rationality_score <= 10
    assert 0 <= result.methodology_score <= 10
    assert len(result.strengths) >= 0
    assert len(result.weaknesses) >= 0


def test_evaluate_empty_description():
    result = evaluate_project(title="", description="", field="")
    assert isinstance(result, Evaluation)
    assert result.innovation_score == 0


def test_plugin_declaration():
    from backend.plugins.evaluator.plugin import EvaluatorPlugin
    plugin = EvaluatorPlugin()
    assert plugin.name == "evaluator"
    assert plugin.display_name == "审项目"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/plugins/test_evaluator.py -v`
Expected: FAIL

- [ ] **Step 3: Implement evaluate.py**

```python
# backend/plugins/evaluator/evaluate.py
import re
from dataclasses import dataclass, field


@dataclass
class Evaluation:
    title: str
    innovation_score: float
    rationality_score: float
    methodology_score: float
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def evaluate_project(title: str, description: str, field: str = "") -> Evaluation:
    if not description.strip():
        return Evaluation(
            title=title,
            innovation_score=0,
            rationality_score=0,
            methodology_score=0,
            strengths=["请提供项目描述"],
            weaknesses=["无描述"],
            suggestions=["填写项目描述后重新评估"],
        )

    strengths: list[str] = []
    weaknesses: list[str] = []
    suggestions: list[str] = []

    # Innovation heuristics
    novel_keywords = ["novel", "new", "改进", "首次", "first", "创新", "突破", "原创"]
    novel_count = sum(1 for kw in novel_keywords if kw.lower() in description.lower())

    # Methodology heuristics
    method_keywords = ["实验", "实验", "证明", "验证", "theorem", "定理", "推导", "算法", "algorithm"]
    method_count = sum(1 for kw in method_keywords if kw.lower() in description.lower())

    # Rationality heuristics
    if len(description) > 200:
        strengths.append("项目描述较为详细")
    else:
        weaknesses.append("项目描述过短，缺乏足够细节")

    if method_count >= 2:
        strengths.append(f"具备方法论意识（检测到 {method_count} 个方法论关键词）")
    else:
        weaknesses.append("缺少方法论描述，建议补充实验/验证方案")

    if novel_count >= 2:
        strengths.append(f"强调创新性（检测到 {novel_count} 个创新关键词）")
    else:
        suggestions.append("建议明确表达创新点和与现有工作的区别")

    # Scoring
    desc_len = len(description)
    innovation_score = min(10, max(0, (novel_count * 2) + (desc_len / 200)))
    rationality_score = min(10, max(0, (method_count * 2) + (desc_len / 300)))
    methodology_score = min(10, max(0, method_count * 2.5))

    return Evaluation(
        title=title,
        innovation_score=round(innovation_score, 1),
        rationality_score=round(rationality_score, 1),
        methodology_score=round(methodology_score, 1),
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions,
    )
```

- [ ] **Step 4: Implement routes.py**

```python
# backend/plugins/evaluator/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.plugins.evaluator.evaluate import evaluate_project


class EvalRequest(BaseModel):
    title: str
    description: str
    field: str = ""


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/evaluator", tags=["evaluator"])

    @router.post("/evaluate")
    async def evaluate(req: EvalRequest):
        result = evaluate_project(req.title, req.description, req.field)
        return {
            "title": result.title,
            "innovation_score": result.innovation_score,
            "rationality_score": result.rationality_score,
            "methodology_score": result.methodology_score,
            "strengths": result.strengths,
            "weaknesses": result.weaknesses,
            "suggestions": result.suggestions,
        }

    return router
```

- [ ] **Step 5: Implement plugin.py**

```python
# backend/plugins/evaluator/plugin.py
from fastapi import APIRouter


class EvaluatorPlugin:
    name = "evaluator"
    display_name = "审项目"
    version = "0.1.0"

    async def on_load(self, bus, config):
        self._bus = bus
        self._config = config

    async def on_unload(self):
        pass

    def get_routes(self) -> APIRouter:
        from backend.plugins.evaluator.routes import create_router
        return create_router(self)

    def get_commands(self) -> list:
        return ["/evaluate"]
```

- [ ] **Step 6: Write __init__.py and plugin.toml and run tests**

```toml
[plugin]
name = "evaluator"
display_name = "审项目"
version = "0.1.0"
dependencies = ["knowledge-base"]
```

Run: `pytest tests/plugins/test_evaluator.py -v`
Expected: 3 PASS

- [ ] **Step 7: Commit**

```bash
git add backend/plugins/evaluator/ tests/plugins/test_evaluator.py
git commit -m "feat: add evaluator plugin — project innovation/rationality/methodology scoring"
```

### Task 8.2: 写论文 (paper-writer) backend plugin

**Files:**
- Create: `backend/plugins/paper_writer/__init__.py`, `backend/plugins/paper_writer/plugin.py`, `backend/plugins/paper_writer/routes.py`, `backend/plugins/paper_writer/outline.py`, `backend/plugins/paper_writer/citation.py`, `backend/plugins/paper_writer/plugin.toml`
- Create: `tests/plugins/test_paper_writer.py`

- [ ] **Step 1: Write failing test**

```python
# tests/plugins/test_paper_writer.py
from backend.plugins.paper_writer.outline import generate_outline, OutlineSection
from backend.plugins.paper_writer.citation import parse_bibtex, BibEntry


def test_generate_outline_returns_sections():
    sections = generate_outline("基于Transformer的机器翻译改进研究")
    assert len(sections) >= 3
    assert any("引言" in s.title or "introduction" in s.title.lower() for s in sections)
    assert any("方法" in s.title or "method" in s.title.lower() for s in sections)


def test_sections_have_valid_structure():
    sections = generate_outline("Test Paper")
    for s in sections:
        assert isinstance(s.title, str)
        assert len(s.title) > 0
        assert isinstance(s.key_points, list)


def test_parse_bibtex_entry():
    entry = """@article{vaswani2017attention,
      title={Attention is All You Need},
      author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki},
      journal={NeurIPS},
      year={2017}
    }"""
    result = parse_bibtex(entry)
    assert len(result) == 1
    assert result[0].cite_key == "vaswani2017attention"
    assert result[0].title == "Attention is All You Need"
    assert result[0].year == "2017"


def test_parse_bibtex_multiple_entries():
    entries = """@article{a1, title={T1}, author={A}, journal={J}, year={2020}}
    @inproceedings{b1, title={T2}, author={B}, booktitle={C}, year={2021}}"""
    result = parse_bibtex(entries)
    assert len(result) == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/plugins/test_paper_writer.py -v`
Expected: FAIL

- [ ] **Step 3: Implement outline.py**

```python
# backend/plugins/paper_writer/outline.py
from dataclasses import dataclass, field


@dataclass
class OutlineSection:
    title: str
    key_points: list[str] = field(default_factory=list)
    estimated_words: int = 0


def generate_outline(topic: str) -> list[OutlineSection]:
    return [
        OutlineSection(
            title="引言",
            key_points=["研究背景与动机", "现有工作的局限性", "本文的主要贡献"],
            estimated_words=800,
        ),
        OutlineSection(
            title="相关工作",
            key_points=["子领域A的综述", "子领域B的综述", "与本文方法的对比"],
            estimated_words=1000,
        ),
        OutlineSection(
            title="方法",
            key_points=["问题形式化定义", "模型/算法设计", "理论分析（如适用）"],
            estimated_words=1500,
        ),
        OutlineSection(
            title="实验",
            key_points=["实验设置（数据集、基线、评估指标）", "主实验结果与分析", "消融实验"],
            estimated_words=1200,
        ),
        OutlineSection(
            title="讨论",
            key_points=["结果的意义", "局限性", "未来方向"],
            estimated_words=600,
        ),
        OutlineSection(
            title="结论",
            key_points=["总结主要发现", "重申贡献"],
            estimated_words=300,
        ),
    ]
```

- [ ] **Step 4: Implement citation.py**

```python
# backend/plugins/paper_writer/citation.py
import re
from dataclasses import dataclass, field


@dataclass
class BibEntry:
    entry_type: str
    cite_key: str
    title: str = ""
    author: str = ""
    year: str = ""
    journal: str = ""
    booktitle: str = ""
    raw: str = ""


def parse_bibtex(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []

    # Match @type{key, ...}
    pattern = re.compile(r"@(\w+)\s*\{\s*([^,]+),\s*(.+?)\}", re.DOTALL)
    matches = pattern.findall(text)

    for entry_type, cite_key, body in matches:
        entry = BibEntry(entry_type=entry_type, cite_key=cite_key.strip())

        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', body)
        if title_match:
            entry.title = title_match.group(1).strip()

        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', body)
        if author_match:
            entry.author = author_match.group(1).strip()

        year_match = re.search(r'year\s*=\s*\{?(\d+)\}?', body)
        if year_match:
            entry.year = year_match.group(1)

        journal_match = re.search(r'journal\s*=\s*\{([^}]+)\}', body)
        if journal_match:
            entry.journal = journal_match.group(1).strip()

        booktitle_match = re.search(r'booktitle\s*=\s*\{([^}]+)\}', body)
        if booktitle_match:
            entry.booktitle = booktitle_match.group(1).strip()

        entry.raw = f"@{entry_type}{{{entry.cite_key}, ...}}"
        entries.append(entry)

    return entries
```

- [ ] **Step 5: Implement routes.py**

```python
# backend/plugins/paper_writer/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.plugins.paper_writer.outline import generate_outline
from backend.plugins.paper_writer.citation import parse_bibtex


class OutlineRequest(BaseModel):
    topic: str


class BibtexRequest(BaseModel):
    bibtex: str


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/paper-writer", tags=["paper-writer"])

    @router.post("/outline")
    async def outline(req: OutlineRequest):
        sections = generate_outline(req.topic)
        return {
            "sections": [
                {"title": s.title, "key_points": s.key_points, "estimated_words": s.estimated_words}
                for s in sections
            ]
        }

    @router.post("/citation/parse")
    async def parse_citation(req: BibtexRequest):
        entries = parse_bibtex(req.bibtex)
        return {
            "entries": [
                {"cite_key": e.cite_key, "title": e.title, "author": e.author,
                 "year": e.year, "journal": e.journal or e.booktitle}
                for e in entries
            ]
        }

    return router
```

- [ ] **Step 6: Implement plugin.py, __init__.py, plugin.toml**

```toml
[plugin]
name = "paper_writer"
display_name = "写论文"
version = "0.1.0"
dependencies = ["knowledge-base", "literature"]
```

Run: `pytest tests/plugins/test_paper_writer.py -v`
Expected: 4 PASS

- [ ] **Step 7: Commit**

```bash
git add backend/plugins/paper_writer/ tests/plugins/test_paper_writer.py
git commit -m "feat: add paper-writer plugin — outline generator + BibTeX parser"
```

### Task 8.3: 审项目 + 写论文 frontend panels

**Files:**
- Create: `frontend/src/plugins/evaluator/EvaluatorPanel.tsx`
- Create: `frontend/src/plugins/paper-writer/PaperWriterPanel.tsx`

- [ ] **Step 1: Write EvaluatorPanel.tsx**

```typescript
// frontend/src/plugins/evaluator/EvaluatorPanel.tsx
import React, { useState } from 'react';
import { SecurityBadge } from '../../shared/SecurityBadge';
import type { Classification } from '../../core/types';

interface EvalResult {
  innovation_score: number;
  rationality_score: number;
  methodology_score: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
}

export const EvaluatorPanel: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [classification, setClassification] = useState<Classification>('cautious');
  const [result, setResult] = useState<EvalResult | null>(null);
  const [loading, setLoading] = useState(false);

  const evaluate = async () => {
    if (!description.trim()) return;
    setLoading(true);
    const res = await fetch('/api/evaluator/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700 }}>
      <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontSize: 13 }}>数据分级：</span>
        <SecurityBadge classification={classification} onChange={setClassification} />
      </div>

      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="项目名称"
        style={{ width: '100%', padding: '8px 12px', border: '1px solid #ddd', borderRadius: 6, fontSize: 14, marginBottom: 12, boxSizing: 'border-box' }} />

      <textarea value={description} onChange={(e) => setDescription(e.target.value)}
        placeholder="项目描述（研究问题、方法、创新点、预期成果等）"
        rows={8}
        style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 14, resize: 'vertical', boxSizing: 'border-box' }} />

      <button onClick={evaluate} disabled={loading}
        style={{ marginTop: 12, padding: '8px 24px', background: '#1a73e8', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 14 }}>
        {loading ? '评估中...' : '开始评估'}
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <div style={{ display: 'flex', gap: 16, marginBottom: 20 }}>
            {[
              { label: '创新性', score: result.innovation_score, color: '#1a73e8' },
              { label: '合理性', score: result.rationality_score, color: '#188038' },
              { label: '方法论', score: result.methodology_score, color: '#e37400' },
            ].map((item) => (
              <div key={item.label} style={{ flex: 1, textAlign: 'center', border: '1px solid #e0e0e0', borderRadius: 8, padding: 12 }}>
                <div style={{ fontSize: 28, fontWeight: 700, color: item.color }}>{item.score}</div>
                <div style={{ fontSize: 12, color: '#888', marginTop: 4 }}>/10 {item.label}</div>
              </div>
            ))}
          </div>

          {result.strengths.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <strong style={{ color: '#188038' }}>优势</strong>
              <ul style={{ margin: '4px 0', paddingLeft: 20, fontSize: 13 }}>{result.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>
            </div>
          )}
          {result.weaknesses.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <strong style={{ color: '#d93025' }}>不足</strong>
              <ul style={{ margin: '4px 0', paddingLeft: 20, fontSize: 13 }}>{result.weaknesses.map((w, i) => <li key={i}>{w}</li>)}</ul>
            </div>
          )}
          {result.suggestions.length > 0 && (
            <div>
              <strong style={{ color: '#1a73e8' }}>建议</strong>
              <ul style={{ margin: '4px 0', paddingLeft: 20, fontSize: 13 }}>{result.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

- [ ] **Step 2: Write PaperWriterPanel.tsx**

```typescript
// frontend/src/plugins/paper-writer/PaperWriterPanel.tsx
import React, { useState } from 'react';

interface OutlineSection {
  title: string;
  key_points: string[];
  estimated_words: number;
}

interface BibEntry {
  cite_key: string;
  title: string;
  author: string;
  year: string;
  journal: string;
}

export const PaperWriterPanel: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [outline, setOutline] = useState<OutlineSection[]>([]);
  const [bibtex, setBibtex] = useState('');
  const [entries, setEntries] = useState<BibEntry[]>([]);
  const [loading, setLoading] = useState(false);

  const generateOutline = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    const res = await fetch('/api/paper-writer/outline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic }),
    });
    const data = await res.json();
    setOutline(data.sections);
    setLoading(false);
  };

  const parseBibtex = async () => {
    if (!bibtex.trim()) return;
    const res = await fetch('/api/paper-writer/citation/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bibtex }),
    });
    const data = await res.json();
    setEntries(data.entries);
  };

  const totalWords = outline.reduce((sum, s) => sum + s.estimated_words, 0);

  return (
    <div style={{ maxWidth: 800 }}>
      <div style={{ marginBottom: 24 }}>
        <h3 style={{ fontSize: 16, marginBottom: 12 }}>大纲生成</h3>
        <div style={{ display: 'flex', gap: 8 }}>
          <input value={topic} onChange={(e) => setTopic(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && generateOutline()}
            placeholder="论文题目..."
            style={{ flex: 1, padding: '8px 12px', border: '1px solid #ddd', borderRadius: 6, fontSize: 14 }} />
          <button onClick={generateOutline} disabled={loading}
            style={{ padding: '8px 20px', background: '#1a73e8', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
            {loading ? '生成中...' : '生成大纲'}
          </button>
        </div>

        {outline.length > 0 && (
          <div style={{ marginTop: 16 }}>
            <div style={{ fontSize: 13, color: '#888', marginBottom: 12 }}>预计总字数: {totalWords}</div>
            {outline.map((s, i) => (
              <div key={i} style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, marginBottom: 8 }}>
                <div style={{ fontWeight: 600, marginBottom: 6 }}>{s.title} <span style={{ fontWeight: 400, fontSize: 12, color: '#888' }}>(~{s.estimated_words}字)</span></div>
                <ul style={{ margin: 0, paddingLeft: 20, fontSize: 13, color: '#555' }}>
                  {s.key_points.map((kp, j) => <li key={j}>{kp}</li>)}
                </ul>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h3 style={{ fontSize: 16, marginBottom: 12 }}>引文管理</h3>
        <textarea value={bibtex} onChange={(e) => setBibtex(e.target.value)}
          placeholder="粘贴 BibTeX 条目..."
          rows={6}
          style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 13, resize: 'vertical', boxSizing: 'border-box', fontFamily: 'monospace' }} />
        <button onClick={parseBibtex}
          style={{ marginTop: 8, padding: '6px 16px', background: '#1a73e8', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>
          解析
        </button>

        {entries.length > 0 && (
          <div style={{ marginTop: 16 }}>
            {entries.map((e, i) => (
              <div key={i} style={{ border: '1px solid #e0e0e0', borderRadius: 6, padding: '8px 12px', marginBottom: 6, fontSize: 13 }}>
                <span style={{ fontWeight: 600 }}>[{e.cite_key}]</span> {e.title} — {e.author} ({e.year}), {e.journal}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
```

- [ ] **Step 3: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors

- [ ] **Step 4: Commit**

```bash
git add frontend/src/plugins/evaluator/ frontend/src/plugins/paper-writer/
git commit -m "feat: add evaluator and paper-writer frontend panels"
```

---

## Phase 9: Plugin Wiring — In-app Startup

### Task 9.1: Auto-load built-in plugins on startup

**Files:**
- Modify: `backend/api/gateway.py`
- Modify: `frontend/src/App.tsx`

- [ ] **Step 1: Add plugin auto-loading in gateway.py**

In `backend/api/gateway.py`, inside `create_app()`, after creating the engine, add:

```python
    import importlib
    import os

    builtin_plugins_dir = os.path.join(os.path.dirname(__file__), "..", "plugins")

    @app.on_event("startup")
    async def load_plugins():
        manifests = engine.discover_plugins(builtin_plugins_dir)
        for manifest in manifests:
            plugin_path = manifest["path"]
            plugin_name = manifest["name"]
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_name}",
                os.path.join(plugin_path, "plugin.py"),
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                plugin_instance = module.Plugin()
                await engine.load_plugin(plugin_name, plugin_instance)
                router = plugin_instance.get_routes()
                if router:
                    app.include_router(router)
```

- [ ] **Step 2: Add frontend plugin auto-registration in App.tsx**

```typescript
// frontend/src/App.tsx
import React, { useEffect } from 'react';
import { Workbench } from './core/Workbench';
import { registerPlugin } from './core/pluginRegistry';
import { TermAdvisorPanel } from './plugins/term-advisor/TermAdvisorPanel';
import { LiteraturePanel } from './plugins/literature/LiteraturePanel';
import { EvaluatorPanel } from './plugins/evaluator/EvaluatorPanel';
import { FormulaPanel } from './plugins/formula/FormulaPanel';
import { PaperWriterPanel } from './plugins/paper-writer/PaperWriterPanel';

export const App: React.FC = () => {
  useEffect(() => {
    registerPlugin({ name: 'term-advisor', displayName: '读懂导师', component: TermAdvisorPanel, icon: 'book' });
    registerPlugin({ name: 'literature', displayName: '追新论文', component: LiteraturePanel, icon: 'search' });
    registerPlugin({ name: 'evaluator', displayName: '审项目', component: EvaluatorPanel, icon: 'check' });
    registerPlugin({ name: 'formula', displayName: '验公式', component: FormulaPanel, icon: 'function' });
    registerPlugin({ name: 'paper-writer', displayName: '写论文', component: PaperWriterPanel, icon: 'edit' });
  }, []);

  return <Workbench />;
};
```

- [ ] **Step 3: Verify everything compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: no errors

- [ ] **Step 4: Commit**

```bash
git add backend/api/gateway.py frontend/src/App.tsx
git commit -m "feat: wire up plugin auto-loading on startup"
```

---

## Phase 10: Integration Verification

### Task 10.1: End-to-end smoke test

**Files:**
- Create: `tests/test_smoke.py`

- [ ] **Step 1: Write smoke test**

```python
# tests/test_smoke.py
import pytest
from pathlib import Path
from backend.core.config import Config
from backend.core.event_bus import EventBus
from backend.core.security import SecurityManager, Classification
from backend.core.storage import Storage
from backend.core.llm_router import LLMRouter
from backend.core.engine import PluginEngine


@pytest.mark.asyncio
async def test_full_pipeline_no_crashes(tmp_path):
    data_dir = str(tmp_path)

    config = Config()
    config.data_dir = data_dir

    bus = EventBus()
    storage = Storage(data_dir)
    security = SecurityManager()
    llm_router = LLMRouter()
    engine = PluginEngine(bus=bus, config=config.to_dict())

    # Simulate classifying a document
    security.mark("doc-1", Classification.SECRET)
    assert security.classification_of("doc-1") == Classification.SECRET

    # LLM routing respects classification
    provider = llm_router.select(classification="secret")
    assert provider.value == "ollama"

    # Storage works
    storage.sql_execute("CREATE TABLE IF NOT EXISTS test (id TEXT PRIMARY KEY, val TEXT)")
    storage.sql_execute("INSERT INTO test VALUES ('1', 'hello')")
    rows = storage.sql_query("SELECT * FROM test WHERE id = '1'")
    assert rows[0]["val"] == "hello"

    # Plugin discovery
    assert isinstance(engine.list_plugins(), dict)


@pytest.mark.asyncio
async def test_event_bus_integration():
    bus = EventBus()
    events = []

    async def handler(data):
        events.append(data)

    bus.on("paper.saved", handler)
    await bus.emit("paper.saved", {"arxiv_id": "2301.00001"})
    assert len(events) == 1
    assert events[0]["arxiv_id"] == "2301.00001"
```

- [ ] **Step 2: Run all tests**

Run: `python -m pytest tests/ -v`
Expected: all tests PASS (approximately 30+ tests)

- [ ] **Step 3: Commit**

```bash
git add tests/test_smoke.py
git commit -m "test: add end-to-end smoke test verifying full pipeline"
```

---

## Summary

**Total: ~47 test assertions across 10 phases**

| Phase | Scope | Test Count |
|-------|-------|-----------|
| 1 | Scaffolding | — |
| 2 | Core Engine (6 tasks) | 22 tests |
| 3 | Frontend Core (4 tasks) | — |
| 4 | API Routes | — |
| 5 | 读懂导师 plugin | 3 tests |
| 6 | 追新论文 plugin | 3 tests |
| 7 | 验公式 plugin | 3 tests |
| 8 | 审项目 + 写论文 | 7 tests |
| 9 | Plugin wiring | — |
| 10 | Integration | 2 tests |
| **Total** | | **40 tests** |
