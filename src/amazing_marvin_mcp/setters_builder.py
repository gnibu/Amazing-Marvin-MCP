"""Convert TaskUpdateRequest into Marvin's setters format for /doc/update."""

import time

from .models import TaskUpdateRequest

# Map snake_case model fields to Marvin camelCase keys
_FIELD_MAP: dict[str, str] = {
    "title": "title",
    "due_date": "dueDate",
    "scheduled_date": "day",
    "note": "note",
    "label_ids": "labelIds",
    "priority": "priority",
    "parent_id": "parentId",
    "is_starred": "isStarred",
    "is_frogged": "isFrogged",
    "time_estimate": "timeEstimate",
    "backburner": "backburner",
}


def build_setters(update: TaskUpdateRequest) -> dict:
    """Convert a TaskUpdateRequest into Marvin's $set + fieldUpdates format.

    Only includes fields that are not None. Adds updatedAt and
    fieldUpdates.<key> timestamps automatically.
    """
    now_ms = int(time.time() * 1000)
    set_values: dict = {}
    field_updates: dict = {}

    for model_field, marvin_key in _FIELD_MAP.items():
        value = getattr(update, model_field)
        if value is None:
            continue
        # Convert time_estimate from minutes to milliseconds for Marvin
        if model_field == "time_estimate":
            value = value * 60 * 1000
        set_values[marvin_key] = value
        field_updates[marvin_key] = now_ms

    set_values["updatedAt"] = now_ms

    result: dict = {"$set": set_values}
    if field_updates:
        result["$set"]["fieldUpdates"] = field_updates

    return result
