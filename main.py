#!/usr/bin/env python3
"""
Demo script for PawPal+ — tests the core scheduling logic.
"""

from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(owner: Owner, scheduler: Scheduler) -> None:
    """Pretty-print today's schedule."""
    print("\n" + "=" * 60)
    print(f"📅 TODAY'S SCHEDULE FOR {owner.name.upper()}")
    print("=" * 60)
    
    schedule = scheduler.generate_daily_schedule()
    
    if not schedule:
        print("✅ No tasks scheduled — enjoy your day!")
    else:
        for i, task in enumerate(schedule, 1):
            print(f"{i}. {task.get_description()}")
    
    print("=" * 60 + "\n")


def main() -> None:
    # Create owner
    owner = Owner("Jordan")
    
    # Create two pets
    mochi = Pet(name="Mochi", animal_type="dog", breed="mix", age=3)
    luna = Pet(name="Luna", animal_type="cat", breed="Persian", age=5)
    
    # Add tasks to Mochi (dog)
    mochi.add_task(Task(
        title="Morning walk",
        duration_minutes=20,
        priority="high",
        scheduled_time=datetime.now().replace(hour=8, minute=0),
        pet_name="Mochi"
    ))
    mochi.add_task(Task(
        title="Lunch feeding",
        duration_minutes=10,
        priority="high",
        scheduled_time=datetime.now().replace(hour=12, minute=0),
        pet_name="Mochi"
    ))
    mochi.add_task(Task(
        title="Evening playtime",
        duration_minutes=30,
        priority="medium",
        scheduled_time=datetime.now().replace(hour=17, minute=0),
        pet_name="Mochi"
    ))
    
    # Add tasks to Luna (cat)
    luna.add_task(Task(
        title="Fresh water refill",
        duration_minutes=5,
        priority="high",
        scheduled_time=datetime.now().replace(hour=9, minute=0),
        pet_name="Luna"
    ))
    luna.add_task(Task(
        title="Litter box check",
        duration_minutes=10,
        priority="medium",
        scheduled_time=datetime.now().replace(hour=15, minute=0),
        pet_name="Luna"
    ))
    
    # Add pets to owner
    owner.add_pet(mochi)
    owner.add_pet(luna)
    
    # Create scheduler and print schedule
    scheduler = Scheduler(owner)
    print_schedule(owner, scheduler)
    
    # Also print the explain output
    print("📋 SCHEDULE DETAILS:")
    for explanation in scheduler.explain_schedule():
        print(f"  • {explanation}")
    print()


if __name__ == "__main__":
    main()
