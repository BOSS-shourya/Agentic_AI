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


my_agent = AgentBlueprint(
    name="xav_bot",
    goal="correct assignment of my students",
    done_when="It's complete when all assignments of my students are corrected and feedback is provided.",
    tools=[
        "ACces to internet",
        "PDF reader",
    ],
    memory=[
        "List of students and their assignments",
        "Feedback provided to each student in previous sessions",
    ],
    actions=[
        "Review each student's assignment",
        "Provide feedback and corrections",
        "Notify me when all assignments are corrected and feedback is provided",
    ],
)


if __name__ == "__main__":
    example.show()
    my_agent.show()
