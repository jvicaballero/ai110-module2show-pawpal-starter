from datetime import time

from pawpal_system import Assignment, Employee, Pet, Task


def test_task_completion_updates_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False

    task.mark_completed()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    assert len(pet.get_tasks()) == 1


def test_creating_assignment_registers_with_employee():
    pet = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    employee = Employee(name="Alice")

    assignment = Assignment(
        employee=employee,
        pet=pet,
        task=task,
        start_time=time(8, 0),
        end_time=time(8, 30),
    )

    assert assignment in employee.get_assignments()
    assert len(employee.get_assignments()) == 1


def test_reassigning_moves_assignment_between_employees():
    pet = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    alice = Employee(name="Alice")
    bob = Employee(name="Bob")

    assignment = Assignment(
        employee=alice,
        pet=pet,
        task=task,
        start_time=time(8, 0),
        end_time=time(8, 30),
    )
    assert assignment in alice.get_assignments()

    bob.assign_task(assignment)

    assert assignment not in alice.get_assignments()
    assert assignment in bob.get_assignments()
    assert assignment.employee is bob
