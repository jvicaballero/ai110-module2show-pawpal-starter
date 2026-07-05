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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...



Today's Schedule
========================================
08:00 - Morning walk for Mochi (high priority) -> Alice
08:00 - Feeding for Mochi (high priority) -> Bob
08:10 - Litter box cleaning for Biscuit (medium priority) -> Bob

Assignment Details
========================================
Morning walk | Mochi | Alice | 08:00-08:30 (30 min)
Feeding | Mochi | Bob | 08:00-08:10 (10 min)
Litter box cleaning | Biscuit | Bob | 08:10-08:25 (15 min)

```

## 🧪 Testing PawPal+

```bash
python -m pytest -v
```

The suite in `tests/test_pawpal.py` covers:

- **Core model behavior** — marking a task completed, adding a task to a pet, an `Assignment` registering itself with its `Employee`, and reassigning an `Assignment` between employees.
- **Sorting** — `sort_by_time()` orders tasks earliest-preferred-time-first and pushes untimed tasks to the end.
- **Filtering** — `filter_tasks()` correctly narrows by completion status, by pet name, and by both combined.
- **Conflict detection** — `find_conflicts()`/`check_conflicts()` catch a same-pet double-booking produced by `build_schedule()`, and report a clean schedule with no false positives.
- **Recurring tasks** — completing a `"daily"` task via `Pet.complete_task()` spawns a new incomplete occurrence with `due_date` advanced by one day, while completing a `"once"` task spawns nothing.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\jvica\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: d:\codepathprojectsfin\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collecting ... collected 10 items

tests/test_pawpal.py::test_task_completion_updates_status PASSED         [ 10%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 20%]
tests/test_pawpal.py::test_creating_assignment_registers_with_employee PASSED [ 30%]
tests/test_pawpal.py::test_reassigning_moves_assignment_between_employees PASSED [ 40%]
tests/test_pawpal.py::test_sort_by_time_orders_earliest_first_and_untimed_last PASSED [ 50%]
tests/test_pawpal.py::test_filter_tasks_by_completion_status_and_pet_name PASSED [ 60%]
tests/test_pawpal.py::test_find_conflicts_flags_same_pet_double_booking PASSED [ 70%]
tests/test_pawpal.py::test_check_conflicts_reports_clean_schedule PASSED [ 80%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_occurrence PASSED [ 90%]
tests/test_pawpal.py::test_completing_once_task_creates_no_next_occurrence PASSED [100%]

============================= 10 passed in 0.04s ==============================
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — the core scheduling logic (sorting, filtering, conflict detection, recurrence) is well covered and passing, but `build_schedule()`'s greedy assignment algorithm itself and edge cases like zero employees, weekly recurrence, and multi-owner scenarios don't yet have dedicated tests, so a 5th star awaits broader coverage.

## 📐 Smarter Scheduling

| Feature           | Method(s)                                          | Notes                                                                                                                     |
| ------------------ | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Task sorting      | `Scheduler.sort_by_time()`, `Scheduler.prioritize_tasks()` | `sort_by_time()` orders `(pet, task)` pairs by `Task.preferred_time` ("HH:MM" strings sort correctly without parsing since they're zero-padded); untimed tasks sort last. `prioritize_tasks()` orders tasks time-sensitive first, then by priority weight (high > medium > low), and feeds the result into `build_schedule()`. |
| Filtering         | `Scheduler.filter_tasks()`                         | Filters `(pet, task)` pairs by completion status (`completed=True/False`) and/or pet name (`pet_name="Mochi"`). Both filters are optional and combine with AND when both are given. |
| Conflict handling | `Scheduler.find_conflicts()`, `Scheduler.check_conflicts()`, `Scheduler._times_overlap()` | `find_conflicts()` scans a built `Schedule` for assignment pairs that overlap in time **and** are actually impossible to carry out — same pet double-booked, or same employee double-booked. (Two different pets handled by two different employees at the same time is fine and isn't flagged.) `check_conflicts()` wraps this into a plain warning string ("No scheduling conflicts detected." or a bulleted list) so callers never need a try/except. |
| Recurring tasks   | `Task.next_occurrence()`, `Pet.complete_task()`    | `Task.next_occurrence()` returns a fresh, incomplete copy of a `"daily"` or `"weekly"` task with `due_date` advanced by 1 or 7 days (returns `None` for `"once"`). `Pet.complete_task()` is the orchestration point: it marks the task complete and, if it recurs, appends the new occurrence to the pet's task list automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
