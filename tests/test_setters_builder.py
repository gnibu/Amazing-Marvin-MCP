"""Tests for setters builder conversion."""

from unittest.mock import patch

from amazing_marvin_mcp.models import TaskUpdateRequest
from amazing_marvin_mcp.setters_builder import build_setters

FROZEN_TIME_MS = 1700000000000


def _setters_to_dict(setters: list[dict]) -> dict:
    """Helper to convert setters list to a flat dict for easier assertions."""
    return {s["key"]: s["val"] for s in setters}


class TestBuildSetters:
    """Test conversion from TaskUpdateRequest to Marvin setters format."""

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_title_only(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", title="New Title")
        result = build_setters(update)

        assert isinstance(result, list)
        values = _setters_to_dict(result)
        assert values["title"] == "New Title"
        assert values["updatedAt"] == FROZEN_TIME_MS
        assert values["fieldUpdates.title"] == FROZEN_TIME_MS

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_due_date_maps_correctly(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", due_date="2025-12-31")
        result = build_setters(update)

        values = _setters_to_dict(result)
        assert values["dueDate"] == "2025-12-31"

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_scheduled_date_maps_to_day(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", scheduled_date="2025-12-30")
        result = build_setters(update)

        values = _setters_to_dict(result)
        assert values["day"] == "2025-12-30"

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_time_estimate_converts_to_ms(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", time_estimate=30)
        result = build_setters(update)

        values = _setters_to_dict(result)
        # 30 minutes * 60 seconds * 1000 ms
        assert values["timeEstimate"] == 30 * 60 * 1000

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_boolean_fields(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(
            item_id="task1", is_starred=True, is_frogged=False, backburner=True
        )
        result = build_setters(update)

        values = _setters_to_dict(result)
        assert values["isStarred"] is True
        assert values["isFrogged"] is False
        assert values["backburner"] is True

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_none_fields_excluded(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", title="Only Title")
        result = build_setters(update)

        values = _setters_to_dict(result)
        assert "dueDate" not in values
        assert "day" not in values
        assert "note" not in values
        assert "labelIds" not in values

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_label_ids(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", label_ids=["lbl1", "lbl2"])
        result = build_setters(update)

        values = _setters_to_dict(result)
        assert values["labelIds"] == ["lbl1", "lbl2"]

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_multiple_fields(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(
            item_id="task1",
            title="Updated",
            due_date="2025-12-31",
            note="Notes here",
            priority="high",
        )
        result = build_setters(update)

        values = _setters_to_dict(result)
        assert values["title"] == "Updated"
        assert values["dueDate"] == "2025-12-31"
        assert values["note"] == "Notes here"
        assert values["priority"] == "high"
        # 4 fields + 4 fieldUpdates + 1 updatedAt = 9 entries
        assert len(result) == 9

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_no_updates_still_has_updated_at(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1")
        result = build_setters(update)

        values = _setters_to_dict(result)
        assert values["updatedAt"] == FROZEN_TIME_MS
        # Only updatedAt, no fieldUpdates entries
        assert len(result) == 1
