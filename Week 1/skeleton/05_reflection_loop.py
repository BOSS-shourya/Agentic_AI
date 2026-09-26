import sys, os, re
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

MAX_STEPS = 8


def reflect(client, goal, answer):
    return "CONFIRM"   # <- replace this stub


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
            return answer   # <- replace: only return after a CONFIRM

        match = re.search(r"calculator\[(.+?)\]", line)
        if match:
            expr = match.group(1)
            try:
                result = calculator(expr)
            except Exception as e:
                result = f"error: {e}"
            print(f"        observation: calculator[{expr}] = {result}")
            history += f"\nYou ran calculator[{expr}] and got {result}."
        else:
            history += "\n(No valid action found; reply with ACTION: or FINAL:.)"

    return "Stopped: reached the step limit without a confirmed answer."


if __name__ == "__main__":
    goal = "What is (23 * 7) + 19?"
    print("FINAL:", run_agent(goal))
