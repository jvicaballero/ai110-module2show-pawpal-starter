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
    id: str = field(default_factory=_new_id)

    def mark_completed(self) -> None:
        """Flip this task's status to completed."""
        self.completed = True

    def get_effort_level(self) -> int:
        """Score effort as duration weighted by priority."""
        weight = _PRIORITY_WEIGHT.get(self.priority, 1)
        return self.duration_minutes * weight


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
        """Sort pending tasks: time-sensitive first, then by priority weight."""
        return sorted(
            pending,
            key=lambda pair: (
                not pair[1].time_sensitive,
                -_PRIORITY_WEIGHT.get(pair[1].priority, 1),
            ),
        )

    def build_schedule(self, day: date, start_time: time) -> Schedule:
        """Greedily assign prioritized tasks to whichever employee is free soonest."""
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
