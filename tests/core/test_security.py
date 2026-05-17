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


def test_classify_batch_marks_multiple():
    sm = SecurityManager()
    sm.classify_batch({
        "a": Classification.SECRET,
        "b": Classification.PUBLIC,
    })
    assert sm.classification_of("a") == Classification.SECRET
    assert sm.classification_of("b") == Classification.PUBLIC
