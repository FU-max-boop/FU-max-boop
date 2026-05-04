# Claw-Eval Static Task Preflight

This is a small research-engineering contribution around Claw-Eval, a benchmark
for trustworthy autonomous agent evaluation.

I statically scanned all 300 public task definitions and added a no-model,
no-service, no-container preflight utility that separates local setup, asset,
and metadata readiness issues from model-side agent failures.

## Published Code

- Fork branch: https://github.com/FU-max-boop/claw-eval/tree/docs/claw-eval-preflight-anatomy
- Upstream compare view: https://github.com/claw-eval/claw-eval/compare/main...FU-max-boop:claw-eval:docs/claw-eval-preflight-anatomy

## Snapshot

- Tasks scanned: 300
- Local preflight-ready tasks: 232
- Local blocked tasks: 68
- Main blocker: missing local media/document fixtures in the GitHub checkout,
  especially multimodal video assets that are distributed separately.

## Files

- `report.md`: mini reproduction and contribution report
- `tools/preflight_tasks.py`: static task readiness checker
- `docs/static_task_preflight.md`: documentation proposed for the upstream repo
- `outputs/`: CSV, JSON, and Markdown preflight outputs
- `patches/`: patch generated from the pushed fork branch
