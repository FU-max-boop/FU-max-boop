# OpenCUA AgentNetBench Preflight

This is a small research-engineering contribution for OpenCUA / AgentNetBench. I added a static preflight utility that checks whether a local AgentNetBench run is ready before starting expensive GUI-agent evaluation.

Published branch: https://github.com/FU-max-boop/OpenCUA/tree/docs/agentnetbench-preflight

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
