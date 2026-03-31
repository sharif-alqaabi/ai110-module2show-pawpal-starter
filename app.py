import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        time_available=60,
        preferences=[],
    )

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

Use this app to add pets, create care tasks, and generate a daily care schedule.
"""
)

st.divider()

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
available_time = st.number_input(
    "Time available today (minutes)",
    min_value=1,
    max_value=720,
    value=owner.time_available,
)
preferences_text = st.text_input(
    "Preferences",
    value=", ".join(owner.preferences),
    placeholder="Example: prioritize health, short walks",
)

if st.button("Save owner details"):
    owner.name = owner_name
    owner.time_available = int(available_time)
    parsed_preferences = [item.strip() for item in preferences_text.split(",") if item.strip()]
    owner.update_preferences(parsed_preferences)
    st.success("Owner details updated.")

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=1)
    care_notes = st.text_input("Care notes", placeholder="Example: needs a calm morning routine")
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.error("Enter a pet name before adding a pet.")
    else:
        owner.add_pet(
            Pet(
                name=pet_name.strip(),
                species=species,
                age=int(age),
                care_notes=care_notes.strip(),
            )
        )
        st.success(f"Added {pet_name.strip()} to {owner.name}'s household.")

st.subheader("Current Pets")
if owner.pets:
    for pet in owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species}, age {pet.age})")
        if pet.care_notes:
            st.caption(pet.care_notes)
        if pet.tasks:
            st.table(
                [
                    {
                        "Task": task.name,
                        "Category": task.category,
                        "Duration": task.duration,
                        "Priority": task.priority,
                        "Frequency": task.frequency,
                        "Completed": task.completed,
                    }
                    for task in pet.tasks
                ]
            )
        else:
            st.caption("No tasks yet for this pet.")
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)

    with st.form("add_task_form"):
        task_name = st.text_input("Task name", value="Morning walk")
        category = st.text_input("Category", value="exercise")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], index=0)
        required_today = st.checkbox("Required today", value=True)
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        priority_map = {"low": 1, "medium": 2, "high": 3}
        selected_pet.add_task(
            Task(
                name=task_name.strip(),
                category=category.strip() or "general",
                duration=int(duration),
                priority=priority_map[priority_label],
                frequency=frequency,
                required_today=required_today,
            )
        )
        st.success(f"Added {task_name.strip()} to {selected_pet.name}.")
else:
    st.info("Add a pet before creating tasks.")

st.divider()

st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_daily_plan()

    if not plan:
        st.warning("No tasks fit within the available time today.")
    else:
        st.write("Planned tasks:")
        st.table(
            [
                {
                    "Task": task.name,
                    "Category": task.category,
                    "Duration": f"{task.duration} min",
                    "Priority": task.priority,
                }
                for task in plan
            ]
        )
        st.markdown(scheduler.explain_plan())
