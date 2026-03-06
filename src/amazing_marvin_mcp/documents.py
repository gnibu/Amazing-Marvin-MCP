"""Document read/update operations via /doc/* endpoints."""

from typing import Any

from .api import MarvinAPIClient
from .models import TaskUpdateRequest
from .setters_builder import build_setters


def get_document(api_client: MarvinAPIClient, doc_id: str) -> dict[str, Any]:
    """Read any document by ID."""
    return api_client.get_document(doc_id)


def update_task_friendly(
    api_client: MarvinAPIClient, update: TaskUpdateRequest
) -> dict[str, Any]:
    """Update a task using the friendly TaskUpdateRequest model."""
    setters = build_setters(update)
    return api_client.update_document(update.item_id, setters)


def update_document_raw(
    api_client: MarvinAPIClient, item_id: str, setters: dict
) -> dict[str, Any]:
    """Update a document with raw setters for power users."""
    return api_client.update_document(item_id, setters)
