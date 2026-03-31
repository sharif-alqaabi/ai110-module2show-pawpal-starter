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
        )
    )
    mochi.add_task(
        Task(
            name="Breakfast",
            category="feeding",
            duration=10,
            priority=4,
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            name="Medication",
            category="health",
            duration=5,
            priority=5,
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            name="Litter cleanup",
            category="hygiene",
            duration=10,
            priority=2,
            frequency="daily",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    return Scheduler(owner=owner)


def print_schedule(scheduler: Scheduler) -> None:
    plan = scheduler.generate_daily_plan()

    print("Today's Schedule")
    print("=" * 16)

    if not plan:
        print("No tasks fit in the available time today.")
        return

    for index, task in enumerate(plan, start=1):
        print(
            f"{index}. {task.name} | category: {task.category} | "
            f"duration: {task.duration} min | priority: {task.priority}"
        )

    print()
    print(scheduler.explain_plan())


if __name__ == "__main__":
    demo_scheduler = build_demo_data()
    print_schedule(demo_scheduler)
