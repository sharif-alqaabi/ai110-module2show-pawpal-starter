import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

DATA_FILE = "data.json"

if "owner" not in st.session_state:
    st.session_state.owner = Owner.load_from_json(DATA_FILE)

owner = st.session_state.owner
scheduler = Scheduler(owner=owner)


def build_task_rows(tasks: list[Task]) -> list[dict[str, str | int | bool]]:
    return [
        {
            "Task": task.name,
            "Category": task.category,
            "Time": task.time,
            "Due Date": task.due_date.isoformat(),
            "Duration": f"{task.duration} min",
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Completed": task.completed,
        }
        for task in tasks
    ]


def persist_owner_data() -> None:
    owner.save_to_json(DATA_FILE)

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
    persist_owner_data()
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
        persist_owner_data()
        st.success(f"Added {pet_name.strip()} to {owner.name}'s household.")

st.subheader("Current Pets")
if owner.pets:
    for pet in owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species}, age {pet.age})")
        if pet.care_notes:
            st.caption(pet.care_notes)
        if pet.tasks:
            st.table(build_task_rows(scheduler.sort_by_time(pet.tasks)))
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
        task_time = st.text_input("Task time (HH:MM)", value="08:00")
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
                time=task_time.strip() or "09:00",
                required_today=required_today,
            )
        )
        persist_owner_data()
        st.success(f"Added {task_name.strip()} to {selected_pet.name}.")
else:
    st.info("Add a pet before creating tasks.")

st.divider()

st.subheader("Task Explorer")
if owner.pets and scheduler.tasks:
    filter_pet_name = st.selectbox(
        "Filter by pet",
        ["All pets"] + [pet.name for pet in owner.pets],
    )
    filter_status = st.selectbox(
        "Filter by status",
        ["Incomplete", "Completed", "All tasks"],
    )

    if filter_pet_name == "All pets":
        filtered_tasks = scheduler.sort_by_time()
    else:
        filtered_tasks = scheduler.sort_by_time(scheduler.filter_tasks_by_pet(filter_pet_name))

    if filter_status == "Incomplete":
        filtered_tasks = [task for task in filtered_tasks if not task.completed]
    elif filter_status == "Completed":
        filtered_tasks = [task for task in filtered_tasks if task.completed]

    if filtered_tasks:
        st.table(build_task_rows(filtered_tasks))
    else:
        st.info("No tasks match the selected filters.")
else:
    st.info("Add pets and tasks to explore sorted and filtered views.")

st.divider()

st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    plan = scheduler.generate_daily_plan()
    conflict_warnings = scheduler.detect_conflicts(plan)

    if not plan:
        st.warning("No tasks fit within the available time today.")
    else:
        st.success("Schedule generated successfully.")
        st.write("Planned tasks:")
        st.table(build_task_rows(plan))

        if conflict_warnings:
            for warning in conflict_warnings:
                st.warning(warning)
        else:
            st.success("No schedule conflicts detected.")

        st.info(scheduler.explain_plan())

st.caption(f"Data is automatically saved to `{DATA_FILE}`.")
