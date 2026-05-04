# OpenCUA AgentNetBench Evaluator Validity + Preflight

This is a research-engineering contribution for OpenCUA / AgentNetBench. I first added a static preflight utility that checks whether a local AgentNetBench run is ready before starting expensive GUI-agent evaluation.

I then added an evaluator-validity fix with offline regression tests, because small evaluator mistakes can directly change benchmark scores.

Published branch: https://github.com/FU-max-boop/OpenCUA/tree/docs/agentnetbench-preflight

## Evaluator Validity Fix

The evaluator update addresses four scoring risks:

- importing `eval.py` no longer auto-runs `pip install editdistance`; missing
  `editdistance` uses a built-in Levenshtein fallback
- opposite-direction scroll actions no longer get full credit
- numeric scroll actions now score direction plus amount similarity
- `press` / `hotkey` comparison preserves key order and repeated keys instead of using sets
- extra predicted actions are penalized, so a correct first action followed by unrelated actions does not receive full credit

I added offline regression tests for:

- missing optional `editdistance`
- wrong-direction scroll
- same-direction scroll with different amount
- hotkey order mismatch
- repeated-key mismatch
- extra-action penalty

## What It Checks

- trajectory JSON parseability
- required trajectory fields
- step and alternative-option shapes
- referenced screenshot/image existence
- GUI action types
- relative coordinate bounds
- duplicate task IDs
- runtime dependencies
- model-to-agent selection
- OpenAI-compatible endpoint URL and API-key configuration

## Validation Result

The sample AgentNetBench data passed the static readiness checks:

- 5 trajectories scanned
- 54 steps scanned
- 12 checks passed
- 1 warning: optional `editdistance` dependency missing
- 0 blockers

## Files

- `preflight.py`: proposed utility
- `report.md`: local validation report
- `report.json`: machine-readable report
- `0001-add-agentnetbench-preflight-checks.patch`: patch for review
- `test_eval.py`: evaluator-validity regression tests
- `0002-fix-agentnetbench-evaluator-validity.patch`: patch for review
