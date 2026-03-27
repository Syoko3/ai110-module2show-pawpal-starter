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

--- I used the AI tools during this project for 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

--- I did not accept an AI suggestion as-is for 

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

--- I tested on 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

--- I am very confident that my scheduler works correctly by 

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

--- I am most satisfied with 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

--- I would improve 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

--- 
