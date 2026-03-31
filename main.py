from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_data() -> Scheduler:
    owner = Owner(name="Jordan", time_available=60, preferences=["prioritize health"])

    mochi = Pet(name="Mochi", species="dog", age=3, care_notes="Needs daily exercise.")
    luna = Pet(name="Luna", species="cat", age=5, care_notes="Prefers calm mornings.")

    mochi.add_task(
        Task(
            name="Morning walk",
            category="exercise",
            duration=20,
            priority=3,
            frequency="daily",
            time="08:30",
        )
    )
    mochi.add_task(
        Task(
            name="Breakfast",
            category="feeding",
            duration=10,
            priority=4,
            frequency="daily",
            time="07:45",
        )
    )
    luna.add_task(
        Task(
            name="Medication",
            category="health",
            duration=5,
            priority=5,
            frequency="daily",
            time="07:15",
        )
    )
    luna.add_task(
        Task(
            name="Litter cleanup",
            category="hygiene",
            duration=10,
            priority=2,
            frequency="daily",
            time="09:00",
        )
    )
    mochi.add_task(
        Task(
            name="Evening play",
            category="enrichment",
            duration=15,
            priority=2,
            frequency="daily",
            time="18:00",
        )
    )
    luna.add_task(
        Task(
            name="Breakfast refill",
            category="feeding",
            duration=10,
            priority=3,
            frequency="daily",
            time="08:30",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)
    mochi.tasks[1].mark_complete()

    return Scheduler(owner=owner)


def print_schedule(scheduler: Scheduler) -> None:
    plan = scheduler.generate_daily_plan()
    mochi_tasks = scheduler.filter_tasks_by_pet("Mochi")
    incomplete_tasks = scheduler.filter_tasks_by_status(False)
    tasks_by_time = scheduler.sort_by_time()
    conflict_warnings = scheduler.detect_conflicts()
    next_medication = scheduler.mark_task_complete("Luna", "Medication")

    print("Today's Schedule")
    print("=" * 16)

    if not plan:
        print("No tasks fit in the available time today.")
        return

    for index, task in enumerate(plan, start=1):
        print(
            f"{index}. {task.time} | {task.name} | category: {task.category} | "
            f"duration: {task.duration} min | priority: {task.priority}"
        )

    print()
    print("Tasks Sorted by Time")
    print("=" * 20)
    for task in tasks_by_time:
        print(f"- {task.time} | {task.name}")

    print()
    print("Conflict Warnings")
    print("=" * 17)
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"- {warning}")
    else:
        print("No scheduling conflicts found.")

    print()
    print("Incomplete Tasks")
    print("=" * 16)
    for task in incomplete_tasks:
        print(f"- {task.name} ({task.time})")

    print()
    print("Mochi's Tasks")
    print("=" * 12)
    for task in mochi_tasks:
        status = "done" if task.completed else "todo"
        print(f"- {task.name} [{status}]")

    print()
    print("Recurring Task Check")
    print("=" * 20)
    if next_medication is not None:
        print(
            "Medication completed. "
            f"Next occurrence is due on {next_medication.due_date.isoformat()}."
        )
    else:
        print("No recurring task was generated.")

    print()
    print(scheduler.explain_plan())


if __name__ == "__main__":
    demo_scheduler = build_demo_data()
    print_schedule(demo_scheduler)
