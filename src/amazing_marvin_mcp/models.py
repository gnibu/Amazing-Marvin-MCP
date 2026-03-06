"""Pydantic request models for Amazing Marvin API operations."""

from pydantic import BaseModel, Field


class TaskUpdateRequest(BaseModel):
    """Friendly task update - converted to setters internally."""

    item_id: str
    title: str | None = None
    due_date: str | None = Field(default=None, description="YYYY-MM-DD")
    scheduled_date: str | None = Field(
        default=None, description="YYYY-MM-DD (maps to 'day' in Marvin)"
    )
    note: str | None = None
    label_ids: list[str] | None = None
    priority: str | None = None
    parent_id: str | None = None
    is_starred: bool | None = None
    is_frogged: bool | None = None
    time_estimate: int | None = Field(
        default=None, description="Time estimate in minutes"
    )
    backburner: bool | None = None


class EventCreateRequest(BaseModel):
    """Request to create a calendar event."""

    title: str
    start: str = Field(description="ISO 8601 datetime string")
    length_minutes: int = Field(description="Duration in minutes")
    note: str | None = None


class HabitUpdateRequest(BaseModel):
    """Request to record or undo a habit."""

    habit_id: str
    action: str = Field(description="'record' or 'undo'")
    value: int | None = Field(default=None, description="Optional value for the habit")


class ReminderSetRequest(BaseModel):
    """A single reminder to set."""

    task_id: str
    reminder_time: str = Field(description="ISO 8601 datetime string")
    note: str | None = None
