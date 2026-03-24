from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional
import uuid


# ---------------------------------------------------------------------------
# Enum
# ---------------------------------------------------------------------------

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# ---------------------------------------------------------------------------
# Time-slot helpers
# ---------------------------------------------------------------------------

_TIME_SLOT_START: dict[str, int] = {
    "morning":   7,
    "afternoon": 12,
    "evening":   17,
    "night":     20,
}

def _slot_start(preferred_time: str, base_date: date) -> datetime:
    """Return a datetime for the preferred time slot on base_date."""
    hour = _TIME_SLOT_START.get(preferred_time.lower(), 8)
    return datetime(base_date.year, base_date.month, base_date.day, hour, 0)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ScheduledTask:
    task: Task
    pet: Pet
    start_time: datetime
    end_time: datetime
    rationale_note: str = ""

    def get_remaining_time(self) -> int:
        """Return minutes remaining until end_time, or 0 if already past."""
        now = datetime.now()
        if now >= self.end_time:
            return 0
        delta = self.end_time - now
        return int(delta.total_seconds() // 60)


@dataclass
class Schedule:
    schedule_id: str
    date: date
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    reasoning_summary: str = ""

    @property
    def total_duration(self) -> int:
        """Compute total scheduled minutes by summing all task durations."""
        return sum(st.task.duration for st in self.scheduled_tasks)

    def add_entry(self, entry: ScheduledTask) -> None:
        """Append a ScheduledTask only if it does not overlap an existing slot."""
        if self._has_overlap(entry):
            raise ValueError(
                f"Task '{entry.task.title}' ({entry.start_time:%H:%M}–"
                f"{entry.end_time:%H:%M}) overlaps an existing scheduled task."
            )
        self.scheduled_tasks.append(entry)

    def _has_overlap(self, entry: ScheduledTask) -> bool:
        """Return True if entry's time window collides with any existing entry."""
        for existing in self.scheduled_tasks:
            if entry.start_time < existing.end_time and existing.start_time < entry.end_time:
                return True
        return False

    def remove_entry(self, task_id: str) -> None:
        """Remove the scheduled entry whose task matches the given task_id."""
        self.scheduled_tasks = [
            st for st in self.scheduled_tasks if st.task.task_id != task_id
        ]

    def get_summary(self) -> str:
        """Return a formatted, terminal-friendly overview of the day's schedule."""
        WIDTH = 60
        if not self.scheduled_tasks:
            return "No tasks scheduled."

        priority_colors = {
            "CRITICAL": "\033[91m",
            "HIGH":     "\033[93m",
            "MEDIUM":   "\033[94m",
            "LOW":      "\033[92m",
        }
        RESET = "\033[0m"
        BOLD  = "\033[1m"

        def colorize(priority_name: str, text: str) -> str:
            """Wrap text in the ANSI color code for the given priority level."""
            return f"{priority_colors.get(priority_name, '')}{text}{RESET}"

        lines = [
            f"\n{BOLD}{'═' * WIDTH}{RESET}",
            f"{BOLD}  🐾 PawPal Daily Schedule — {self.date}{RESET}",
            f"{BOLD}{'═' * WIDTH}{RESET}",
            f"  Total time scheduled : {self.total_duration} min",
            f"  Tasks planned        : {len(self.scheduled_tasks)}",
            f"{'─' * WIDTH}",
        ]

        for st in sorted(self.scheduled_tasks, key=lambda s: s.start_time):
            pri   = st.task.priority.name
            badge = colorize(pri, f"[{pri}]")
            lines += [
                f"  🕐 {st.start_time:%I:%M %p} → {st.end_time:%I:%M %p}",
                f"     {badge} {BOLD}{st.task.title}{RESET}",
                f"     🐶 Pet      : {st.pet.name}",
                f"     ⏱  Duration : {st.task.duration} min",
                f"     🔁 Frequency: {st.task.frequency.capitalize()}",
                f"     💡 Note     : {st.rationale_note}",
                f"{'─' * WIDTH}",
            ]

        return "\n".join(lines)


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
        """Set is_completed to True to mark this task as done."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Reset is_completed to False to reopen this task."""
        self.is_completed = False

    def edit(self, field: str, value: object) -> None:
        """Update a single task field by name, raising AttributeError if unknown."""
        if not hasattr(self, field):
            raise AttributeError(f"Task has no attribute '{field}'.")
        setattr(self, field, value)


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
        """Append a task to this pet and set its back-reference to this pet."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by ID, silently ignoring unknown IDs."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def update_info(self, field: str, value: str) -> None:
        """Update a single pet attribute by name, raising AttributeError if unknown."""
        if not hasattr(self, field):
            raise AttributeError(f"Pet has no attribute '{field}'.")
        setattr(self, field, value)

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of this pet's task list."""
        return list(self.tasks)


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
        daily_time_available: int,
        preferences: Optional[list[str]] = None,
    ) -> None:
        """Initialise an Owner with contact info, time budget, and an empty pet list."""
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.phone = phone
        self.preferred_schedule_time = preferred_schedule_time
        self.daily_time_available = daily_time_available
        self.preferences: list[str] = preferences or []
        self.pets: list[Pet] = []
        self.scheduler: Optional[Scheduler] = None

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner and set its back-reference."""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Unregister a pet by ID, leaving all other pets unchanged."""
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def update_preferences(self, prefs: list[str]) -> None:
        """Replace the owner's preference list with the provided values."""
        self.preferences = prefs

    def get_schedule(self) -> Optional[Schedule]:
        """Delegate schedule retrieval to the attached Scheduler, or return None."""
        if self.scheduler:
            return self.scheduler.generated_schedule
        return None

    def all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair across all pets owned by this owner."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


