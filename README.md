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

## ✨ Features

- **Priority-aware ordering** — time-sensitive tasks are scheduled first, then ranked by priority weight (high > medium > low), so urgent care never gets bumped by something lower-stakes.
- **Sorting by time** — tasks line up chronologically by their preferred "HH:MM" time; tasks with no preferred time sort to the end instead of cluttering the top.
- **Filtering by pet or status** — narrow the task list down to a single pet, or to just pending/completed tasks, without writing a new query each time.
- **Conflict warnings** — after a schedule is built, it's checked for double-bookings (the same pet or the same employee assigned to overlapping tasks) and a plain-language warning is surfaced instead of silently producing a broken plan.
- **Daily/weekly recurrence** — marking a recurring task complete automatically creates its next occurrence, with the due date rolled forward, so daily walks and weekly groomings never have to be re-entered by hand.

## 📐 Smarter Scheduling

| Feature           | Method(s)                                          | Notes                                                                                                                     |
| ------------------ | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Task sorting      | `Scheduler.sort_by_time()`, `Scheduler.prioritize_tasks()` | `sort_by_time()` orders `(pet, task)` pairs by `Task.preferred_time` ("HH:MM" strings sort correctly without parsing since they're zero-padded); untimed tasks sort last. `prioritize_tasks()` orders tasks time-sensitive first, then by priority weight (high > medium > low), and feeds the result into `build_schedule()`. |
| Filtering         | `Scheduler.filter_tasks()`                         | Filters `(pet, task)` pairs by completion status (`completed=True/False`) and/or pet name (`pet_name="Mochi"`). Both filters are optional and combine with AND when both are given. |
| Conflict handling | `Scheduler.find_conflicts()`, `Scheduler.check_conflicts()`, `Scheduler._times_overlap()` | `find_conflicts()` scans a built `Schedule` for assignment pairs that overlap in time **and** are actually impossible to carry out — same pet double-booked, or same employee double-booked. (Two different pets handled by two different employees at the same time is fine and isn't flagged.) `check_conflicts()` wraps this into a plain warning string ("No scheduling conflicts detected." or a bulleted list) so callers never need a try/except. |
| Recurring tasks   | `Task.next_occurrence()`, `Pet.complete_task()`    | `Task.next_occurrence()` returns a fresh, incomplete copy of a `"daily"` or `"weekly"` task with `due_date` advanced by 1 or 7 days (returns `None` for `"once"`). `Pet.complete_task()` is the orchestration point: it marks the task complete and, if it recurs, appends the new occurrence to the pet's task list automatically. |

## 📸 Demo Walkthrough

### UI features

The Streamlit app (`app.py`) lets a user:

- Set the **owner's name** and add one or more **pets** (name, breed, species).
- Add **care tasks** to a selected pet — title, duration, priority, an optional preferred time, an optional recurrence (`once`/`daily`/`weekly`), and whether it's time-sensitive.
- **Filter and view tasks** by pet and by completion status, sorted chronologically by preferred time.
- **Generate a daily schedule** with one click, which assigns every pending task to a staff member and displays the resulting timeline as a table.
- See a **conflict warning or success banner** immediately below the schedule, so a double-booked pet or employee is impossible to miss.

### Example workflow

1. Add an owner (e.g. "Jordan") and a pet (e.g. "Mochi").
2. Add a couple of care tasks for Mochi — say, a high-priority "Morning walk" at `07:00` and a "Grooming" session, both time-sensitive.
3. Open the **Tasks** section to see them sorted by preferred time and filtered by pet/status.
4. Click **Generate schedule** to build today's plan — the app assigns each task to whichever employee (e.g. Alice or Bob) is free soonest.
5. Review the schedule table and the warning/success banner underneath it before finalizing the day's plan.

### Key Scheduler behaviors shown

- **Sorting** — `Scheduler.sort_by_time()` orders tasks chronologically by preferred time; `Scheduler.prioritize_tasks()` puts time-sensitive, high-priority tasks first when the schedule is actually built.
- **Filtering** — `Scheduler.filter_tasks()` narrows the task list by pet name and/or completion status.
- **Conflict warnings** — `Scheduler.find_conflicts()` / `Scheduler.check_conflicts()` detect when the greedy scheduler has double-booked a pet (two employees assigned to the same pet at overlapping times) or an employee, and surface it as a warning rather than failing silently.
- **Recurrence** — completing a `"daily"` or `"weekly"` task via `Pet.complete_task()` automatically creates its next occurrence.

### Sample CLI output (`python main.py`)

`main.py` exercises the same Scheduler methods outside the UI — useful for quickly checking behavior from the terminal:

```
Today's Schedule
========================================
08:00 - Evening walk for Mochi (high priority) -> Alice
08:00 - Morning walk for Mochi (high priority) -> Bob
08:30 - Litter box cleaning for Biscuit (medium priority) -> Alice

Assignment Details
========================================
Evening walk | Mochi | Alice | 08:00-08:30 (30 min)
Morning walk | Mochi | Bob | 08:00-08:30 (30 min)
Litter box cleaning | Biscuit | Alice | 08:30-08:45 (15 min)

Employee Workload
========================================
Alice: 2 task(s), 45 min total
Bob: 1 task(s), 30 min total

Tasks Sorted by Preferred Time
========================================
07:00 | Morning walk (Mochi)
09:00 | Litter box cleaning (Biscuit)
12:30 | Feeding (Mochi)
18:00 | Evening walk (Mochi)

Pending Tasks (filter by completion status)
========================================
Evening walk (Mochi)
Morning walk (Mochi)
Litter box cleaning (Biscuit)

Mochi's Tasks (filter by pet name)
========================================
Evening walk | completed=False
Morning walk | completed=False
Feeding | completed=True

Conflict Check
========================================
Warning: scheduling conflicts detected:
  - 'Evening walk' (Mochi, Alice) overlaps 'Morning walk' (Mochi, Bob) [same pet]
```

Note the conflict warning at the bottom: Mochi's evening and morning walks were both assigned to the `08:00` slot across two different employees, which `check_conflicts()` correctly flags as a same-pet double-booking — exactly the scenario `build_schedule()`'s greedy, employee-only algorithm doesn't prevent on its own.

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
