from datetime import date, time

from pawpal_system import Assignment, Employee, Owner, Pet, Scheduler, Task


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


def test_sort_by_time_orders_earliest_first_and_untimed_last():
    pet = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    pet.add_task(Task(title="Evening walk", duration_minutes=30, priority="high", preferred_time="18:00"))
    pet.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", preferred_time="07:00"))
    pet.add_task(Task(title="Whenever", duration_minutes=10, priority="low"))
    owner = Owner(name="Jordan")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    ordered = scheduler.sort_by_time(owner.get_all_tasks())

    assert [task.title for _, task in ordered] == ["Morning walk", "Evening walk", "Whenever"]


def test_filter_tasks_by_completion_status_and_pet_name():
    mochi = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    luna = Pet(name="Luna", breed="Tabby", species="cat")
    walk = Task(title="Walk", duration_minutes=20, priority="high")
    feeding = Task(title="Feeding", duration_minutes=5, priority="low")
    feeding.mark_completed()
    mochi.add_task(walk)
    mochi.add_task(feeding)
    luna.add_task(Task(title="Litter box", duration_minutes=5, priority="medium"))
    owner = Owner(name="Jordan")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner)

    pending = scheduler.filter_tasks(completed=False)
    assert {task.title for _, task in pending} == {"Walk", "Litter box"}

    mochis_tasks = scheduler.filter_tasks(pet_name="Mochi")
    assert {task.title for _, task in mochis_tasks} == {"Walk", "Feeding"}

    mochis_pending = scheduler.filter_tasks(completed=False, pet_name="Mochi")
    assert [task.title for _, task in mochis_pending] == ["Walk"]


def test_find_conflicts_flags_same_pet_double_booking():
    pet = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high", time_sensitive=True))
    pet.add_task(Task(title="Grooming", duration_minutes=30, priority="high", time_sensitive=True))
    owner = Owner(name="Jordan")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner, employees=[Employee(name="Alice"), Employee(name="Bob")])

    schedule = scheduler.build_schedule(day=date(2026, 7, 4), start_time=time(8, 0))
    conflicts = scheduler.find_conflicts(schedule)

    assert len(conflicts) == 1
    assert conflicts[0]["same_pet"] is True
    assert "Warning" in scheduler.check_conflicts(schedule)


def test_check_conflicts_reports_clean_schedule():
    pet = Pet(name="Biscuit", breed="Tabby", species="cat")
    pet.add_task(Task(title="Litter box", duration_minutes=15, priority="medium"))
    owner = Owner(name="Sam")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner, employees=[Employee(name="Alice")])

    schedule = scheduler.build_schedule(day=date(2026, 7, 4), start_time=time(8, 0))

    assert scheduler.find_conflicts(schedule) == []
    assert scheduler.check_conflicts(schedule) == "No scheduling conflicts detected."


def test_completing_daily_task_creates_next_occurrence():
    pet = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    walk = Task(title="Morning walk", duration_minutes=30, priority="high", frequency="daily", due_date=date(2026, 7, 4))
    pet.add_task(walk)

    next_walk = pet.complete_task(walk)

    assert walk.completed is True
    assert next_walk is not None
    assert next_walk.completed is False
    assert next_walk.due_date == date(2026, 7, 5)
    assert next_walk in pet.get_tasks()


def test_completing_once_task_creates_no_next_occurrence():
    pet = Pet(name="Biscuit", breed="Tabby", species="cat")
    vet_visit = Task(title="Vet visit", duration_minutes=60, priority="high")
    pet.add_task(vet_visit)

    next_task = pet.complete_task(vet_visit)

    assert vet_visit.completed is True
    assert next_task is None
    assert len(pet.get_tasks()) == 1
