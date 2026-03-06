"""Tests for Pydantic request models."""

import pytest
from pydantic import ValidationError

from amazing_marvin_mcp.models import (
    EventCreateRequest,
    HabitUpdateRequest,
    ReminderSetRequest,
    TaskUpdateRequest,
)


class TestTaskUpdateRequest:
    """Test TaskUpdateRequest model validation."""

    def test_minimal_update(self):
        update = TaskUpdateRequest(item_id="abc123")
        assert update.item_id == "abc123"
        assert update.title is None
        assert update.due_date is None

    def test_full_update(self):
        update = TaskUpdateRequest(
            item_id="abc123",
            title="New Title",
            due_date="2025-12-31",
            scheduled_date="2025-12-30",
            note="Some notes",
            label_ids=["lbl1", "lbl2"],
            priority="high",
            parent_id="proj1",
            is_starred=True,
            is_frogged=False,
            time_estimate=30,
            backburner=False,
        )
        assert update.title == "New Title"
        assert update.label_ids == ["lbl1", "lbl2"]
        assert update.time_estimate == 30

    def test_missing_item_id_raises(self):
        with pytest.raises(ValidationError):
            TaskUpdateRequest()  # type: ignore[call-arg]


class TestEventCreateRequest:
    """Test EventCreateRequest model validation."""

    def test_valid_event(self):
        event = EventCreateRequest(
            title="Meeting",
            start="2025-12-31T10:00:00Z",
            length_minutes=60,
            note="Team sync",
        )
        assert event.title == "Meeting"
        assert event.length_minutes == 60

    def test_minimal_event(self):
        event = EventCreateRequest(
            title="Meeting",
            start="2025-12-31T10:00:00Z",
            length_minutes=30,
        )
        assert event.note is None

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            EventCreateRequest(title="Meeting")  # type: ignore[call-arg]


class TestHabitUpdateRequest:
    """Test HabitUpdateRequest model validation."""

    def test_record_habit(self):
        habit = HabitUpdateRequest(habit_id="hab1", action="record")
        assert habit.action == "record"
        assert habit.value is None

    def test_record_with_value(self):
        habit = HabitUpdateRequest(habit_id="hab1", action="record", value=3)
        assert habit.value == 3

    def test_undo_habit(self):
        habit = HabitUpdateRequest(habit_id="hab1", action="undo")
        assert habit.action == "undo"


class TestReminderSetRequest:
    """Test ReminderSetRequest model validation."""

    def test_valid_reminder(self):
        reminder = ReminderSetRequest(
            task_id="task1",
            reminder_time="2025-12-31T09:00:00Z",
            note="Don't forget!",
        )
        assert reminder.task_id == "task1"

    def test_minimal_reminder(self):
        reminder = ReminderSetRequest(
            task_id="task1",
            reminder_time="2025-12-31T09:00:00Z",
        )
        assert reminder.note is None
