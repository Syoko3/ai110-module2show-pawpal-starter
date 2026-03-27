# PawPal+ Project Reflection

## 1. System Design

--- Track pet care tasks, consider constraints, produce a daily plan

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

--- My initial UML design shows the relationship of the classes. Owner owns the Pet, Pet has the Task, Scheduler manages the Owner and generates the Schedule, Schedule contains ScheduledTask that wraps the Task, and Task uses the Priority to sort the tasks based on the priority.
--- I included Owner, Pet, Task, Scheduler, Schedule, ScheduledTask, and Priority. Owner class holds personal info and scheduling preferences. Pet class is linked back to its Owner and carries its own list of tasks. Task class contains required duration and priority, with frequency, preferredTime, and whether it is completed or not for tracking. Scheduler class pulls in the Owner's constraints and generates the plan. It also explains the reasoning of the plan to surface the logic behind the generated schedule. Schedule class holds the ordered list of scheduled items and a reasoningSummary string. ScheduledTask class wraps a Task with startTime, endTime, and rationalNote for explanation that why it was placed there. Priority class is the enumeration to keep comparisons consistent. It contains LOW, MEDIUM, HIGH, and CRITICAL.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

--- My design changed during implementation. I added Scheduler.load_tasks() to collect the tasks from Owner --> Pet --> Task into the task_queue because the scheduler needs to collect all tasks into one list before any scheduling work. I also added add_entry() to avoid any other tasks to be scheduled at the same time as the current task.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

--- My scheduler considers the priority first, then considers the time. I decided that priority mattered the most because pet care involves some health tasks, which they need to be finished first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

--- One tradeoff my scheduler makes is building the next task occurrence for recurring tasks and attaching it to the same pet. This tradeoff is reasonable for this scenario because the app is a lightweight pet care app, and this version has better readability and has less repeated logic.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

--- I used the AI tools during this project for designing the UML diagram, refactoring the logic to the other files, and debugging such as adding task completion status. The prompts or questions that were most helpful were creating a UML design based on brainstormed attributes and methods, and asking for some edge cases to generate some pytest tests based on these cases.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

--- I did not accept an AI suggestion as-is for fixing the time conflict issue before adding the requesting time from the user. I evaluated by checking the logic in the detect_time_conflicts() tests in test_pawpal.py and testing the UI. I verified the AI suggestion by adding the requesting time for each task, so that the user can assign the task with their requested time.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

--- I tested on the task completion status, task addition, filtering tasks, daily and weekly tasks, sorting tasks, and time conflicts. These tests were important because the completed tasks should be moved to the list of completed tasks, and the length of the task list should be increased by 1 after adding the tasks. Filtering tasks should return the tasks with same completion status, and daily and weekly tasks should create a new incomplete task due tomorrow or next week. Sorting the tasks based on time was important because it can generate the sorted schedule based on the time. Detecting time conflicts was important because it can notify the users to show the tasks that have time conflicts.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

--- I am very confident that my scheduler works correctly by sorting the tasks by the time and giving the warning for the tasks that have time conflicts. It also generates the schedule for today and schedule summary with reasoning. If I had more time, I would test for the schedule based on the species type.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

--- I am most satisfied with implementing the logic from pawpal_system.py to app.py using AI tools to make the UI usable and reflecting the logic from pawpal_system.py.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

--- I would improve or redesign on removing id numbers from the owner and pet. I think these id numbers are not important for the UI because the id numbers generates randomly and the UI doesn't ask about the id numbers, just asking for the owner's name and pet's name.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

--- One important thing I learned about designing systems or working with AI on this project was to create an initial UML design using the Mermaid.js, then implement the skeleton of the classes based on the UML design. This could be helpful for the future because it can generate tests and debug easier based on the tests to make a smarter UI.
