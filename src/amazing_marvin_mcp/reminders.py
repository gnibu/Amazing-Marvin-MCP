"""Reminder set/delete operations."""

from typing import Any

from .api import MarvinAPIClient


def set_reminders(
    api_client: MarvinAPIClient, reminders: list[dict[str, Any]]
) -> dict[str, Any]:
    """Set reminders."""
    return api_client.set_reminders(reminders)


def delete_reminders(
    api_client: MarvinAPIClient, reminder_ids: list[str]
) -> dict[str, Any]:
    """Delete specific reminders by ID."""
    return api_client.delete_reminders(reminder_ids)
