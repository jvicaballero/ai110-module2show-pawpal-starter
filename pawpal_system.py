# Logic Layer, where backend classes will live

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

_PRIORITY_WEIGHT = {"low": 1, "medium": 2, "high": 3}


def _new_id() -> str:
    """Generate a short unique id string."""
    return uuid.uuid4().hex[:8]


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    frequency: str = "once"  # e.g. "once", "daily", "weekly"
    time_sensitive: bool = False
    completed: bool = False
    preferred_time: str | None = None  # "HH:MM", zero-padded 24h
    due_date: date | None = None
    id: str = field(default_factory=_new_id)

    _RECURRENCE_STEP = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}

    def mark_completed(self) -> None:
        """Flip this task's status to completed."""
        self.completed = True

    def get_effort_level(self) -> int:
        """Score effort as duration weighted by priority."""
        weight = _PRIORITY_WEIGHT.get(self.priority, 1)
        return self.duration_minutes * weight

    def next_occurrence(self) -> "Task | None":
        """Generate the next instance of a recurring task.

        Copies this task's fields into a brand-new, incomplete Task and advances
        due_date by one day ("daily") or seven days ("weekly").

        Returns:
            A new Task, or None if frequency is "once" (or unrecognized).
        """
        step = self._RECURRENCE_STEP.get(self.frequency)
        if step is None:
            return None
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            time_sensitive=self.time_sensitive,
            preferred_time=self.preferred_time,
            due_date=self.due_date + step if self.due_date else None,
        )


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    tasks: list[Task] = field(default_factory=list)
    id: str = field(default_factory=_new_id)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return a copy of all tasks for this pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> list[Task]:
        """Return tasks that are not yet completed."""
        return [task for task in self.tasks if not task.completed]

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task completed and roll it forward if it recurs.

        Lives on Pet rather than Task because spawning the next occurrence
        requires appending to this pet's task list, which Task has no reference to.

        Args:
            task: a task belonging to this pet (must already be in self.tasks
                to be picked up by future get_pending_tasks() calls).

        Returns:
            The newly created next-occurrence Task, or None if the task doesn't recur.
        """
        task.mark_completed()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)
    pickup_time: time | None = None
    total_cost: float = 0.0
    id: str = field(default_factory=_new_id)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pets."""
        self.pets.append(pet)

    def get_pickup_time(self) -> time | None:
        """Return the owner's scheduled pickup time."""
        return self.pickup_time

    def get_total_cost(self) -> float:
        """Return the total cost owed by this owner."""
        return self.total_cost

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair across all of this owner's pets."""
        return [(pet, task) for pet in self.pets for task in pet.get_tasks()]


@dataclass
class Assignment:
    employee: "Employee"
    pet: Pet
    task: Task
    start_time: time
    end_time: time

    def __post_init__(self) -> None:
        """Register this assignment with its employee on creation."""
        self.employee.assign_task(self)

    def get_duration(self) -> int:
        """Return the assignment's length in minutes."""
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return end_minutes - start_minutes


@dataclass
class Employee:
    name: str
    assignments: list[Assignment] = field(default_factory=list)
    id: str = field(default_factory=_new_id)

    def assign_task(self, assignment: Assignment) -> None:
        """Assign this employee to the given assignment, moving it from any prior employee."""
        previous_employee = assignment.employee
        if previous_employee is not self and assignment in previous_employee.assignments:
            previous_employee.assignments.remove(assignment)
        assignment.employee = self
        if assignment not in self.assignments:
            self.assignments.append(assignment)

    def get_assignments(self) -> list[Assignment]:
        """Return a copy of all assignments held by this employee."""
        return list(self.assignments)


@dataclass
class Schedule:
    day: date
    owner: Owner
    available_employees: list[Employee] = field(default_factory=list)
    assignments: list[Assignment] = field(default_factory=list)

    def add_assignment(self, assignment: Assignment) -> None:
        """Add an assignment to this day's schedule."""
        self.assignments.append(assignment)


