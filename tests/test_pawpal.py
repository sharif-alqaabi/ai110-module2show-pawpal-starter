from datetime import date, timedelta

from pawpal_system import Pet, Task


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
