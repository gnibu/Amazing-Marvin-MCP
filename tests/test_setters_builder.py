"""Tests for setters builder conversion."""

from unittest.mock import patch

from amazing_marvin_mcp.models import TaskUpdateRequest
from amazing_marvin_mcp.setters_builder import build_setters

FROZEN_TIME_MS = 1700000000000


class TestBuildSetters:
    """Test conversion from TaskUpdateRequest to Marvin setters format."""

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_title_only(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", title="New Title")
        result = build_setters(update)

        assert "$set" in result
        assert result["$set"]["title"] == "New Title"
        assert result["$set"]["updatedAt"] == FROZEN_TIME_MS
        assert result["$set"]["fieldUpdates"]["title"] == FROZEN_TIME_MS

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_due_date_maps_correctly(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", due_date="2025-12-31")
        result = build_setters(update)

        assert result["$set"]["dueDate"] == "2025-12-31"

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_scheduled_date_maps_to_day(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", scheduled_date="2025-12-30")
        result = build_setters(update)

        assert result["$set"]["day"] == "2025-12-30"

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_time_estimate_converts_to_ms(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", time_estimate=30)
        result = build_setters(update)

        # 30 minutes * 60 seconds * 1000 ms
        assert result["$set"]["timeEstimate"] == 30 * 60 * 1000

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_boolean_fields(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(
            item_id="task1", is_starred=True, is_frogged=False, backburner=True
        )
        result = build_setters(update)

        assert result["$set"]["isStarred"] is True
        assert result["$set"]["isFrogged"] is False
        assert result["$set"]["backburner"] is True

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_none_fields_excluded(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", title="Only Title")
        result = build_setters(update)

        set_values = result["$set"]
        assert "dueDate" not in set_values
        assert "day" not in set_values
        assert "note" not in set_values
        assert "labelIds" not in set_values

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_label_ids(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1", label_ids=["lbl1", "lbl2"])
        result = build_setters(update)

        assert result["$set"]["labelIds"] == ["lbl1", "lbl2"]

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

        set_values = result["$set"]
        assert set_values["title"] == "Updated"
        assert set_values["dueDate"] == "2025-12-31"
        assert set_values["note"] == "Notes here"
        assert set_values["priority"] == "high"
        assert len(result["$set"]["fieldUpdates"]) == 4

    @patch("amazing_marvin_mcp.setters_builder.time")
    def test_no_updates_still_has_updated_at(self, mock_time):
        mock_time.time.return_value = FROZEN_TIME_MS / 1000
        update = TaskUpdateRequest(item_id="task1")
        result = build_setters(update)

        assert result["$set"]["updatedAt"] == FROZEN_TIME_MS
        assert "fieldUpdates" not in result["$set"]
