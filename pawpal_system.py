from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
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

    def get_description(self) -> str:
        """Return a formatted string description of the task with status and timing info."""
        status = "done" if self.completed else "pending"
        time_label = self.scheduled_time.strftime("%H:%M") if self.scheduled_time else "unscheduled"
        pet_label = f" ({self.pet_name})" if self.pet_name else ""
        return f"{self.title}{pet_label} [{status}] ({self.priority}, {self.duration_minutes} min, {time_label})"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

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

    def generate_daily_schedule(self) -> List[Task]:
        """Generate and return a prioritized daily schedule of tasks."""
        tasks = self.get_tasks()

        priority_order = {"high": 1, "medium": 2, "low": 3}
        tasks.sort(key=lambda task: (
            priority_order.get(task.priority, 99),
            task.completed,
            task.scheduled_time or datetime.max,
            task.duration_minutes,
        ))
        return tasks

    def explain_schedule(self) -> List[str]:
        """Return a list of formatted descriptions for today's schedule."""
        schedule = self.generate_daily_schedule()
        return [task.get_description() for task in schedule]

    def schedule_next_task(self) -> Optional[Task]:
        """Return the highest-priority pending task, or None if no task is pending."""
        pending = [task for task in self.get_tasks() if not task.completed]
        if not pending:
            return None
        return sorted(pending, key=lambda task: (task.priority, task.duration_minutes))[0]
