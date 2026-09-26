import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient


def demo_hallucination(client):
    print("=" * 60)
    print(" 1 · HALLUCINATION")
    print("=" * 60)
    prompt = ("Tell me about the 'PyGundam-7B' Python library. "
              "What are its main features and how do I install it?")
    print(f"Prompt: {prompt}\n")
    print(client.get_completion(prompt), "\n")
    print(">> The library does not exist — yet the model confidently describes it.")
    print(">> Fix (Module 5): ground the model in real documents with RAG.\n")


def demo_reasoning(client):
    print("=" * 60)
    print(" 2 · MULTI-STEP REASONING")
    print("=" * 60)
    puzzle = (
        "Three boxes: A has Red, B has Blue, C has Green.\n"
        "1) Swap A and B. 2) Swap B and C. "
        "3) Take the ball in A into your pocket. 4) Swap A and C.\n"
        "What is in A, B, C, and the pocket at the end?"
    )
    ground_truth = "A: Red, B: Green, C: (empty), Pocket: Blue"

    print("Attempt 1 — direct answer (no reasoning shown):")
    direct = client.get_completion(puzzle + "\nGive only the final answer.", temperature=0.0)
    print(direct, "\n")

    print("Attempt 2 — chain-of-thought:")
    cot_prompt = ""  # TODO 1
    if not cot_prompt:
        print("(Complete TODO 1 to run the chain-of-thought version.)\n")
    else:
        print(client.get_completion(cot_prompt, temperature=0.0), "\n")

    print(f"Ground truth: {ground_truth}")
    print(">> Without intermediate steps, models often lose track of state.")
    print(">> Fix (Modules 3-4): reasoning structure (ReAct) + memory.")


def main():
    client = LLMClient()
    demo_hallucination(client)
    demo_reasoning(client)


if __name__ == "__main__":
    main()
