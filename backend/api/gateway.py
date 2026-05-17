# backend/api/gateway.py
import hashlib
import importlib
import json
import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.core.engine import PluginEngine
from backend.core.event_bus import EventBus
from backend.core.config import Config
from backend.core.storage import Storage
from backend.core.security import SecurityManager, Classification
from backend.core.llm_router import LLMRouter

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    messages: list[dict] = Field(..., max_length=100)
    classification: str = Field(max_length=20)
    doc_id: str = Field(max_length=200)


class ClassifyRequest(BaseModel):
    doc_id: str = Field(max_length=200)
    level: str = Field(max_length=20)


class SearchRequest(BaseModel):
    collection: str = Field(max_length=100)
    query: str = Field(max_length=1000)
    n: int = Field(default=5, ge=1, le=100)


class SettingsUpdate(BaseModel):
    ollama_base_url: str = ""
    ollama_model: str = ""
    cloud_provider: str = ""
    cloud_api_key: str = ""
    cloud_model: str = ""


def _hash_messages(messages: list[dict]) -> str:
    """Deterministic SHA-256 hash of messages for audit trail."""
    canonical = json.dumps(messages, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def _rebuild_llm_router(config: Config, app: FastAPI) -> None:
    """Rebuild LLMRouter from current config — called after settings update."""
    app.state.llm_router = LLMRouter(
        ollama_base_url=config.ollama_base_url,
        ollama_model=config.ollama_model,
        cloud_provider=config.cloud_provider,
        cloud_api_key=config.cloud_api_key,
        cloud_model=config.cloud_model,
    )


def create_app(config: Config) -> FastAPI:
    app = FastAPI(title="研墨", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:5174", "tauri://localhost"],
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

    @app.post("/api/chat")
    async def chat(req: ChatRequest, request: Request):
        sec = request.app.state.security
        llm = request.app.state.llm_router

        sec.mark(req.doc_id, Classification(req.classification))
        approved = sec.allow_cloud(req.doc_id)
        provider = llm.select(classification=req.classification, cloud_approved=approved)

        content_hash = _hash_messages(req.messages)
        if provider.value != "ollama":
            sec.log_cloud_send(req.doc_id, llm.cloud_model, content_hash)

        result = await llm.chat(provider, req.messages)
        return {"content": result, "provider": provider.value}

    @app.post("/api/security/classify")
    async def classify(req: ClassifyRequest, request: Request):
        sec = request.app.state.security
        sec.mark(req.doc_id, Classification(req.level))
        return {"status": "ok"}

    @app.get("/api/security/allow-cloud/{doc_id}")
    async def allow_cloud(doc_id: str, request: Request):
        sec = request.app.state.security
        allowed = sec.allow_cloud(doc_id)
        return {"allowed": allowed}

    @app.get("/api/security/audit-log")
    async def audit_log(request: Request):
        sec = request.app.state.security
        return {"entries": sec.audit_log()}

    @app.get("/api/settings")
    async def get_settings(request: Request):
        cfg = request.app.state.config
        return cfg.to_dict()

    @app.put("/api/settings")
    async def update_settings(req: SettingsUpdate, request: Request):
        cfg = request.app.state.config
        for key, val in req.model_dump(exclude_unset=True).items():
            if hasattr(cfg, key):
                setattr(cfg, key, val)
        cfg.save()
        _rebuild_llm_router(cfg, request.app)
        return {"status": "ok"}

    @app.post("/api/knowledge/search")
    async def search_knowledge(req: SearchRequest, request: Request):
        storage = request.app.state.storage
        collection = storage.chroma_collection(req.collection)
        results = collection.query(query_texts=[req.query], n_results=req.n)
        return {"results": results.get("ids", [[]])}

    # Set up plugin directories
    builtin_plugins_dir = os.path.join(os.path.dirname(__file__), "..", "plugins")
    user_plugins_dir = os.path.join(config.data_dir, "plugins")
    engine.set_user_plugins_dir(user_plugins_dir)
    engine._plugin_dirs = [builtin_plugins_dir, user_plugins_dir]

    @app.on_event("startup")
    async def load_plugins():
        manifests = engine.discover_all()
        for manifest in manifests:
            loaded = await engine.load_plugin_from_path(
                manifest["path"], manifest["name"]
            )
            if loaded:
                plugin = engine._plugins.get(manifest["name"])
                if plugin:
                    router = plugin.get_routes()
                    if router:
                        app.include_router(router)

    # Plugin management routes
    @app.get("/api/plugins/available")
    async def available_plugins():
        manifests = engine.discover_all()
        loaded = set(engine.list_plugins().keys())
        return {
            "plugins": [
                {**m, "loaded": m["name"] in loaded}
                for m in manifests
            ]
        }

    @app.post("/api/plugins/{name}/load")
    async def load_single_plugin(name: str):
        manifests = engine.discover_all()
        match = next((m for m in manifests if m["name"] == name), None)
        if not match:
            return {"status": "error", "message": "Plugin not found"}
        if name in engine.list_plugins():
            return {"status": "ok", "message": "Already loaded"}
        ok = await engine.load_plugin_from_path(match["path"], name)
        if ok:
            plugin = engine._plugins.get(name)
            if plugin:
                router = plugin.get_routes()
                if router:
                    app.include_router(router)
            return {"status": "ok"}
        return {"status": "error", "message": "Failed to load plugin"}

    @app.post("/api/plugins/{name}/unload")
    async def unload_single_plugin(name: str):
        if name not in engine.list_plugins():
            return {"status": "error", "message": "Plugin not loaded"}
        await engine.unload_plugin(name)
        return {"status": "ok"}

    return app
