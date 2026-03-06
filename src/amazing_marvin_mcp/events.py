"""Event creation and time block operations."""

from typing import Any

from .api import MarvinAPIClient


def add_event(
    api_client: MarvinAPIClient,
    title: str,
    start: str,
    length_minutes: int,
    note: str | None = None,
) -> dict[str, Any]:
    """Create a calendar event. Converts length_minutes to milliseconds for Marvin."""
    ms_per_minute = 60_000
    event_data: dict[str, Any] = {
        "title": title,
        "start": start,
        "length": length_minutes * ms_per_minute,
    }
    if note is not None:
        event_data["note"] = note
    return api_client.add_event(event_data)


def get_today_time_blocks(
    api_client: MarvinAPIClient, date: str | None = None
) -> list[dict[str, Any]]:
    """Get time blocks for a date (defaults to today)."""
    return api_client.get_today_time_blocks(date)
