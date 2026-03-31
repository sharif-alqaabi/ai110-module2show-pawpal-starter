from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: int
    frequency: str
    required_today: bool = True
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as finished."""
        pass

    def fits_schedule(self, available_time: int) -> bool:
        """Return whether the task can fit in the available time."""
        pass

    def describe_reason(self) -> str:
        """Explain why this task matters in the daily plan."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task_name: str) -> None:
        """Remove a task by name."""
        pass

    def list_upcoming_needs(self) -> List[Task]:
        """Return the tasks that still need attention."""
        pass


@dataclass
class Owner:
    name: str
    time_available: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, preferences: List[str]) -> None:
        """Update the owner's planning preferences."""
        pass

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        pass

    def view_today_plan(self) -> str:
        """Return a human-readable view of today's plan."""
        pass


@dataclass
class Scheduler:
    owner: Owner
    pets: List[Pet] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    available_time: Optional[int] = None

    def generate_daily_plan(self) -> List[Task]:
        """Build the final ordered plan for the day."""
        pass

    def sort_by_priority(self) -> List[Task]:
        """Sort tasks so the most important ones come first."""
        pass

    def filter_unfit_tasks(self) -> List[Task]:
        """Remove tasks that do not fit the current constraints."""
        pass

    def explain_plan(self) -> str:
        """Summarize why the scheduler chose this plan."""
        pass
