"""Extended reward point operations."""

from typing import Any

from .api import MarvinAPIClient


def spend_reward_points(
    api_client: MarvinAPIClient, points: int, date: str
) -> dict[str, Any]:
    """Spend reward points."""
    return api_client.spend_reward_points(points, date)


def unclaim_reward_points(
    api_client: MarvinAPIClient, item_id: str, date: str
) -> dict[str, Any]:
    """Unclaim reward points for an item."""
    return api_client.unclaim_reward_points(item_id, date)
