import sys
import os
import re
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
        line = (response or "").strip()
        print(f"[step {step}] {line}")

        final = re.fullmatch(r"FINAL:[ \t]*([^\r\n]+)", line, re.IGNORECASE)
        if final and final.group(1).strip():
            return final.group(1).strip()

        match = re.fullmatch(
            r"ACTION:[ \t]*calculator\[([^\[\]\r\n]+)\]", line, re.IGNORECASE
        )
        if match:
            expr = match.group(1).strip()
            try:
                result = calculator(expr)
            except (ArithmeticError, SyntaxError, TypeError, ValueError) as error:
                result = f"error: {error}"
            print(f"        observation: calculator[{expr}] = {result}")

            history += f"\nYou ran calculator[{expr}] and got {result}."
        else:
            history += (
                "\nInvalid or empty response. Reply with exactly one line: "
                "ACTION: calculator[<expression>] or FINAL: <answer>."
            )

    return "Stopped: reached the step limit without a FINAL answer."


if __name__ == "__main__":
    goal = "What is (23 * 7) + 19?"
    final = run_agent(goal)
    print("-" * 60)
    print(f"AGENT'S FINAL ANSWER: {final}")
