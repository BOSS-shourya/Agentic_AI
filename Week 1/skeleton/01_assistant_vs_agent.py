import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient
from utils.safe_math import evaluate_arithmetic


def calculator(expression: str):
    return evaluate_arithmetic(expression)


def main():
    client = LLMClient()

    task = "What is 18.5% of 2480, plus 365? Give only the number."

    print("=" * 60)
    print(" (A) ASSISTANT — answers in words (may be wrong)")
    print("=" * 60)
    assistant_answer = client.get_completion(task, temperature=0.0)
    print(assistant_answer, "\n")

    print("=" * 60)
    print(" (B) AGENT — uses the calculator tool (exact)")
    print("=" * 60)
    expression = "0.185 * 2480 + 365"   # (matches the task above; change if your task differs)
    tool_result = calculator(expression)
    print(f"calculator({expression!r}) = {tool_result}\n")

    print("-" * 60)
    print("ANALYSIS: The assistant produced text; the agent RAN CODE.")
    print("Only the agent's answer is guaranteed correct — that's why agents use tools.")


if __name__ == "__main__":
    main()
