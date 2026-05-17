import tempfile
import pytest
from backend.core.storage import Storage


@pytest.fixture
def storage():
    tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
    s = Storage(tmp.name)
    yield s
    s.close()
    tmp.cleanup()


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
    tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
    s = Storage(tmp.name)
    yield s
    s.close()
    tmp.cleanup()


def test_chroma_add_and_search(chroma_storage):
    collection = chroma_storage.chroma_collection("test_terms")
    collection.add(
        ids=["t1", "t2"],
        documents=["transformer model architecture", "gradient descent optimization"],
        metadatas=[{"name": "transformer"}, {"name": "gradient_descent"}],
    )
    results = collection.query(query_texts=["neural network architecture"], n_results=1)
    assert len(results["ids"][0]) == 1
