# Week 1 — Foundations of Agentic AI

Module 1. Three sessions (Mon 2h · Wed 2h · Sat 4h lab). This week is about
**building the mental model** — it is deliberately light on coding. You'll run a
few short demos, design an agent on paper, and finish by building one small,
real **agent loop**.

## Learning objectives
By the end of the week you can:
- Explain what an AI **agent** is and how it differs from an assistant.
- Name the **four parts** of every agent: goal, tools, memory, actions.
- Describe three LLM limits (hallucination, no-action, reasoning drift) and how agents address them.
- Trace the **agent loop**: observe → reason → act → evaluate.
- Run a working agent loop and design a blueprint of your own.

## Exercises (completed implementations are in `skeleton/`)

| File | What it is | Status |
|------|-----------|---------|
| `00_setup_check.py` | Verify your environment + first LLM call | Run to check API setup |
| `01_assistant_vs_agent.py` | Compare a language-only answer with an exact arithmetic tool | Complete; requires API key |
| `02_llm_reasoning_limits.py` | See hallucination & reasoning drift | Complete; requires API key |
| `03_agent_anatomy.py` | **Design your agent blueprint** — *deliverable* | Complete; no API key |
| `04_agent_loop.py` | **Build the agent loop** — the week's coding exercise | Complete; requires API key |
| `05_reflection_loop.py` | Add self-check (reflect → retry) to the loop | Complete; requires API key |
| `06_multi_tool_agent.py` | Two tools + choose one; safe arithmetic calculator | Complete; requires API key |
| `07_advanced_agent.py` | *Advanced:* native function calling | Complete; OpenAI or Groq API |

## How to run
```bash
cd "Week 1"
python skeleton/00_setup_check.py
python skeleton/01_assistant_vs_agent.py
# ...and so on
```

## Deliverables (bring to next Monday)
1. **Agent blueprint** — your completed `03_agent_anatomy.py` (`my_agent`).
2. **Working agent loop** — your completed `04_agent_loop.py` solving `(23 * 7) + 19 = 180`.
3. All files pushed to your course **GitHub repo**.

See **STUDENT_ACTION_ITEMS.md** for the full checklist.
