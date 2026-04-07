"""
Tests for PawPal+ system.
"""

import pytest
from pawpal_system import Owner, Pet, Task


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
