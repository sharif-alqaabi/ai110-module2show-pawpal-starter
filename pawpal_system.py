from __future__ import annotations

from datetime import date, timedelta
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: int
    frequency: str
    time: str = "09:00"
    due_date: date = field(default_factory=date.today)
    required_today: bool = True
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as finished."""
        self.completed = True

    def is_due_today(self, reference_date: date | None = None) -> bool:
        """Return whether the task should be scheduled on the reference date."""
        current_date = reference_date or date.today()
        return self.required_today and self.due_date <= current_date

    def next_due_date(self) -> date | None:
        """Return the next due date for recurring tasks."""
        normalized_frequency = self.frequency.lower()
        if normalized_frequency == "daily":
            return self.due_date + timedelta(days=1)
        if normalized_frequency == "weekly":
            return self.due_date + timedelta(weeks=1)
        return None

    def create_next_occurrence(self) -> Task | None:
        """Create the next recurring task instance when applicable."""
        next_due = self.next_due_date()
        if next_due is None:
            return None

        return Task(
            name=self.name,
            category=self.category,
            duration=self.duration,
            priority=self.priority,
            frequency=self.frequency,
            time=self.time,
            due_date=next_due,
            required_today=next_due <= date.today(),
        )

    def fits_schedule(self, available_time: int) -> bool:
        """Return whether the task can fit in the available time."""
        return self.is_due_today() and not self.completed and self.duration <= available_time

    def describe_reason(self) -> str:
        """Explain why this task matters in the daily plan."""
        reason = f"{self.name} is a {self.category} task"
        reason += f" with priority {self.priority}"
        if self.required_today:
            reason += " and it is needed today"
        return reason + "."


@dataclass
class Pet:
    name: str
    species: str
    age: int
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove a task by name."""
        self.tasks = [task for task in self.tasks if task.name != task_name]

    def list_upcoming_needs(self) -> List[Task]:
        """Return the tasks that still need attention."""
        return [
            task
            for task in self.tasks
            if task.is_due_today() and not task.completed
        ]

    def mark_task_complete(self, task_name: str) -> Task | None:
        """Complete a task and create its next recurring instance if needed."""
        for task in self.tasks:
            if task.name == task_name and not task.completed:
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    self.tasks.append(next_task)
                return next_task
        return None


@dataclass
class Owner:
    name: str
    time_available: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, preferences: List[str]) -> None:
        """Update the owner's planning preferences."""
        self.preferences = preferences

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet owned by this person."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def view_today_plan(self) -> str:
        """Return a human-readable view of today's plan."""
        upcoming_tasks = [
            task for task in self.get_all_tasks() if task.is_due_today() and not task.completed
        ]
        if not upcoming_tasks:
            return f"{self.name} has no remaining pet care tasks for today."

        task_names = ", ".join(task.name for task in upcoming_tasks)
        return f"Today's remaining tasks for {self.name}: {task_names}."


@dataclass
class Scheduler:
    owner: Owner
    available_time: int = 0

    @property
    def pets(self) -> List[Pet]:
        """Return the pets managed by the scheduler through the owner."""
        return self.owner.pets

    @property
    def tasks(self) -> List[Task]:
        """Flatten all pet tasks into a single list for scheduling."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_available_time(self) -> int:
        """Return the scheduler's available time, falling back to the owner's time."""
        return self.available_time or self.owner.time_available

    def generate_daily_plan(self) -> List[Task]:
        """Build the final ordered plan for the day."""
        fitting_tasks = self.filter_unfit_tasks()
        prioritized_tasks = self.sort_by_priority(fitting_tasks)
        return self.sort_by_time(prioritized_tasks)

    def sort_by_priority(self, tasks: List[Task] | None = None) -> List[Task]:
        """Sort tasks so the most important ones come first."""
        task_list = tasks if tasks is not None else self.tasks
        return sorted(
            task_list,
            key=lambda task: (-task.priority, task.duration, task.name.lower()),
        )

    def sort_by_time(self, tasks: List[Task] | None = None) -> List[Task]:
        """Sort tasks by their HH:MM time value."""
        task_list = tasks if tasks is not None else self.tasks
        return sorted(
            task_list,
            key=lambda task: tuple(int(part) for part in task.time.split(":")),
        )

    def filter_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return tasks that match the requested completion status."""
        return [task for task in self.tasks if task.completed is completed]

    def filter_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks for the named pet."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.tasks
        return []

    def mark_task_complete(self, pet_name: str, task_name: str) -> Task | None:
        """Complete a pet task and create its next recurring occurrence when needed."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.mark_task_complete(task_name)
        return None

    def detect_conflicts(self, tasks: List[Task] | None = None) -> List[str]:
        """Return warning messages for tasks that share the same scheduled time."""
        task_list = self.sort_by_time(tasks if tasks is not None else self.tasks)
        warnings: List[str] = []

        for index, current_task in enumerate(task_list):
            for other_task in task_list[index + 1 :]:
                if current_task.time != other_task.time:
                    continue

                warnings.append(
                    "Conflict detected: "
                    f"'{current_task.name}' and '{other_task.name}' are both scheduled for "
                    f"{current_task.time}."
                )

        return warnings

    def filter_unfit_tasks(self) -> List[Task]:
        """Remove tasks that do not fit the current constraints."""
        remaining_time = self.get_available_time()
        selected_tasks: List[Task] = []

        for task in self.sort_by_priority():
            if task.fits_schedule(remaining_time):
                selected_tasks.append(task)
                remaining_time -= task.duration

        return selected_tasks

    def explain_plan(self) -> str:
        """Summarize why the scheduler chose this plan."""
        plan = self.generate_daily_plan()
        if not plan:
            return "No tasks fit within the available time today."

        lines = ["Today's plan:"]
        for task in plan:
            lines.append(
                f"- {task.time} | {task.name} ({task.duration} min): {task.describe_reason()}"
            )

        unused_time = self.get_available_time() - sum(task.duration for task in plan)
        lines.append(f"Unused time remaining: {unused_time} minutes.")
        for warning in self.detect_conflicts(plan):
            lines.append(f"Warning: {warning}")
        return "\n".join(lines)
