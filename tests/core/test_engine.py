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
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        plugin_dir = Path(tmp) / "test_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.toml").write_text("""[plugin]
name = "discovered"
display_name = "discovered plugin"
version = "0.1.0"
""")
        (plugin_dir / "__init__.py").write_text("")
        (plugin_dir / "plugin.py").write_text("""
class Plugin:
    name = "discovered"
    display_name = "discovered plugin"
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
