# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- My initial UML would consist of 4 tables:
  - Owner
  - Pet
  - Task
  - Schedule (Added later on)
  - Employee (Added later on)
  - Assignment (Added later on)
- What classes did you include, and what responsibilities did you assign to each?
  - Owner - Name of the owner, maybe how much the services would cost in total? Would have a reference to a Pet, I think also a pickup time for the pet?
  - Pet - Identifiers like name, breed, would also have a reference to a list of Services to be done
  - Tasks - A list of Services to be done for the pet
  - Schedule - Meat and potatoes of it, Would need the time it would take for each task (to measure out the effort) maybe in the form of start and end time? Keep a list of all tasks to do for that day. This table would reference both pet and tasks How would I measure effort level (do i even need to)? Are there some tasks that need to be done as a priority?
  - Employee - An employee is assigned a pet and a task to do for each pet. An employee can have many assignments.
  - Assignment - Dictates which employee is assigned to what pet and what tasks. An Assignment has information on which Employee is assigned to what pet, what task, and the estimated time to perform a task.

**b. Design changes**

- Did your design change during implementation?
  - Yes
- If yes, describe at least one change and why you made it.
  - So Initially I had 3 tasks, but I was told that maybe handling the tasks to be done should be added in a separate table called schedule, where it'll list out all the tasks to be done that day. I'm also contemplating if it is worth keeping track of past tasks? If I need to remove already completed tasks, or just add a bool like completed.
  - Its easier to think about this way so that each table has a completely separate responsibility rather than the task table do the heavy lifting.
  - Now that I'm thinking about it also, maybe I should have another table for the workers and who is assigned to the pet.

  - After consulting my Claude Code, some urgent changes were made to my plan:
    - Each table requires an identifier (id), this is a problem since we might potentially lose some data on deletion/completions of task (I.E, we might have 2 pets with the same name, the same task done to two different pets.)
    - Its hard to check on Pet table, what task/Employee they were assigned to. I'd have to scan the schedule/ Employee table to get the answer, no direct Pet -> Assignment
    - Some data types are allowing for direct mutation of a class' data and not giving just the copy to work with. This is pretty bad practice to do, and more touches separation of concerns.
    - Bidirectional link between Employee and Assignment isn't enforced. Assignment.employee and Employee.assignments both exist, but nothing keeps them in sync — calling employee.assign_task(a) doesn't set a.employee, and vice versa. Easy to end up with an Assignment pointing to an Employee who doesn't have it in their list (or duplicates on repeated calls).
    - No path from Pet's tasks → an actual Schedule. Schedule only holds assignments it's already given (add_assignment), but nothing in the file turns a Pet's unassigned tasks into Assignments. generate_plan() has no visibility into Owner/Pet/Employee pools to pull from — right now it can only reorder assignments that already exist. This is the core scheduling gap since the whole point of the app is to build the plan from raw tasks.

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
- AI was practically the MVP when it came to planning. I had an initial idea in mind as to how the UML would look, as well as what relationship each class would have. After consulting Claude for what I might potentially be missing, it brought up some gaps in the relationships in my table that should be addressed. This also gave me a eureka moment for what classes I might need to include as well (Assignments, Employee). After a couple passes with the updated plan, reviewing the Mermaid.js file really solidified my confidence as to the functionality/relationship of each class. However, the actual data and method within each class was definitely something worth improving. Claude caught this very early on and I decided to go with its suggestions (I.E no unique identifiers, incorrect handling of getters and setters).
- What kinds of prompts or questions were most helpful?
- Just a force of habbit on my part, but I like to ask for summaries of the current changes on the file. AI models like to yap and give 5 part essays on what changed/why it changed/other things to consider. Secondly, I like to break down each change and ask why it suggests to do that; 9/10 times it suggests an overcomplicated solution when we could just introduce a new class to handle the logic. "Lets have 3 other ways to fix this problem" is super helpful since at least 1 of the solutions it suggests is the one I am thinking.
- WOW the 1-line documentation on each method is suuuuper useful. Not only is it a sanity check for yourself that the function does in fact perform what it should do, but documentation is a painstakingly useful tool all developers practice to be able to pass off work to others with ease.

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
