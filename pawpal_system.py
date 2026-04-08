from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    scheduled_time: Optional[datetime] = None
    notes: str = ""
    completed: bool = False
    pet_name: Optional[str] = None
    frequency: str = "none"

    def get_description(self) -> str:
        """Return a formatted string description of the task with status and timing info."""
        status = "done" if self.completed else "pending"
        time_label = self.scheduled_time.strftime("%H:%M") if self.scheduled_time else "unscheduled"
        pet_label = f" ({self.pet_name})" if self.pet_name else ""
        frequency_label = f" [{self.frequency}]" if self.frequency != "none" else ""
        return f"{self.title}{pet_label}{frequency_label} [{status}] ({self.priority}, {self.duration_minutes} min, {time_label})"

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return the next recurring task if applicable."""
        self.completed = True
        if self.frequency not in {"daily", "weekly"} or self.scheduled_time is None:
            return None

        delta = timedelta(days=1 if self.frequency == "daily" else 7)
        next_time = self.scheduled_time + delta
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            scheduled_time=next_time,
            notes=self.notes,
            completed=False,
            pet_name=self.pet_name,
            frequency=self.frequency,
        )

    def is_complete(self) -> bool:
        """Return True if the task is complete, False otherwise."""
        return self.completed


@dataclass
class Pet:
    name: str
    animal_type: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks associated with this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]


class Owner:
    def __init__(self, name: str) -> None:
        """Initialize an Owner with a name and empty pet list."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all of this owner's pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all of this owner's pets."""
        return [task for task in self.get_all_tasks() if not task.completed]


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Initialize a Scheduler with an owner reference."""
        self.owner = owner

    def get_tasks(self) -> List[Task]:
        """Return all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by scheduled time, with unscheduled tasks last."""
        tasks = self.get_tasks() if tasks is None else tasks
        return sorted(tasks, key=lambda task: task.scheduled_time or datetime.max)

    def filter_by_pet(self, pet_name: str, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks that belong to the given pet."""
        tasks = self.get_tasks() if tasks is None else tasks
        return [task for task in tasks if task.pet_name == pet_name]

    def filter_by_completion(self, completed: bool, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks that match the completion status."""
        tasks = self.get_tasks() if tasks is None else tasks
        return [task for task in tasks if task.completed is completed]

    def generate_daily_schedule(self) -> List[Task]:
        """Generate and return a prioritized daily schedule of tasks."""
        tasks = self.get_tasks()

        priority_order = {"high": 1, "medium": 2, "low": 3}
        return sorted(tasks, key=lambda task: (
            priority_order.get(task.priority, 99),
            task.completed,
            task.scheduled_time or datetime.max,
            task.duration_minutes,
        ))

    def explain_schedule(self) -> List[str]:
        """Return a list of formatted descriptions for today's schedule."""
        schedule = self.generate_daily_schedule()
        return [task.get_description() for task in schedule]

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and add the next recurring occurrence if needed."""
        next_task = task.mark_complete()
        if next_task is None:
            return None

        for pet in self.owner.get_pets():
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                return next_task

        return None

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Detect tasks scheduled at the same time and return warning messages."""
        tasks = self.get_tasks() if tasks is None else tasks
        scheduled_tasks = [task for task in tasks if task.scheduled_time is not None]
        grouped: dict[datetime, List[Task]] = {}
        for task in scheduled_tasks:
            time_key = task.scheduled_time.replace(second=0, microsecond=0)
            grouped.setdefault(time_key, []).append(task)

        warnings: List[str] = []
        for time, entries in grouped.items():
            if len(entries) < 2:
                continue
            pet_groups: dict[str, List[Task]] = {}
            for task in entries:
                if task.pet_name:
                    pet_groups.setdefault(task.pet_name, []).append(task)

            same_pet_conflicts = [pet for pet, tasks_by_pet in pet_groups.items() if len(tasks_by_pet) > 1]
            if same_pet_conflicts:
                for pet in same_pet_conflicts:
                    warnings.append(
                        f"Conflict: {pet} has multiple tasks scheduled at {time.strftime('%H:%M')}"
                    )
            if len(pet_groups) > 1:
                involved = ", ".join(sorted(pet_groups.keys()))
                warnings.append(
                    f"Potential owner conflict: tasks for {involved} are scheduled at {time.strftime('%H:%M')}"
                )

        return warnings

    def schedule_next_task(self) -> Optional[Task]:
        """Return the highest-priority pending task, or None if no task is pending."""
        pending = [task for task in self.get_tasks() if not task.completed]
        if not pending:
            return None
        return sorted(pending, key=lambda task: (
            {"high": 1, "medium": 2, "low": 3}.get(task.priority, 99),
            task.scheduled_time or datetime.max,
            task.duration_minutes,
        ))[0]
