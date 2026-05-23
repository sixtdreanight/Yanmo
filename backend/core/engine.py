import importlib.util
import logging
import os
import tomllib
from pathlib import Path
from typing import Any

from backend.core.event_bus import EventBus

logger = logging.getLogger(__name__)


class PluginEngine:
    def __init__(self, bus: EventBus, config: dict[str, Any]):
        self._bus = bus
        self._config = config
        self._plugins: dict[str, Any] = {}
        self._plugin_dirs: list[str] = []
        self._user_plugins_dir: str = ""

    def set_user_plugins_dir(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        self._user_plugins_dir = path

    def discover_plugins(self, plugins_dir: str) -> list[dict[str, Any]]:
        manifests = []
        base = Path(plugins_dir)
        if not base.exists():
            return manifests
        for candidate in base.iterdir():
            if not candidate.is_dir():
                continue
            manifest_path = candidate / "plugin.toml"
            if not manifest_path.exists():
                continue
            try:
                raw = tomllib.loads(manifest_path.read_text())
            except Exception:
                continue
            p = raw.get("plugin", {})
            manifests.append({
                "name": p.get("name", candidate.name),
                "display_name": p.get("display_name", candidate.name),
                "version": p.get("version", "0.0.0"),
                "description": p.get("description", ""),
                "author": p.get("author", ""),
                "path": str(candidate),
                "source": "builtin" if str(base) in str(Path(__file__).parent.parent / "plugins") else "user",
            })
        return manifests

    def discover_all(self) -> list[dict[str, Any]]:
        """Discover from all registered plugin directories."""
        manifests: list[dict[str, Any]] = []
        for d in self._plugin_dirs:
            manifests.extend(self.discover_plugins(d))
        return manifests

    async def load_plugin_from_path(self, plugin_path: str, plugin_name: str) -> bool:
        """Load a plugin from its directory path. Returns True on success."""
        plugin_file = os.path.join(plugin_path, "plugin.py")
        if not os.path.exists(plugin_file):
            logger.warning("No plugin.py found at %s", plugin_path)
            return False

        try:
            # SECURITY: 仅从受信任目录加载（builtin: backend/plugins/, user: ~/.yanmo/plugins/）
            # 插件在进程内运行，可访问 os/subprocess/socket。生产部署建议：
            #   1. 验证 plugin.toml 签名
            #   2. 使用 subprocess/multiprocessing 隔离不受信任的第三方插件
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_name}", plugin_file
            )
            if not spec or not spec.loader:
                return False
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            plugin_instance = module.Plugin()
            await self.load_plugin(plugin_name, plugin_instance)
            logger.info("Plugin loaded: %s from %s", plugin_name, plugin_path)
            return True
        except Exception:
            logger.exception("Failed to load plugin %s from %s", plugin_name, plugin_path)
            return False

    async def load_plugin(self, name: str, plugin: Any) -> None:
        await plugin.on_load(self._bus, self._config)
        self._plugins[name] = plugin

    async def unload_plugin(self, name: str) -> None:
        if name in self._plugins:
            await self._plugins[name].on_unload()
            del self._plugins[name]

    def list_plugins(self) -> dict[str, Any]:
        return dict(self._plugins)

    def get_plugin_info(self, name: str) -> dict[str, Any] | None:
        plugin = self._plugins.get(name)
        if not plugin:
            return None
        return {
            "name": getattr(plugin, "name", name),
            "display_name": getattr(plugin, "display_name", name),
            "version": getattr(plugin, "version", "0.0.0"),
        }

    async def shutdown(self) -> None:
        for name in list(self._plugins):
            await self.unload_plugin(name)
