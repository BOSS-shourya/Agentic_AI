"""
03 · Agent anatomy — design a task-execution agent blueprint.

   >>> THIS IS YOUR WEEK 1 DELIVERABLE. <<<

Every agent, from a toy to a production system, is made of four parts:
    GOAL     — what it's trying to achieve (and how we know it's done)
    TOOLS    — how it acts on the world (APIs, code, search, databases)
    MEMORY   — what it remembers between steps
    ACTIONS  — the sequence of steps it takes

A worked EXAMPLE is filled in for you below. Study it, then design YOUR OWN
agent for a real, repetitive, multi-step task you'd like to automate.

-------------------------------------------------------------------
YOUR TASK
  TODO: Fill in `my_agent` with your own blueprint. Keep the task realistic
        and bounded. Be specific about `done_when` — a vague goal can't be
        evaluated. Then run the file to print your blueprint.
-------------------------------------------------------------------
No LLM/API key needed for this exercise — it's pure design.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class AgentBlueprint:
    name: str
    goal: str
    done_when: str
    tools: List[str] = field(default_factory=list)
    memory: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)

    def show(self):
        print("=" * 60)
        print(f" AGENT BLUEPRINT: {self.name}")
        print("=" * 60)
        print(f"GOAL       : {self.goal}")
        print(f"DONE WHEN  : {self.done_when}")
        print("TOOLS      :")
        for t in self.tools:
            print(f"   - {t}")
        print("MEMORY     :")
        for m in self.memory:
            print(f"   - {m}")
        print("ACTIONS    :")
        for i, a in enumerate(self.actions, 1):
            print(f"   {i}. {a}")
        print()


# ---------------------------------------------------------------------------
# WORKED EXAMPLE (already complete) — a restaurant-booking agent
# ---------------------------------------------------------------------------
example = AgentBlueprint(
    name="Restaurant Booking Agent",
    goal="Book a dinner table for 4 people this Friday at 8 PM near the user.",
    done_when="A confirmed booking (with a reference number) exists, or the user is told none is available.",
    tools=[
        "restaurant_search(area, cuisine) -> list of places",
        "check_availability(place, date, time, party_size) -> bool",
        "make_booking(place, date, time, party_size) -> confirmation",
    ],
    memory=[
        "User preferences (cuisine, budget, location)",
        "Places already tried (so it doesn't repeat)",
        "The current best candidate",
    ],
    actions=[
        "Search restaurants matching the user's preferences",
        "For each candidate, check availability for Friday 8 PM, party of 4",
        "If available, make the booking and return the confirmation",
        "If none available, report back and suggest alternative times",
    ],
)


# ---------------------------------------------------------------------------
# YOUR BLUEPRINT — assignment feedback agent
# ---------------------------------------------------------------------------
my_agent = AgentBlueprint(
    name="Assignment Feedback Agent",
    goal="Grade each submitted student assignment against the supplied rubric and draft actionable feedback.",
    done_when="Every assignment in the provided batch has a rubric-based score and feedback draft, or is marked for instructor review with the reason recorded.",
    tools=[
        "read_assignment(file_path) -> assignment text",
        "read_rubric(file_path) -> grading criteria and point values",
        "save_feedback(student_id, assignment_id, score, feedback) -> saved draft",
    ],
    memory=[
        "The roster and assignments in the current batch, including processing status",
        "The rubric criteria and point values used for this batch",
        "Scores, feedback drafts, and reasons for any instructor-review flags",
    ],
    actions=[
        "Load the assignment batch and rubric; confirm each submission can be matched to a student and assignment.",
        "For each submission, assess each rubric criterion and calculate the total score from the criterion scores.",
        "Draft concise, evidence-based feedback that cites the rubric and the submitted work.",
        "Flag missing, unreadable, ambiguous, or out-of-scope submissions for instructor review instead of guessing.",
        "Save each score and feedback draft, then verify every submission is either complete or flagged with a reason.",
    ],
)


if __name__ == "__main__":
    example.show()
    my_agent.show()
