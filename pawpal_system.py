from dataclasses import dataclass, field
from datetime import date
from typing import Any


# ─────────────────────────────────────────────
# PetCareTask
# ─────────────────────────────────────────────

@dataclass
class PetCareTask:
    task_id: str
    name: str
    category: str           # e.g. "walk", "feeding", "meds", "grooming"
    duration_minutes: int
    priority: int           # 1 (highest) – 5 (lowest)
    preferred_time: str     # e.g. "08:00"
    is_recurring: bool = False
    notes: str = ""

    def add_task(self) -> None:
        """Register/persist this task (hook for storage layer)."""
        pass

    def edit_task(self, field: str, value: Any) -> None:
        """Update a single field by name."""
        pass

    def delete_task(self) -> None:
        """Remove this task (hook for storage layer)."""
        pass

    def get_task_details(self) -> dict:
        """Return a dict summary of this task."""
        pass


# ─────────────────────────────────────────────
# ScheduledTask  (a PetCareTask placed in time)
# ─────────────────────────────────────────────

@dataclass
class ScheduledTask:
    task: PetCareTask
    start_time: str         # e.g. "09:00"
    end_time: str           # e.g. "09:30"
    status: str = "pending" # "pending" | "complete" | "skipped"

    def mark_complete(self) -> None:
        """Mark this scheduled task as done."""
        pass

    def reschedule(self, new_time: str) -> None:
        """Move the task to a new start time and recalculate end_time."""
        pass


# ─────────────────────────────────────────────
# PetInfo
# ─────────────────────────────────────────────

@dataclass
class PetInfo:
    owner_name: str
    owner_email: str
    pet_name: str
    pet_type: str           # e.g. "dog", "cat"
    breed: str
    age: int
    weight: float
    medical_notes: list[str] = field(default_factory=list)

    def get_summary(self) -> str:
        """Return a human-readable summary of owner + pet info."""
        pass

    def update_info(self, field: str, value: Any) -> None:
        """Update a single field by name."""
        pass


# ─────────────────────────────────────────────
# Constraints
# ─────────────────────────────────────────────

@dataclass
class Constraints:
    total_time_available: int       # minutes
    owner_wake_time: str            # e.g. "07:00"
    owner_sleep_time: str           # e.g. "22:00"
    blocked_time_slots: list[str] = field(default_factory=list)
    max_tasks_per_day: int = 10
    owner_preferences: list[str] = field(default_factory=list)
    priority_threshold: int = 3     # tasks with priority > threshold may be skipped

    def set_time_window(self, start: str, end: str) -> None:
        """Set the owner's active time window for the day."""
        pass

    def add_blocked_slot(self, slot: str) -> None:
        """Add a time slot during which no tasks should be scheduled."""
        pass

    def add_preference(self, pref: str) -> None:
        """Append an owner preference (e.g. 'no tasks before 8am')."""
        pass

    def is_task_allowed(self, task: PetCareTask) -> bool:
        """Return True if the task passes all constraint checks."""
        pass

    def get_available_minutes(self) -> int:
        """Calculate total schedulable minutes after blocked slots."""
        pass


# ─────────────────────────────────────────────
# DailySchedule
# ─────────────────────────────────────────────

@dataclass
class DailySchedule:
    schedule_date: date
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    skipped_tasks: list[PetCareTask] = field(default_factory=list)
    reasoning: str = ""

    def generate_schedule(
        self, tasks: list[PetCareTask], constraints: Constraints
    ) -> None:
        """
        Main entry point. Filter tasks through constraints, prioritize,
        fit into the time window, and populate scheduled_tasks / skipped_tasks.
        """
        pass

    def prioritize_tasks(self, tasks: list[PetCareTask]) -> list[PetCareTask]:
        """Return tasks sorted by priority (and any other ordering rules)."""
        pass

    def fit_tasks_to_window(
        self, tasks: list[PetCareTask], constraints: Constraints
    ) -> list[ScheduledTask]:
        """Assign start/end times to tasks that fit within available time."""
        pass

    def display_plan(self) -> str:
        """Return a formatted, human-readable daily plan."""
        pass

    def explain_reasoning(self) -> str:
        """Return a plain-English explanation of scheduling decisions."""
        pass

    def export_schedule(self) -> dict:
        """Serialize the schedule to a dict (for JSON / Streamlit state)."""
        pass