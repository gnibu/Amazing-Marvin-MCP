"""Habit operations."""

from typing import Any

from .api import MarvinAPIClient


def get_habits(api_client: MarvinAPIClient) -> list[dict[str, Any]]:
    """List all habits."""
    return api_client.get_habits()


def get_habit(api_client: MarvinAPIClient, habit_id: str) -> dict[str, Any]:
    """Get a single habit with history."""
    return api_client.get_habit(habit_id)


def record_habit(
    api_client: MarvinAPIClient, habit_id: str, value: int | None = None
) -> dict[str, Any]:
    """Record a habit occurrence."""
    data: dict[str, Any] = {"habitId": habit_id, "action": "record"}
    if value is not None:
        data["value"] = value
    return api_client.update_habit(data)


def undo_habit(api_client: MarvinAPIClient, habit_id: str) -> dict[str, Any]:
    """Undo last habit recording."""
    return api_client.update_habit({"habitId": habit_id, "action": "undo"})
