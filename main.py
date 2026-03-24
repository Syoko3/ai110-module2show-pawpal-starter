from pawpal_system import Priority, ScheduledTask, Schedule
from pawpal_system import Task, Pet, Owner, ScheduleAdjustment, Scheduler
import uuid

def run_test():
    # ✅ Fix 1: daily_time_available is an int (minutes), not a string
    owner = Owner(str(uuid.uuid4()), "Sohdai", "sohdai@gmail.com", "123-456-7890", "morning", 120)

    # ✅ Fix 2: Pet signature is (pet_id, name, species, breed, age) — owner set via add_pet()
    dog = Pet(str(uuid.uuid4()), "Dog", "Canine", "Labrador", 5)
    cat = Pet(str(uuid.uuid4()), "Cat", "Feline", "Siamese", 3)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Tasks with varying priorities and preferred times
    task1 = Task("T1", "Feed the dog",          "Care",     10, Priority.HIGH,   "daily",  "morning")
    task2 = Task("T2", "Play with the cat",      "Playing",  30, Priority.MEDIUM, "weekly", "morning")
    task3 = Task("T3", "Take the dog for a walk","Exercise", 60, Priority.HIGH,   "weekly", "afternoon")

    dog.add_task(task1)
    cat.add_task(task2)
    dog.add_task(task3)

    # Generate and display the schedule
    scheduler = Scheduler(str(uuid.uuid4()), owner)
    scheduler.generate_schedule()

    print("Today's Schedule:")
    scheduler.display_plan()
    print(scheduler.explain_reasoning())

if __name__ == "__main__":
    run_test()