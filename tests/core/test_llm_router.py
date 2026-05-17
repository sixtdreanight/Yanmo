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
