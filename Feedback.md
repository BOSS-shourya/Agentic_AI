# Feedback

Date: 2026-09-27

- Missing a Problem folder or file with the actual problem you want to solve. Please add one.
- No secrets found; good.
- Your `.gitignore` is good.

## Week 1 skeleton review (2026-09-27)

Overall: 01–07 complete, with 07 stretch Level 3. Very strong work, and the shared AST evaluator in `utils/safe_math.py` is excellent.

- 01, 02: Done.
- 03: Done. *Assignment Feedback Agent* is properly rewritten: bounded to one batch, evaluable `done_when`, signatures, and it flags unclear cases instead of guessing.
- 04: Done, but brittle. `line` is the whole reply (line 43) and the regexes use `fullmatch`, so `FINAL: 180` followed by an explanation line is rejected. Keep only the first line.
- 05: Done, but brittle. `verdict.upper() == "CONFIRM"` (line 49) rejects "CONFIRM."; use `startswith("CONFIRM")`. Same first-line issue as 04.
- 06: Done.
- 07: Done + Level 3 (argument validation, bad-JSON handling). Try Levels 1, 2 and 4 next.
- Please keep the module docstrings/TODO banners; they were removed from 01–05.

## Follow-up review (2026-10-07)

**Previous feedback:** Not implemented. There are no new commits since 26 Sep (last push: "Merge latest README changes from GitHub"). Still open:
- Problem statement file: missing.
- 04: `line` is still the whole reply with `fullmatch` regexes; keep only the first line.
- 05: `verdict.upper() == "CONFIRM"` still rejects "CONFIRM."; use `startswith("CONFIRM")`.
- Module docstrings / TODO banners in 01–05: still removed.

Please address the points above first, then push Week 2 (labs 00–06 were due Mon 5 Oct; the `project/` milestone is due Sat 10 Oct).
