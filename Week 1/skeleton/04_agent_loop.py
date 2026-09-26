import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient


def calculator(expression: str):
    return eval(expression, {"__builtins__": {}}, {})


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
    history = ""

    for step in range(1, MAX_STEPS + 1):

        prompt = ""  # TODO 1

        line = ""  # TODO 2
        print(f"[step {step}] {line}")

        if line.upper().startswith("FINAL:"):
            return line.split(":", 1)[1].strip()

        match = re.search(r"calculator\[(.+?)\]", line)
        if match:
            expr = match.group(1)
            result = None  # TODO 3
            print(f"        observation: calculator[{expr}] = {result}")

            pass  # TODO 4
        else:
            history += "\n(No valid action found; reply with ACTION: or FINAL:.)"

    return "Stopped: reached the step limit without a FINAL answer."


if __name__ == "__main__":
    goal = "What is (23 * 7) + 19?"
    final = run_agent(goal)
    print("-" * 60)
    print(f"AGENT'S FINAL ANSWER: {final}")
