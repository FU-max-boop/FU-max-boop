# Claw-Eval Mini Preflight Report

Date: 2026-05-04

## One-Sentence Claim

Claw-Eval's trustworthy-agent-evaluation goal would benefit from an explicit static preflight layer that separates local setup/asset/metadata readiness issues from model-side agent failures before expensive three-trial benchmark runs.

## Paper Understanding

Claw-Eval targets a core problem in modern autonomous-agent evaluation: final-output-only grading misses important failures inside the trajectory. The paper frames three gaps in existing benchmarks:

- trajectory-opaque grading;
- underspecified safety and robustness evaluation;
- narrow modality and interaction coverage.

The benchmark addresses these gaps with 300 human-verified tasks across general service orchestration, multimodal perception/generation, and multi-turn professional dialogue. Its grading design records multiple evidence channels, evaluates completion/safety/robustness, and uses three-trial statistics to distinguish consistent reliability from lucky success.

This makes the benchmark valuable, but also makes reproduction heavier: an evaluator needs task metadata, services, fixtures, sandbox files, graders, model APIs, and sometimes media assets before any model-side conclusion is meaningful.

## What I Reproduced

I cloned the public GitHub repository:

```text
https://github.com/claw-eval/claw-eval
```

Local checkout:

```text
/Users/fu/Desktop/ai study/builds/claw-eval-ra/claw-eval
```

I did not run model evaluation, mock services, or sandbox containers yet. Instead, I reproduced the benchmark's task metadata layer by statically scanning all public `tasks/*/task.yaml` definitions and checking local file references.

## Contribution Implemented

Branch:

```text
docs/claw-eval-preflight-anatomy
```

Commit:

```text
f51ee0f Add static task preflight utility
```

Added files:

- `scripts/preflight_tasks.py`
- `docs/static_task_preflight.md`

The script performs a no-model, no-service, no-container preflight over task metadata:

- task split, category, language, difficulty, tags, dimensions;
- grader presence;
- service fixture references;
- sandbox file and prompt attachment references;
- tool/endpoint consistency;
- scoring-weight sanity;
- send-like tools without explicit send-safety checks;
- prompts that depend on external URLs.

## Local Findings

Generated outputs:

- `research/claw-eval-ra/preflight/claw_eval_task_preflight.csv`
- `research/claw-eval-ra/preflight/claw_eval_task_preflight.json`
- `research/claw-eval-ra/preflight/claw_eval_static_preflight_summary.md`

Static preflight snapshot:

| Metric | Count |
|---|---:|
| Tasks scanned | 300 |
| Local preflight-ready tasks | 232 |
| Local blocked tasks | 68 |
| General split | 161 |
| Multimodal split | 101 |
| Multi-turn split | 38 |
| English tasks | 179 |
| Chinese tasks | 121 |

The main blocking pattern is not YAML or grader failure. It is missing local sandbox media/document fixtures in the GitHub checkout:

- 64 multimodal/video tasks reference local video fixtures such as `fixtures/video.mp4` or `fixtures/video.webm`;
- 4 general PinBench-style document tasks reference missing document attachments or sandbox files;
- this is consistent with the README note that video fixtures are hosted through the Hugging Face dataset rather than stored in GitHub.

## Why This Is Useful

This contribution gives maintainers and new evaluators a cheap first pass before running expensive evaluations:

```text
Is this task blocked by local setup/assets/metadata, or is it ready for model-side evaluation?
```

That distinction matters for Claw-Eval because the paper's main claim is about trustworthy agent evaluation. If setup/asset failures are mixed with model failures, the resulting analysis is less diagnostic.

## Proposed Next Step

If this direction is useful, the next supervised mini-project could extend the preflight layer in two directions:

1. **Fixture archive verification**: once the Hugging Face fixtures are downloaded, verify GitHub + HF coverage jointly.
2. **Failure taxonomy**: run a small ready subset and separate setup failures, tool/service failures, safety violations, robustness instability, and model-side reasoning failures.

This naturally extends the Spider2-DBT preflight work into a second, more general agent benchmark reliability artifact.