@dataclass
class Scheduler:
    """The "brain": retrieves, organizes, and assigns tasks across an owner's pets."""

    owner: Owner
    employees: list[Employee] = field(default_factory=list)

    def get_pending_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair still incomplete across the owner's pets."""
        return [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.get_pending_tasks()
        ]

    def prioritize_tasks(
        self, pending: list[tuple[Pet, Task]]
    ) -> list[tuple[Pet, Task]]:
        """Order pending tasks for scheduling: time-sensitive tasks first, then by priority weight.

        Args:
            pending: (pet, task) pairs to order, e.g. from get_pending_tasks().

        Returns:
            A new list sorted with time_sensitive=True tasks first, ties broken by
            descending priority weight (high > medium > low). O(n log n).
        """
        return sorted(
            pending,
            key=lambda pair: (
                not pair[1].time_sensitive,
                -_PRIORITY_WEIGHT.get(pair[1].priority, 1),
            ),
        )

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter every (pet, task) pair by completion status and/or pet name.

        Args:
            completed: keep only tasks with this completed value; None means no filter.
            pet_name: keep only tasks belonging to the pet with this name; None means no filter.

        Returns:
            The (pet, task) pairs matching all filters given (an AND of whichever are set).
        """
        pairs = self.owner.get_all_tasks()
        if completed is not None:
            pairs = [pair for pair in pairs if pair[1].completed == completed]
        if pet_name is not None:
            pairs = [pair for pair in pairs if pair[0].name == pet_name]
        return pairs

    def sort_by_time(
        self, pending: list[tuple[Pet, Task]]
    ) -> list[tuple[Pet, Task]]:
        """Sort pending tasks by their preferred_time.

        "HH:MM" strings are zero-padded, so plain lexicographic sort order matches
        chronological order without parsing into datetime.time.

        Args:
            pending: (pet, task) pairs to order.

        Returns:
            A new list ordered earliest-preferred_time first; tasks with no
            preferred_time sort last.
        """
        return sorted(
            pending,
            key=lambda pair: pair[1].preferred_time or "99:99",
        )

    def build_schedule(self, day: date, start_time: time) -> Schedule:
        """Build a day's schedule using a greedy earliest-available-employee algorithm.

        Tasks are taken in prioritize_tasks() order; each is handed to whichever
        employee's clock is currently earliest, then that employee's clock advances
        by the task's duration. This only prevents double-booking an employee — it
        does not check whether the same pet ends up double-booked; use
        find_conflicts()/check_conflicts() on the result for that. O(n * m) for
        n tasks and m employees (a scan over employees per task).

        Args:
            day: the calendar day being scheduled.
            start_time: the time every employee's clock starts at.

        Returns:
            A Schedule with one Assignment per pending task, or an empty Schedule
            if there are no employees.
        """
        schedule = Schedule(day=day, owner=self.owner, available_employees=list(self.employees))
        if not self.employees:
            return schedule

        pending = self.prioritize_tasks(self.get_pending_tasks())
        next_available = {
            employee.id: datetime.combine(day, start_time) for employee in self.employees
        }

        for pet, task in pending:
            employee = min(self.employees, key=lambda e: next_available[e.id])
            clock = next_available[employee.id]
            end_clock = clock + timedelta(minutes=task.duration_minutes)

            assignment = Assignment(
                employee=employee,
                pet=pet,
                task=task,
                start_time=clock.time(),
                end_time=end_clock.time(),
            )
            schedule.add_assignment(assignment)
            next_available[employee.id] = end_clock

        return schedule

    @staticmethod
    def _times_overlap(start_a: time, end_a: time, start_b: time, end_b: time) -> bool:
        """Check whether two half-open time intervals [start_a, end_a) and [start_b, end_b) overlap.

        Returns:
            True if the intervals share any time, False otherwise.
        """
        return start_a < end_b and start_b < end_a

    def find_conflicts(self, schedule: Schedule) -> list[dict]:
        """Detect overlapping assignments that are actually impossible to carry out.

        Checks every pair of assignments (O(n^2) in the number of assignments) and
        flags a pair only when the overlap is a genuine impossibility: the same pet
        double-booked, or the same employee double-booked. Two different pets
        overlapping under two different employees is fine and is not flagged.

        Args:
            schedule: the built Schedule to inspect.

        Returns:
            A list of dicts, one per conflicting pair, each with keys "same_pet"
            (bool), "same_employee" (bool), and "assignments" (the two Assignment
            objects involved).
        """
        conflicts = []
        assignments = schedule.assignments
        for i, first in enumerate(assignments):
            for second in assignments[i + 1:]:
                same_pet = first.pet.id == second.pet.id
                same_employee = first.employee.id == second.employee.id
                if not (same_pet or same_employee):
                    continue
                if not self._times_overlap(
                    first.start_time, first.end_time, second.start_time, second.end_time
                ):
                    continue
                conflicts.append(
                    {
                        "same_pet": same_pet,
                        "same_employee": same_employee,
                        "assignments": (first, second),
                    }
                )
        return conflicts

    def check_conflicts(self, schedule: Schedule) -> str:
        """Run find_conflicts() and render the result as a human-readable message.

        Always returns a string rather than raising, so callers can display it
        as a warning without needing a try/except.

        Args:
            schedule: the built Schedule to inspect.

        Returns:
            "No scheduling conflicts detected." if there are none, otherwise a
            multi-line warning listing each conflicting pair and why.
        """
        conflicts = self.find_conflicts(schedule)
        if not conflicts:
            return "No scheduling conflicts detected."

        lines = ["Warning: scheduling conflicts detected:"]
        for conflict in conflicts:
            first, second = conflict["assignments"]
            reason = "same pet" if conflict["same_pet"] else "same employee"
            lines.append(
                f"  - '{first.task.title}' ({first.pet.name}, {first.employee.name}) "
                f"overlaps '{second.task.title}' ({second.pet.name}, {second.employee.name}) "
                f"[{reason}]"
            )
        return "\n".join(lines)

    def explain_schedule(self, schedule: Schedule) -> str:
        """Render a human-readable summary of a schedule's assignments."""
        if not schedule.assignments:
            return "No tasks scheduled."

        lines = []
        for assignment in schedule.assignments:
            lines.append(
                f"{assignment.start_time.strftime('%H:%M')} - "
                f"{assignment.task.title} for {assignment.pet.name} "
                f"({assignment.task.priority} priority) -> {assignment.employee.name}"
            )
        return "\n".join(lines)
