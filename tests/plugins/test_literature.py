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
