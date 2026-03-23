from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enum
# ---------------------------------------------------------------------------

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ScheduledTask:
    task: Task
    start_time: str
    end_time: str
    rationale_note: str = ""


@dataclass
class Schedule:
    schedule_id: str
    date: date
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    reasoning_summary: str = ""
    total_duration: int = 0  # minutes

    def add_entry(self, task: ScheduledTask) -> None:
        pass

    def remove_entry(self, task_id: str) -> None:
        pass

    def get_summary(self) -> str:
        pass


@dataclass
class Task:
    task_id: str
    title: str
    description: str
    duration: int              # minutes
    priority: Priority
    frequency: str             # e.g. "daily", "weekly"
    preferred_time: str        # e.g. "morning", "evening"
    is_completed: bool = False
    pet: Optional[Pet] = None

    def mark_complete(self) -> None:
        pass

    def mark_incomplete(self) -> None:
        pass

    def edit(self, field: str, value: object) -> None:
        pass

    def get_remaining_time(self) -> int:
        pass


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    breed: str
    age: int
    medical_notes: str = ""
    tasks: list[Task] = field(default_factory=list)
    owner: Optional[Owner] = None

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def update_info(self, field: str, value: str) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


# ---------------------------------------------------------------------------
# Regular classes
# ---------------------------------------------------------------------------

class Owner:
    def __init__(
        self,
        owner_id: str,
        name: str,
        email: str,
        phone: str,
        preferred_schedule_time: str,
        daily_time_available: int,          # minutes
        preferences: Optional[list[str]] = None,
    ) -> None:
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.phone = phone
        self.preferred_schedule_time = preferred_schedule_time
        self.daily_time_available = daily_time_available
        self.preferences: list[str] = preferences or []
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> None:
        pass

    def update_preferences(self, prefs: list[str]) -> None:
        pass

    def get_schedule(self) -> Schedule:
        pass


class Scheduler:
    def __init__(self, scheduler_id: str, owner: Owner) -> None:
        self.scheduler_id = scheduler_id
        self.owner = owner
        self.task_queue: list[Task] = []
        self.total_time_available: int = owner.daily_time_available
        self.generated_schedule: Optional[Schedule] = None

    def generate_schedule(self) -> Schedule:
        pass

    def prioritize_tasks(self) -> list[Task]:
        pass

    def apply_constraints(self) -> list[Task]:
        pass

    def explain_reasoning(self) -> str:
        pass

    def display_plan(self) -> None:
        pass

    def adjust_schedule(self, task_id: str) -> None:
        pass