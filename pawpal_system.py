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

    def get_description(self) -> str:
        return f"{self.title} ({self.priority}, {self.duration_minutes} min)"


@dataclass
class Pet:
    name: str
    animal_type: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


class Owner:
    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        return self.pets


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_daily_schedule(self) -> List[Task]:
        tasks: List[Task] = []
        for pet in self.owner.get_pets():
            tasks.extend(pet.get_tasks())

        # Simple ordering by priority and duration for a basic schedule
        priority_order = {"high": 1, "medium": 2, "low": 3}
        tasks.sort(key=lambda task: (priority_order.get(task.priority, 99), task.duration_minutes))
        return tasks

    def explain_schedule(self) -> List[str]:
        schedule = self.generate_daily_schedule()
        return [f"{task.get_description()}" for task in schedule]
