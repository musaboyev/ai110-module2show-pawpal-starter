"""
Tests for PawPal+ system.
"""

import pytest
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTaskCompletion:
    """Test task completion behavior."""
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's status."""
        task = Task(
            title="Morning walk",
            duration_minutes=20,
            priority="high"
        )
        
        # Initially, task should not be complete
        assert task.completed == False
        assert task.is_complete() == False
        
        # Mark complete
        task.mark_complete()
        
        # Now it should be complete
        assert task.completed == True
        assert task.is_complete() == True


class TestTaskAddition:
    """Test adding tasks to pets."""
    
    def test_adding_task_increases_pet_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(name="Mochi", animal_type="dog", breed="mix", age=3)
        
        # Initially no tasks
        assert len(pet.get_tasks()) == 0
        
        # Add a task
        task1 = Task(title="Walk", duration_minutes=20, priority="high")
        pet.add_task(task1)
        
        # Should have 1 task now
        assert len(pet.get_tasks()) == 1
        
        # Add another task
        task2 = Task(title="Feed", duration_minutes=10, priority="high")
        pet.add_task(task2)
        
        # Should have 2 tasks now
        assert len(pet.get_tasks()) == 2


class TestSchedulerSortingFiltering:
    """Test scheduler sorting and filtering behaviors."""

    def test_sort_by_time_orders_tasks_chronologically(self):
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", animal_type="dog", breed="mix", age=3)
        pet.add_task(Task(title="Afternoon play", duration_minutes=20, priority="medium", scheduled_time=datetime(2026, 1, 1, 15, 0), pet_name="Mochi"))
        pet.add_task(Task(title="Morning walk", duration_minutes=20, priority="high", scheduled_time=datetime(2026, 1, 1, 8, 0), pet_name="Mochi"))
        pet.add_task(Task(title="Lunchtime feed", duration_minutes=10, priority="high", scheduled_time=datetime(2026, 1, 1, 12, 0), pet_name="Mochi"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_by_time()

        assert [task.title for task in sorted_tasks] == ["Morning walk", "Lunchtime feed", "Afternoon play"]

    def test_filter_by_pet_returns_only_matching_tasks(self):
        owner = Owner("Jordan")
        mochi = Pet(name="Mochi", animal_type="dog", breed="mix", age=3)
        luna = Pet(name="Luna", animal_type="cat", breed="Persian", age=5)
        mochi.add_task(Task(title="Walk", duration_minutes=20, priority="high", pet_name="Mochi"))
        luna.add_task(Task(title="Feed", duration_minutes=10, priority="medium", pet_name="Luna"))
        owner.add_pet(mochi)
        owner.add_pet(luna)

        scheduler = Scheduler(owner)
        luna_tasks = scheduler.filter_by_pet("Luna")

        assert len(luna_tasks) == 1
        assert luna_tasks[0].title == "Feed"


class TestRecurringAndConflictDetection:
    """Test recurring task generation and conflict warnings."""

    def test_mark_complete_creates_next_daily_task(self):
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", animal_type="dog", breed="mix", age=3)
        task = Task(
            title="Morning walk",
            duration_minutes=20,
            priority="high",
            scheduled_time=datetime(2026, 1, 1, 8, 0),
            pet_name="Mochi",
            frequency="daily"
        )
        pet.add_task(task)
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        next_task = scheduler.mark_task_complete(task)

        assert task.completed is True
        assert next_task is not None
        assert next_task.scheduled_time == datetime(2026, 1, 2, 8, 0)
        assert next_task.frequency == "daily"
        assert next_task.pet_name == "Mochi"
        assert len(pet.get_tasks()) == 2

    def test_detect_conflicts_flags_duplicate_times(self):
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", animal_type="dog", breed="mix", age=3)
        pet.add_task(Task(title="Morning walk", duration_minutes=20, priority="high", scheduled_time=datetime(2026, 1, 1, 8, 0), pet_name="Mochi"))
        pet.add_task(Task(title="Vet check", duration_minutes=15, priority="medium", scheduled_time=datetime(2026, 1, 1, 8, 0), pet_name="Mochi"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts()

        assert any("Conflict: Mochi" in warning for warning in conflicts)
