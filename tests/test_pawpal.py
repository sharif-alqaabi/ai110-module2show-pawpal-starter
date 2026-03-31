from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_task_status() -> None:
    task = Task(
        name="Medication",
        category="health",
        duration=5,
        priority=5,
        frequency="daily",
    )

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(
        name="Morning walk",
        category="exercise",
        duration=20,
        priority=3,
        frequency="daily",
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_mark_task_complete_creates_next_daily_occurrence() -> None:
    pet = Pet(name="Luna", species="cat", age=5)
    task = Task(
        name="Medication",
        category="health",
        duration=5,
        priority=5,
        frequency="daily",
        due_date=date.today(),
    )
    pet.add_task(task)

    next_task = pet.mark_task_complete("Medication")

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_sort_by_time_returns_tasks_in_chronological_order() -> None:
    owner = Owner(name="Jordan", time_available=60)
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(
        Task(
            name="Morning walk",
            category="exercise",
            duration=20,
            priority=3,
            frequency="daily",
            time="08:30",
        )
    )
    pet.add_task(
        Task(
            name="Breakfast",
            category="feeding",
            duration=10,
            priority=4,
            frequency="daily",
            time="07:45",
        )
    )
    pet.add_task(
        Task(
            name="Medication",
            category="health",
            duration=5,
            priority=5,
            frequency="daily",
            time="07:15",
        )
    )
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    sorted_tasks = scheduler.sort_by_time()

    assert [task.name for task in sorted_tasks] == [
        "Medication",
        "Breakfast",
        "Morning walk",
    ]


def test_detect_conflicts_flags_duplicate_task_times() -> None:
    owner = Owner(name="Jordan", time_available=60)
    pet = Pet(name="Luna", species="cat", age=5)
    pet.add_task(
        Task(
            name="Medication",
            category="health",
            duration=5,
            priority=5,
            frequency="daily",
            time="08:30",
        )
    )
    pet.add_task(
        Task(
            name="Breakfast refill",
            category="feeding",
            duration=10,
            priority=3,
            frequency="daily",
            time="08:30",
        )
    )
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:30" in warnings[0]
    assert "Medication" in warnings[0]
    assert "Breakfast refill" in warnings[0]