@dataclass
class ScheduleAdjustment:
    """Describes a single targeted change to apply to a generated schedule."""
    task_id: str
    new_start_time: Optional[datetime] = None
    new_end_time: Optional[datetime] = None
    new_priority: Optional[Priority] = None
    remove: bool = False


class Scheduler:
    def __init__(self, scheduler_id: str, owner: Owner) -> None:
        """Initialise the Scheduler, link it to the owner, and reset the task queue."""
        self.scheduler_id = scheduler_id
        self.owner = owner
        self.task_queue: list[tuple[Pet, Task]] = []
        self.total_time_available: int = owner.daily_time_available
        self.generated_schedule: Optional[Schedule] = None
        owner.scheduler = self

    def load_tasks(self) -> None:
        """Collect all incomplete tasks from owner → pets → tasks into task_queue."""
        self.task_queue = [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if not task.is_completed
        ]

    def prioritize_tasks(self) -> list[tuple[Pet, Task]]:
        """Sort task_queue by priority descending, using preferred_time slot as tiebreaker."""
        slot_order = list(_TIME_SLOT_START.keys())

        def sort_key(pair: tuple[Pet, Task]) -> tuple[int, int]:
            """Return a (negated priority, slot index) tuple for stable sorting."""
            _, task = pair
            pri  = -task.priority.value
            slot = slot_order.index(task.preferred_time.lower()) \
                   if task.preferred_time.lower() in slot_order else 99
            return (pri, slot)

        return sorted(self.task_queue, key=sort_key)

    def apply_constraints(self) -> list[tuple[Pet, Task]]:
        """Filter tasks to fit the time budget, favouring the owner's preferred slot first."""
        prioritized = self.prioritize_tasks()
        owner_pref  = self.owner.preferred_schedule_time.lower()

        preferred = [(p, t) for p, t in prioritized if t.preferred_time.lower() == owner_pref]
        others    = [(p, t) for p, t in prioritized if t.preferred_time.lower() != owner_pref]

        ordered, total = [], 0
        for pair in preferred + others:
            _, task = pair
            if total + task.duration <= self.total_time_available:
                ordered.append(pair)
                total += task.duration
        return ordered

    def generate_schedule(self) -> Schedule:
        """Run the full pipeline (load → prioritise → constrain → slot) and return a Schedule."""
        self.load_tasks()
        constrained = self.apply_constraints()
        today = date.today()

        schedule = Schedule(schedule_id=str(uuid.uuid4()), date=today)
        slot_cursors: dict[str, datetime] = {}

        for pet, task in constrained:
            slot = task.preferred_time.lower()
            if slot not in slot_cursors:
                slot_cursors[slot] = _slot_start(slot, today)

            start = slot_cursors[slot]
            end   = start + timedelta(minutes=task.duration)
            note  = (
                f"Priority={task.priority.name}; "
                f"fits within {self.total_time_available}-min window"
            )
            entry = ScheduledTask(task=task, pet=pet, start_time=start, end_time=end, rationale_note=note)
            schedule.add_entry(entry)
            slot_cursors[slot] = end

        schedule.reasoning_summary = self.explain_reasoning(constrained)
        self.generated_schedule = schedule
        return schedule

    def explain_reasoning(
        self, constrained: Optional[list[tuple[Pet, Task]]] = None
    ) -> str:
        """Return a colour-formatted explanation of which tasks were scheduled or skipped."""
        WIDTH = 60
        BOLD  = "\033[1m"
        RESET = "\033[0m"
        GREEN = "\033[92m"
        RED   = "\033[91m"

        source = constrained or (
            [(st.pet, st.task) for st in self.generated_schedule.scheduled_tasks]
            if self.generated_schedule else []
        )
        if not source:
            return "No tasks were scheduled."

        skipped = [(pet, task) for pet, task in self.task_queue if (pet, task) not in source]

        lines = [
            f"\n{BOLD}{'═' * WIDTH}{RESET}",
            f"{BOLD}  🧠 Scheduling Reasoning{RESET}",
            f"{BOLD}{'═' * WIDTH}{RESET}",
            f"  Owner            : {self.owner.name}",
            f"  Time budget      : {self.total_time_available} min",
            f"  Preferred slot   : {self.owner.preferred_schedule_time.capitalize()}",
            f"  Tasks considered : {len(self.task_queue)}",
            f"{'─' * WIDTH}",
            f"{BOLD}  ✅ Scheduled ({len(source)}){RESET}",
        ]
        for pet, task in source:
            lines.append(
                f"  {GREEN}✔{RESET} {task.title:<28} "
                f"{task.priority.name:<8} {task.duration} min  [{pet.name}]"
            )
        if skipped:
            lines += [f"{'─' * WIDTH}", f"{BOLD}  ⛔ Excluded — time budget exceeded ({len(skipped)}){RESET}"]
            for pet, task in skipped:
                lines.append(
                    f"  {RED}✘{RESET} {task.title:<28} "
                    f"{task.priority.name:<8} {task.duration} min  [{pet.name}]"
                )
        lines.append(f"{'═' * WIDTH}\n")
        return "\n".join(lines)

    def display_plan(self) -> None:
        """Print the generated schedule to stdout, or warn if none exists yet."""
        if not self.generated_schedule:
            print("No schedule generated yet. Call generate_schedule() first.")
            return
        print(self.generated_schedule.get_summary())

    def adjust_schedule(self, adjustment: ScheduleAdjustment) -> None:
        """Apply a ScheduleAdjustment (remove, reschedule, or reprioritise) to the current schedule."""
        if not self.generated_schedule:
            raise RuntimeError("No schedule to adjust. Call generate_schedule() first.")

        sched = self.generated_schedule

        if adjustment.remove:
            sched.remove_entry(adjustment.task_id)
            return

        target = next(
            (st for st in sched.scheduled_tasks if st.task.task_id == adjustment.task_id), None
        )
        if target is None:
            raise ValueError(f"No scheduled task with id '{adjustment.task_id}'.")

        if adjustment.new_priority is not None:
            target.task.priority = adjustment.new_priority

        if adjustment.new_start_time or adjustment.new_end_time:
            new_start = adjustment.new_start_time or target.start_time
            new_end   = adjustment.new_end_time   or target.end_time

            sched.scheduled_tasks.remove(target)
            probe = ScheduledTask(task=target.task, pet=target.pet, start_time=new_start, end_time=new_end)
            if sched._has_overlap(probe):
                sched.scheduled_tasks.append(target)
                raise ValueError(
                    f"Adjusted time {new_start:%H:%M}–{new_end:%H:%M} conflicts with another task."
                )
            target.start_time = new_start
            target.end_time   = new_end
            sched.scheduled_tasks.append(target)