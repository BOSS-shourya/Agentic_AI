"""
04 · Build the agent loop  —  observe -> reason -> act -> evaluate.

   >>> THE ONE REAL CODING EXERCISE OF WEEK 1. <<<

You'll complete a minimal but REAL agent. Given a goal, it loops:
    OBSERVE   assemble the prompt from the goal + what has happened so far
    REASON    the LLM decides the next step (an ACTION, or a FINAL answer)
    ACT       run the chosen tool (a calculator) and get a result
    EVALUATE  if the LLM said FINAL, stop; otherwise record the result and loop

The calculator tool, system prompt, parsing, and loop steps are implemented.

-------------------------------------------------------------------
The completed `run_agent` implements OBSERVE, REASON, ACT, and EVALUATE.
-------------------------------------------------------------------
Run it:  python "Week 1/skeleton/04_agent_loop.py"
Goal to solve:  "What is (23 * 7) + 19?"   (expected: 180)
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient
from utils.safe_math import evaluate_arithmetic


def calculator(expression: str):
    """Evaluate a math expression exactly."""
    return evaluate_arithmetic(expression)


SYSTEM = """You are a reasoning agent that solves a task step by step.
You have ONE tool:
  calculator[expression]  -> evaluates a math expression (e.g. calculator[23*7]).

At EACH step reply with EXACTLY ONE line, in one of these two forms:
  ACTION: calculator[<expression>]
  FINAL: <the final answer>

Take only ONE action at a time. Use the observations you are given.
"""

MAX_STEPS = 6


def run_agent(goal: str):
    print(f"\nGOAL: {goal}\n" + "-" * 60)
    client = LLMClient()
    history = ""   # the agent's MEMORY of the run

    for step in range(1, MAX_STEPS + 1):

        prompt = f"Task: {goal}\n{history}\nWhat is your next step?"

        response = client.get_completion(
            prompt,
            system_message=SYSTEM,
            temperature=0.0,
            max_tokens=200,
        )
        lines = (response or "").strip().splitlines()
        line = next((item.strip() for item in lines if item.strip()), "")
        print(f"[step {step}] {line}")

        if line.upper().startswith("FINAL:"):
            return line.split(":", 1)[1].strip()

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

    return "Stopped: reached the step limit without a FINAL answer."


if __name__ == "__main__":
    goal = "What is (23 * 7) + 19?"
    final = run_agent(goal)
    print("-" * 60)
    print(f"AGENT'S FINAL ANSWER: {final}")
    # Stretch: add a second tool and let the agent choose between tools.
