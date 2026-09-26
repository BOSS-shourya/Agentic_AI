"""
07 · ADVANCED TRACK — native function calling.  (optional · for fast finishers)

In Labs 04–06 the agent chose tools by writing text like  ACTION: calc[...]  and
we parsed it with a regex. That works, but every serious provider now offers
NATIVE FUNCTION / TOOL CALLING: you describe your tools as JSON schemas, and the
model returns a structured, validated tool call — no fragile string parsing.
This is exactly what Module 2 (Tool Use & Function Calling) is about; you're
getting a head start.

    You  ->  give the model a `tools` schema
    Model ->  returns tool_calls (name + JSON arguments)
    You  ->  run the tool, hand back the result, loop until it stops

This file targets the OpenAI / Groq chat-completions tools API (same shape).
Set LLM_PROVIDER=openai or groq in your .env.

-------------------------------------------------------------------
The native calculator tool schema and tool-calling loop are implemented.
Optional stretch challenges are listed at the bottom.
-------------------------------------------------------------------
Run it:  python "Week 1/skeleton/07_advanced_agent.py"
"""

import sys, os, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.llm_client import LLMClient
from utils.safe_math import evaluate_arithmetic

def calculator(expression: str):
    """AST-safe calculator (no eval)."""
    return evaluate_arithmetic(expression)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a basic arithmetic expression exactly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "An arithmetic expression using numbers and +, -, *, /, and parentheses.",
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    }
]


def run_agent(goal: str):
    client = LLMClient()
    if client.provider not in ("openai", "groq"):
        print("This advanced demo targets LLM_PROVIDER=openai or groq.")
        return
    sdk = client.client                      # the raw OpenAI/Groq SDK client
    model = client._default_model()
    messages = [{"role": "user", "content": goal}]

    for step in range(1, 9):
        response = sdk.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            temperature=0.0,
        )
        msg = response.choices[0].message

        if not getattr(msg, "tool_calls", None):
            print("FINAL:", msg.content or "")
            return msg.content

        messages.append(msg)   # record the assistant's tool request
        for tc in msg.tool_calls:
            try:
                args = json.loads(tc.function.arguments or "{}")
                if not isinstance(args, dict) or not isinstance(args.get("expression"), str):
                    raise ValueError("tool arguments must include a string expression")
                if tc.function.name != "calculator":
                    raise ValueError(f"unknown tool: {tc.function.name}")
                result = calculator(args["expression"])
            except (ArithmeticError, json.JSONDecodeError, SyntaxError, TypeError, ValueError) as error:
                result = f"error: {error}"
            print(f"[step {step}] {tc.function.name} -> {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result),
                }
            )

    print("Stopped: step limit.")


if __name__ == "__main__":
    run_agent("What is (23 * 7) + 19? Use the calculator tool, then give the final number.")


# ============================ CHALLENGES ============================
# Level 1  · Add a second tool (e.g. price_lookup) with its own schema and let
#            the model choose. (previews Module 2)
# Level 2  · Add a REFLECT step: after the model's final answer, ask it to CONFIRM
#            or REVISE, and loop on REVISE. (previews Modules 3–4 & 7)
# Level 3  · Implemented here: validate tool arguments, handle bad JSON, and
#            keep the AST-safe calculator — never eval() model output.
# Level 4  · Write 8–10 lines on how MCP (Model Context Protocol) would replace
#            these hand-written schemas with a shared tool server your agent
#            connects to. (previews Module 6: Multi-Agent + MCP)
# ===================================================================
