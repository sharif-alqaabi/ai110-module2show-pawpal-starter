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
