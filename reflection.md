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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
