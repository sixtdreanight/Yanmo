from enum import Enum
from datetime import datetime, timezone
from typing import Any


class Classification(str, Enum):
    SECRET = "secret"
    CAUTIOUS = "cautious"
    PUBLIC = "public"


class SecurityManager:
    def __init__(self) -> None:
        self._classifications: dict[str, Classification] = {}
        self._cloud_approvals: set[str] = set()
        self._audit: list[dict[str, Any]] = []

    def mark(self, doc_id: str, level: Classification) -> None:
        self._classifications[doc_id] = level

    def classify_batch(self, mapping: dict[str, Classification]) -> None:
        self._classifications.update(mapping)

    def classification_of(self, doc_id: str) -> Classification:
        return self._classifications.get(doc_id, Classification.CAUTIOUS)

    def allow_cloud(self, doc_id: str) -> bool:
        level = self.classification_of(doc_id)
        if level == Classification.SECRET:
            return False
        if level == Classification.PUBLIC:
            return True
        return doc_id in self._cloud_approvals

    def approve_cloud(self, doc_id: str) -> None:
        self._cloud_approvals.add(doc_id)

    def log_cloud_send(self, doc_id: str, target_model: str, content_hash: str) -> None:
        self._audit.append({
            "doc_id": doc_id,
            "target_model": target_model,
            "content_hash": content_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def audit_log(self) -> list[dict[str, Any]]:
        return list(self._audit)
