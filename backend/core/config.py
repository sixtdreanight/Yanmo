import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Config:
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:14b"
    cloud_api_key: str = ""
    cloud_provider: str = ""
    cloud_model: str = ""
    default_classification: str = "cautious"
    data_dir: str = field(default_factory=lambda: str(Path.home() / ".yanmo"))

    _SENSITIVE = {"cloud_api_key"}

    @classmethod
    def load(cls, data_dir: str) -> "Config":
        config_path = Path(data_dir) / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                raw = json.load(f)
            cfg = cls(**{k: v for k, v in raw.items() if k in cls.__dataclass_fields__})
            # SECURITY WARNING: cloud_api_key stored in plaintext in config.json.
            # For production deployments, use environment variables or a system
            # keychain instead to avoid leaking credentials through VCS or backups.
            if cfg.cloud_api_key:
                logger.warning(
                    "cloud_api_key found in config.json — storing API keys in "
                    "plaintext files is not recommended for production. Consider "
                    "using environment variables or a system keychain instead."
                )
            return cfg
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
