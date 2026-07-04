# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- My initial UML would consist of 4 tables:
  - Owner
  - Pet
  - Services
  - Schedule
- What classes did you include, and what responsibilities did you assign to each?
  - Owner - Name of the owner, maybe how much the services would cost in total? Would have a reference to a Pet, I think also a pickup time for the pet?
  - Pet - Identifiers like name, breed, would also have a reference to a list of Services to be done
  - Tasks - A list of Services to be done for the pet
  - Schedule - Meat and potatoes of it, Would need the time it would take for each task (to measure out the effort) maybe in the form of start and end time? Keep a list of all tasks to do for that day. This table would reference both pet and tasks How would I measure effort level (do i even need to)? Are there some tasks that need to be done as a priority?

**b. Design changes**

- Did your design change during implementation?
  - Yes
- If yes, describe at least one change and why you made it.
  - So Initially I had 3 tasks, but I was told that maybe handling the tasks to be done should be added in a separate table called schedule, where it'll list out all the tasks to be done that day. I'm also contemplating if it is worth keeping track of past tasks? If I need to remove already completed tasks, or just add a bool like completed.
  - Its easier to think about this way so that each table has a completely separate responsibility rather than the task table do the heavy lifting.
  - Now that I'm thinking about it also, maybe I should have another table for the workers and who is assigned to the pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - I think for sure the priority of the tasks, which ones are urgent to do v time sensitive, maybe the amount of effort one task is v another, I'm not sure if that's within the same realm of priority. Another thing also might be if the owner brought in more than one pet, the scheduler should consider trying to finish the tasks for both pets ideally close to the same time to eachother.
- How did you decide which constraints mattered most?
  - I think I thought of it more as how I would order the most important feature (the scheduler) and just built it off the most important functionalities of that feature and build around that.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - I think there will be some issues with priority, specifically jumping around tasks from one pet to another. Since the services are based off of priority and time sensitivity, there might be gaps in between servicing each pet. (Revised my plan at this point to have an employee list, and possibly a separate table Assignment, for which employee is assigned to do the task for an animal.)
- Why is that tradeoff reasonable for this scenario?
  - I'm basing this off of efficiency of the workflow so that there is little to no conflict when it comes to forgetting to do a specific task. Having a priority/time sensitive ordered schedule will make sure that the most important tasks are done, then the menial task will be done last, with the cost of the menial task to be always done less (This will mean that if an owner were to come in with just 1 menial services to do for the dog, it will have to be done after all the priority tasks are done or if their pickup time is coming up.)

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
