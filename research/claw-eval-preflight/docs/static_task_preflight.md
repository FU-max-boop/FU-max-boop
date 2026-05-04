# Static Task Preflight

This note documents a lightweight preflight pass for Claw-Eval task metadata.
It is intended to help contributors scope reproduction blockers before running
expensive agent, sandbox, grader, or model-API evaluations.

## What It Checks

`scripts/preflight_tasks.py` reads `tasks/*/task.yaml` and checks:

- task split, category, language, difficulty, tags, and dimensions
- grader presence
- service fixture references
- sandbox file and prompt attachment references
- tool/endpoint consistency
- scoring-weight sanity
- send-like tools without an explicit `tool_not_called` safety check
- prompts that depend on external URLs

The script does **not** execute task code, graders, mock services, agents,
containers, or model calls.

## Local Snapshot

On the current public GitHub checkout used for this preflight pass:

- tasks scanned: 300
- locally preflight-ready by metadata/file-reference checks: 232/300
- locally blocked: 68/300
- split counts: 161 general, 101 multimodal, 38 multi-turn

Most blocked tasks are video/media tasks whose local `sandbox_files` reference
video fixtures such as `fixtures/video.mp4` or `fixtures/video.webm`. This is
consistent with the README note that video fixtures are not included in the
GitHub repository and should be obtained from the Hugging Face dataset.

A smaller group of PinBench-style document tasks reference local document
fixtures that are not present in the GitHub checkout.

## Usage

```bash
python scripts/preflight_tasks.py --repo-root . --out-dir preflight_out
```

This writes:

- `preflight_out/claw_eval_task_preflight.csv`
- `preflight_out/claw_eval_task_preflight.json`
- `preflight_out/claw_eval_static_preflight_summary.md`

## Why This Helps

Claw-Eval evaluates autonomous agents through completion, safety, robustness,
and full-trajectory auditing. Before running three-trial evaluations, a static
preflight layer helps separate setup/asset/metadata readiness issues from
model-side failures.

This is especially useful when comparing agents across task splits, because a
missing local fixture or setup dependency should not be mixed into a model
reliability conclusion.
