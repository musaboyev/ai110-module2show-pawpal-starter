import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner

st.markdown("### Add a pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="mix")
age = st.number_input("Age (years)", min_value=0, max_value=30, value=1)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, animal_type=species, breed=breed, age=int(age))
    owner.add_pet(new_pet)
    st.success(f"Added pet: {new_pet.name} ({new_pet.animal_type})")

pets = owner.get_pets()
if pets:
    st.write("Current pets:")
    pet_table = [{"name": pet.name, "species": pet.animal_type, "breed": pet.breed, "age": pet.age} for pet in pets]
    st.table(pet_table)
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
if pets:
    pet_names = [pet.name for pet in pets]
    selected_pet_name = st.selectbox("Assign task to", pet_names)
    selected_pet = next((pet for pet in pets if pet.name == selected_pet_name), None)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    frequency = st.selectbox("Frequency", ["none", "daily", "weekly"], index=0)
    scheduled_time = st.time_input("Scheduled time", value=datetime.now().time().replace(hour=8, minute=0, second=0, microsecond=0))

    if st.button("Add task"):
        if selected_pet is not None:
            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                pet_name=selected_pet.name,
                frequency=frequency,
                scheduled_time=datetime.now().replace(
                    hour=scheduled_time.hour,
                    minute=scheduled_time.minute,
                    second=0,
                    microsecond=0,
                ),
            )
            selected_pet.add_task(task)
            st.success(f"Added task to {selected_pet.name}: {task_title}")
        else:
            st.error("Please select a pet before adding a task.")

    if pets:
        st.write("Current tasks by pet:")
        for pet in pets:
            if pet.get_tasks():
                st.markdown(f"**{pet.name} ({pet.animal_type})**")
                task_rows = [
                    {"title": t.title, "priority": t.priority, "duration": t.duration_minutes, "frequency": t.frequency, "status": "done" if t.completed else "pending", "time": t.scheduled_time.strftime("%H:%M") if t.scheduled_time else "unscheduled"}
                    for t in pet.get_tasks()
                ]
                st.table(task_rows)
            else:
                st.write(f"{pet.name} has no tasks yet.")
else:
    st.info("Add a pet first before creating tasks.")

st.divider()

st.subheader("Build Schedule")
if pets:
    schedule_pet_options = ["All"] + [pet.name for pet in pets]
    schedule_pet_filter = st.selectbox("Filter schedule by pet", schedule_pet_options)
    status_filter = st.selectbox("Filter schedule by status", ["all", "pending", "done"])
else:
    schedule_pet_filter = "All"
    status_filter = "all"

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("Add tasks first so the scheduler has work to do.")
    else:
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_daily_schedule()

        if schedule_pet_filter != "All":
            schedule = scheduler.filter_by_pet(schedule_pet_filter, schedule)

        if status_filter != "all":
            desired_completed = status_filter == "done"
            schedule = [task for task in schedule if task.completed == desired_completed]

        conflict_warnings = scheduler.detect_conflicts()
        if conflict_warnings:
            for warning in conflict_warnings:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts detected.")

        st.write("### Today's Schedule")
        schedule_rows = [
            {"task": t.title, "pet": t.pet_name, "priority": t.priority, "duration": t.duration_minutes, "frequency": t.frequency, "status": "done" if t.completed else "pending", "time": t.scheduled_time.strftime("%H:%M") if t.scheduled_time else "unscheduled"}
            for t in schedule
        ]
        st.table(schedule_rows)
        st.write("### Explanation")
        for explanation in scheduler.explain_schedule():
            st.write(f"- {explanation}")
