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
        line = (response or "").strip()
        print(f"[step {step}] {line}")

        final = re.fullmatch(r"FINAL:[ \t]*([^\r\n]+)", line, re.IGNORECASE)
        if final and final.group(1).strip():
            answer = final.group(1).strip()
            verdict = (reflect(client, goal, answer) or "").strip()
            print(f"        reflection: {verdict}")
            if verdict.upper() == "CONFIRM":
                return answer
            history += (
                f"\nThe proposed answer {answer!r} was not confirmed. "
                f"Reflection: {verdict or 'No usable verdict was returned.'} "
                "Re-check the work and try again."
            )
            continue

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

    return "Stopped: reached the step limit without a confirmed answer."


if __name__ == "__main__":
    goal = "What is (23 * 7) + 19?"
    print("FINAL:", run_agent(goal))
