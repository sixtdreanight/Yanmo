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
        self._http_client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            self._http_client = httpx.AsyncClient()
        return self._http_client

    async def close(self) -> None:
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

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
        try:
            return Provider(name.lower())
        except ValueError:
            return Provider.OLLAMA

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
        client = self._get_client()
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

        client = self._get_client()
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.cloud_api_key,
                "anthropic-version": "anthropic-2023-06-01",
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
        client = self._get_client()
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
        client = self._get_client()
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
