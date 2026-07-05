from datetime import date, time

import streamlit as st

from pawpal_system import Employee, Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. Add an owner's pets and their care
tasks below, then generate a daily schedule.
"""
)

# --- Persistent state ---------------------------------------------------
# Streamlit reruns this whole script on every interaction, so the Owner and
# Employee pool must live in st.session_state to survive across reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "employees" not in st.session_state:
    st.session_state.employees = [Employee(name="Alice"), Employee(name="Bob")]

owner: Owner = st.session_state.owner

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name and owner_name != owner.name:
    owner.name = owner_name

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    breed = st.text_input("Breed", value="Mixed")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_submitted = st.form_submit_button("Add pet")

if pet_submitted and pet_name:
    owner.add_pet(Pet(name=pet_name, breed=breed, species=species))
    st.success(f"Added {pet_name} to {owner.name}'s pets.")

if not owner.pets:
    st.info("No pets yet. Add one above.")
    st.stop()

st.write("Current pets:", ", ".join(pet.name for pet in owner.pets))

scheduler = Scheduler(owner=owner, employees=st.session_state.employees)

st.divider()

st.subheader("Add a Task")
pet_names = [pet.name for pet in owner.pets]
selected_pet_name = st.selectbox("Which pet is this task for?", pet_names)
selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)

with st.form("add_task_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    col4, col5 = st.columns(2)
    with col4:
        preferred_time = st.time_input("Preferred time (optional)", value=None)
    with col5:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    time_sensitive = st.checkbox("Time sensitive?")
    task_submitted = st.form_submit_button("Add task")

if task_submitted and task_title:
    selected_pet.add_task(
        Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            time_sensitive=time_sensitive,
            frequency=frequency,
            preferred_time=preferred_time.strftime("%H:%M") if preferred_time else None,
        )
    )
    st.success(f"Added '{task_title}' to {selected_pet.name}.")

st.divider()

st.subheader("Tasks")
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    pet_filter = st.selectbox("Filter by pet", ["All pets"] + pet_names)
with filter_col2:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

filtered = scheduler.filter_tasks(
    completed=(status_filter == "Completed") if status_filter != "All" else None,
    pet_name=None if pet_filter == "All pets" else pet_filter,
)
sorted_tasks = scheduler.sort_by_time(filtered)

if sorted_tasks:
    st.table(
        [
            {
                "preferred_time": task.preferred_time or "--:--",
                "title": task.title,
                "pet": pet.name,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "frequency": task.frequency,
                "completed": task.completed,
            }
            for pet, task in sorted_tasks
        ]
    )
else:
    st.info("No tasks match the selected filters.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    st.session_state.schedule = scheduler.build_schedule(day=date.today(), start_time=time(8, 0))

if "schedule" in st.session_state:
    schedule = st.session_state.schedule

    if schedule.assignments:
        st.table(
            [
                {
                    "start": assignment.start_time.strftime("%H:%M"),
                    "end": assignment.end_time.strftime("%H:%M"),
                    "task": assignment.task.title,
                    "pet": assignment.pet.name,
                    "priority": assignment.task.priority,
                    "employee": assignment.employee.name,
                }
                for assignment in schedule.assignments
            ]
        )
    else:
        st.info("No tasks scheduled.")

    conflicts = scheduler.find_conflicts(schedule)
    if conflicts:
        st.warning(scheduler.check_conflicts(schedule))
    else:
        st.success(scheduler.check_conflicts(schedule))
