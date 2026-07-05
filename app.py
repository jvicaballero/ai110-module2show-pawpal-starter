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
    time_sensitive = st.checkbox("Time sensitive?")
    task_submitted = st.form_submit_button("Add task")

if task_submitted and task_title:
    selected_pet.add_task(
        Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            time_sensitive=time_sensitive,
        )
    )
    st.success(f"Added '{task_title}' to {selected_pet.name}.")

if selected_pet.get_tasks():
    st.write(f"Tasks for {selected_pet.name}:")
    st.table(
        [
            {
                "title": task.title,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "time_sensitive": task.time_sensitive,
                "completed": task.completed,
            }
            for task in selected_pet.get_tasks()
        ]
    )
else:
    st.info(f"No tasks yet for {selected_pet.name}.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner, employees=st.session_state.employees)
    schedule = scheduler.build_schedule(day=date.today(), start_time=time(8, 0))
    st.session_state.schedule_explanation = scheduler.explain_schedule(schedule)

if "schedule_explanation" in st.session_state:
    st.code(st.session_state.schedule_explanation)
