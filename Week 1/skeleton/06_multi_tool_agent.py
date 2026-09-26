"""
06 · Multi-tool agent + safe execution.  (NEW · builds on 04)

One tool is a toy. Real agents pick the RIGHT tool from several. Here the agent
has TWO tools and must choose between them to finish a task:

    price_lookup[item]   -> look a price up in a small catalogue
    calc[expression]     -> do the arithmetic  (SAFELY — no eval!)

Example goal: "What is the total price of 3 widgets and 2 gadgets?"
  -> price_lookup[widget] = 25
  -> price_lookup[gadget] = 40
  -> calc[3*25 + 2*40]    = 155

SAFETY: model-generated expressions are untrusted; evaluating them with eval()
can execute dangerous code. This agent uses a locked-down arithmetic parser
instead. Never trust model output blindly — that instinct is the whole of
Module 7 (guardrails).

WHERE THIS GOES: choosing between tools previews Module 2 (tool use /
function calling); locking down execution previews Module 7 (guardrails).

-------------------------------------------------------------------
The completed agent uses an AST-safe calculator, dispatches both tools, and
parses generic ACTION lines.
-------------------------------------------------------------------
Run it:  python "Week 1/skeleton/06_multi_tool_agent.py"
"""

import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.llm_client import LLMClient
from utils.safe_math import evaluate_arithmetic

# --- a tiny catalogue our first tool reads from ---
CATALOGUE = {"widget": 25, "gadget": 40, "sprocket": 12, "bolt": 3}

def price_lookup(item: str):
    """Tool 1: return the catalogue price, or an error string."""
    item = item.strip().lower()
    return CATALOGUE.get(item, f"error: no price for '{item}'")


def safe_calc(expression: str):
    """
    Tool 2: evaluate arithmetic WITHOUT eval().
    Evaluate the arithmetic expression with the shared AST-safe helper and
    return a readable error string for invalid input.
    """
    try:
        return evaluate_arithmetic(expression)
    except (ArithmeticError, SyntaxError, TypeError, ValueError) as error:
        return f"error: {error}"


def dispatch(tool: str, arg: str):
    """
    Return the result of the right tool for `tool`:
        "price_lookup" -> price_lookup(arg)
        "calc"         -> safe_calc(arg)
        anything else  -> "error: unknown tool"
    """
    tool = tool.strip().lower()
    if tool == "price_lookup":
        return price_lookup(arg)
    if tool == "calc":
        return safe_calc(arg)
    return f"error: unknown tool '{tool}'"


SYSTEM = """You are a reasoning agent with TWO tools:
  price_lookup[item]   -> the price of one item from the catalogue
  calc[expression]     -> evaluate a math expression (numbers and + - * / only)

At EACH step reply with EXACTLY ONE line:
  ACTION: <tool>[<argument>]
  FINAL: <the final answer>
Take ONE action at a time and use the observations you are given.
"""

MAX_STEPS = 8


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
            return line.split(":", 1)[1].strip()

        match = re.fullmatch(
            r"ACTION:\s*([A-Za-z_][A-Za-z0-9_]*)\[(.*)\]\s*",
            line,
            flags=re.IGNORECASE,
        )
        if match:
            tool, arg = match.groups()
            result = dispatch(tool, arg)
            print(f"        observation: {tool}[{arg}] = {result}")
            history += f"\nYou ran {tool}[{arg}] and got {result}."
        else:
            history += "\n(No valid action found; reply with ACTION: or FINAL:.)"

    return "Stopped: reached the step limit."


if __name__ == "__main__":
    goal = "What is the total price of 3 widgets and 2 gadgets?"
    print("FINAL:", run_agent(goal))
