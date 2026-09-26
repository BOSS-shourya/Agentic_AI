"""
05 · Reflection — make the agent check its own work.  (NEW · builds on 04)

In Lab 3 you built the loop: observe -> reason -> act -> evaluate.
Real agents add one more move: REFLECT — before trusting a final answer, the
agent critiques it and, if it isn't confident, tries again with that feedback.
This is the "Reflection" / Reflexion pattern, and it's one of the most common
reliability tricks in production agents in 2026.

    observe -> reason -> act -> evaluate -> REFLECT -> (loop again if needed)

WHERE THIS GOES: self-critique + feedback-in-memory is the seed of
Module 3 (agent architectures) and Module 4 (memory); "is the answer good
enough?" is the heart of Module 7 (evaluation & guardrails).

-------------------------------------------------------------------
The completed loop asks the model to reflect on each final answer and retries
when the reflection does not confirm it.
-------------------------------------------------------------------
Run it:  python "Week 1/skeleton/05_reflection_loop.py" (goal solves to 180)
"""

import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.llm_client import LLMClient
from utils.safe_math import evaluate_arithmetic


def calculator(expression: str):
    return evaluate_arithmetic(expression)


SYSTEM = """You are a reasoning agent that solves a task step by step.
You have ONE tool:
  calculator[expression]  -> evaluates a math expression (e.g. calculator[23*7]).
At EACH step reply with EXACTLY ONE line, in one of these two forms:
  ACTION: calculator[<expression>]
  FINAL: <the final answer>
Take only ONE action at a time. Use the observations you are given.
"""

MAX_STEPS = 8


def reflect(client, goal, answer):
    """
    Ask the LLM to check `answer` against `goal`.
    It is prompted to respond with EXACTLY one line:
        CONFIRM
      or
        REVISE: <one sentence on what is wrong>
    Keep temperature=0.0.
    """
    prompt = (
        f"Task: {goal}\nProposed answer: {answer}\n"
        "Check the answer independently against the task. Reply with exactly one line: "
        "CONFIRM if it is correct, or REVISE: <one sentence explaining the error>."
    )
    return client.get_completion(prompt, temperature=0.0, max_tokens=200)


def run_agent(goal: str):
    print(f"\nGOAL: {goal}\n" + "-" * 60)
    client = LLMClient()
    history = ""

    for step in range(1, MAX_STEPS + 1):
        prompt = f"Task: {goal}\n{history}\nWhat is your next step?"
        response = client.get_completion(prompt, system_message=SYSTEM,
                                         temperature=0.0, max_tokens=200)
        line = (response or "").strip().splitlines()[0].strip() if response else ""
        print(f"[step {step}] {line}")

        if line.upper().startswith("FINAL:"):
            answer = line.split(":", 1)[1].strip()
            verdict = (reflect(client, goal, answer) or "").strip()
            print(f"        reflection: {verdict}")
            if verdict.upper().startswith("CONFIRM"):
                return answer
            history += (
                f"\nThe proposed answer {answer!r} was not confirmed. "
                f"Reflection: {verdict or 'No usable verdict was returned.'} "
                "Re-check the work and try again."
            )
            continue

        match = re.search(r"calculator\[(.+?)\]", line)
        if match:
            expr = match.group(1)
            try:
                result = calculator(expr)
            except (ArithmeticError, SyntaxError, TypeError, ValueError) as error:
                result = f"error: {error}"
            print(f"        observation: calculator[{expr}] = {result}")
            history += f"\nYou ran calculator[{expr}] and got {result}."
        else:
            history += "\n(No valid action found; reply with ACTION: or FINAL:.)"

    return "Stopped: reached the step limit without a confirmed answer."


if __name__ == "__main__":
    goal = "What is (23 * 7) + 19?"
    print("FINAL:", run_agent(goal))
