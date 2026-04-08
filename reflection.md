# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
   actions: add a pet, schedule a walk, feeding

- Briefly describe your initial UML design.

My UML design outlines a simple pet care system with four main parts: Owner, Pet, Task, and Scheduler. Each part has its role — pets store information, tasks represent things that need to be done, and the scheduler helps with organizing.


- What classes did you include, and what responsibilities did you assign to each?

The system consists of four main classes: Owner, Pet, Task, and Scheduler.

Owner manages a collection of pets.

Each Pet stores basic information like name, animal type, breed, and age, and is associated with multiple tasks.

Task represents individual care actions such as feeding, walking, or medication, including attributes like time and priority.

Scheduler is responsible for organizing and prioritizing tasks, and generating a daily task list.

**b. Design changes**

- Did your design change during implementation?
  - Yes. I added a dedicated `Scheduler` class after the initial design so that scheduling logic stays separate from the data model.
- If yes, describe at least one change and why you made it.
  - I changed the design to separate task ordering into `Scheduler` instead of keeping it inside `Owner` or `Pet`, which makes the system easier to extend later.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - The scheduler considers task priority, scheduled time, pet assignment, and completion status.
- How did you decide which constraints mattered most?
  - I chose priority first because urgent care tasks should come before routine tasks, then time so the schedule flows in chronological order. Completion status is used to distinguish finished work from pending items.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - The scheduler detects conflicts only when tasks have the exact same scheduled time, instead of checking whether task durations overlap.
- Why is that tradeoff reasonable for this scenario?
  - This keeps the logic simple and reliable for an MVP. Exact-time conflict detection still catches obvious schedule collisions without adding the more complex interval arithmetic needed for full overlap detection.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  - I used AI to help translate the UML into Python class skeletons, review the scheduler design, and wire the Streamlit UI to the backend. AI also helped draft tests and summarize the new features in the README.
- What kinds of prompts or questions were most helpful?
  - Prompts asking for concrete class methods, how to sort tasks by time, how to store objects in `st.session_state`, and how to detect conflicts were the most useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  - I rejected a suggestion that made the scheduler too complex by trying to handle duration overlaps immediately. I kept the design simpler and only implemented exact-time conflict detection for the MVP.
- How did you evaluate or verify what the AI suggested?
  - I compared suggestions against the project requirements, ran the code, and added tests for the behaviors I implemented. If the suggestion introduced unnecessary complexity, I simplified it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  - I tested task completion, pet task addition, sorting by scheduled time, filtering tasks by pet, recurring daily task creation, and duplicate-time conflict detection.
- Why were these tests important?
  - These tests ensure that the scheduler behaves correctly for the core use cases and that the app can handle common pet care scheduling scenarios reliably.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - I am reasonably confident in the current implementation for the features that are covered by tests. The core scheduling logic, sorting, filtering, recurrence, and conflict detection are verified.
- What edge cases would you test next if you had more time?
  - I would test unscheduled tasks, overlapping durations, multiple pets with the same name, and weekly recurring task behavior.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  - I am most satisfied with building a full workflow from UML through backend logic to a working Streamlit UI with tests and documentation.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  - I would improve the conflict detection to consider task duration overlap and add a better UI for editing existing tasks and pet details.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  - I learned that AI is a powerful collaborator when I stay in control of design decisions, verify outputs, and keep the implementation simple and testable.
