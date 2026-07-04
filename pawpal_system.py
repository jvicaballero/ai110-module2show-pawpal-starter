# Logic Layer, where backend classes will live

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    time_sensitive: bool = False
    completed: bool = False

    def mark_completed(self) -> None:
        pass

    def get_effort_level(self) -> int:
        pass


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)
    pickup_time: time | None = None
    total_cost: float = 0.0

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pickup_time(self) -> time:
        pass

    def get_total_cost(self) -> float:
        pass


@dataclass
class Assignment:
    employee: "Employee"
    pet: Pet
    task: Task
    start_time: time
    end_time: time

    def get_duration(self) -> int:
        pass


@dataclass
class Employee:
    name: str
    assignments: list[Assignment] = field(default_factory=list)

    def assign_task(self, assignment: Assignment) -> None:
        pass

    def get_assignments(self) -> list[Assignment]:
        pass


@dataclass
class Schedule:
    day: date
    assignments: list[Assignment] = field(default_factory=list)

    def add_assignment(self, assignment: Assignment) -> None:
        pass

    def generate_plan(self) -> list[Assignment]:
        pass

    def explain_plan(self) -> str:
        pass
