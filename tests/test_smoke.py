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

    security.mark("doc-1", Classification.SECRET)
    assert security.classification_of("doc-1") == Classification.SECRET

    provider = llm_router.select(classification="secret")
    assert provider.value == "ollama"

    storage.sql_execute("CREATE TABLE IF NOT EXISTS test (id TEXT PRIMARY KEY, val TEXT)")
    storage.sql_execute("INSERT INTO test VALUES ('1', 'hello')")
    rows = storage.sql_query("SELECT * FROM test WHERE id = '1'")
    assert rows[0]["val"] == "hello"

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
