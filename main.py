# Testing Ground to verify logic

from datetime import date, time

from pawpal_system import Assignment, Employee, Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", breed="Shiba Inu", species="dog")
    mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time_sensitive=True))
    mochi.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    biscuit = Pet(name="Biscuit", breed="Tabby", species="cat")
    biscuit.add_task(Task(title="Litter box cleaning", duration_minutes=15, priority="medium"))

    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    employees = [Employee(name="Alice"), Employee(name="Bob")]
    scheduler = Scheduler(owner=owner, employees=employees)

    todays_plan = scheduler.build_schedule(day=date.today(), start_time=time(8, 0))

    print("Today's Schedule")
    print("=" * 40)
    print(scheduler.explain_schedule(todays_plan))

    print()
    print("Assignment Details")
    print("=" * 40)
    assignment: Assignment
    for assignment in todays_plan.assignments:
        print(
            f"{assignment.task.title} | {assignment.pet.name} | "
            f"{assignment.employee.name} | "
            f"{assignment.start_time.strftime('%H:%M')}-{assignment.end_time.strftime('%H:%M')} "
            f"({assignment.get_duration()} min)"
        )

    print()
    print("Employee Workload")
    print("=" * 40)
    for employee in employees:
        total_minutes = sum(a.get_duration() for a in employee.get_assignments())
        print(f"{employee.name}: {len(employee.get_assignments())} task(s), {total_minutes} min total")


if __name__ == "__main__":
    main()
