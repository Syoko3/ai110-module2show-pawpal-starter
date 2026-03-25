classDiagram
    class Owner {
        +String ownerId
        +String name
        +String email
        +String phone
        +String preferredScheduleTime
        +int dailyTimeAvailable
        +List~Pet~ pets
        +List~String~ preferences
        +addPet(pet: Pet) void
        +removePet(petId: String) void
        +updatePreferences(prefs: List~String~) void
        +getSchedule() Schedule
    }

    class Pet {
        +String petId
        +String name
        +String species
        +String breed
        +int age
        +String medicalNotes
        +List~Task~ tasks
        +Owner owner
        +addTask(task: Task) void
        +removeTask(taskId: String) void
        +updateInfo(field: String, value: String) void
        +getTasks() List~Task~
    }

    class Task {
        +String taskId
        +String title
        +String description
        +int duration
        +Priority priority
        +String frequency
        +String preferredTime
        +boolean isCompleted
        +Pet pet
        +markComplete() void
        +markIncomplete() void
        +edit(field: String, value: Object) void
        +getRemainingTime() int
    }

    class Scheduler {
        +String schedulerId
        +Owner owner
        +List~Task~ taskQueue
        +int totalTimeAvailable
        +Schedule generatedSchedule
        +generateSchedule() Schedule
        +prioritizeTasks() List~Task~
        +applyConstraints() List~Task~
        +explainReasoning() String
        +displayPlan() void
        +adjustSchedule(taskId: String) void
    }

    class Schedule {
        +String scheduleId
        +Date date
        +List~ScheduledTask~ scheduledTasks
        +String reasoningSummary
        +int totalDuration
        +addEntry(task: ScheduledTask) void
        +removeEntry(taskId: String) void
        +getSummary() String
    }

    class ScheduledTask {
        +Task task
        +String startTime
        +String endTime
        +String rationaleNote
    }

    class Priority {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
        CRITICAL
    }

    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "1" Owner : manages
    Scheduler "1" --> "1" Schedule : generates
    Schedule "1" --> "0..*" ScheduledTask : contains
    ScheduledTask "1" --> "1" Task : wraps
    Task --> Priority : uses