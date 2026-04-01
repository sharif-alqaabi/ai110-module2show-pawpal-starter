# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- Owner and pet management for storing household care information.
- Task creation with category, duration, priority, frequency, due date, and scheduled `HH:MM` time.
- Time-based scheduling that sorts tasks chronologically for a cleaner daily plan.
- Filtering tools that let the app show tasks by pet or by completion status.
- Daily and weekly recurrence support that automatically creates the next task occurrence after completion.
- Conflict warnings that alert the owner when two tasks share the same scheduled time.
- JSON persistence so pets and tasks can be restored from `data.json` between app runs.
- Streamlit UI views for task tables, filtered task exploration, and schedule explanations.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ now includes a smarter scheduling layer beyond the original starter logic.

- Tasks can be sorted by scheduled time in `HH:MM` format.
- Tasks can be filtered by pet name or completion status.
- Daily and weekly recurring tasks automatically generate the next occurrence when completed.
- The scheduler can detect lightweight schedule conflicts and return warnings instead of crashing.

## Optional Extension: Persistence

PawPal+ now supports saving and loading owner, pet, and task data through a custom JSON serialization layer. I used an agent-style workflow to break this into two steps: first adding `save_to_json()` and `load_from_json()` in the backend, then updating the Streamlit session state to load saved data on startup and save changes after user actions.

## Testing PawPal+

Run the automated tests with:

```bash
python -m pytest
```

The current test suite covers task completion, adding tasks to pets, chronological sorting, recurring daily task creation, and conflict detection for duplicate task times.

Confidence Level: 4/5 stars. The core backend behaviors are covered by passing automated tests, but I would still want more edge-case and UI-level tests before calling the whole system fully production-ready.

## 📸 Demo

<img width="2672" height="1522" alt="PawPal+" src="https://github.com/user-attachments/assets/9e5ca950-c694-42cc-859a-03820c4f5d8f" />


