# Hi, I'm Fu

I am building toward work as a student AI researcher / research engineer.

My current focus is making model behavior easier to inspect: small controlled experiments, reproducible evaluation pipelines, and AI workflows that turn vague questions into concrete research artifacts.

## Current Focus

- Context use vs shortcut behavior in language models
- Synthetic benchmarks for compositional generalization
- Research engineering: clean experiment runners, result cards, and reproducible figures
- Agentic AI workflows for research, learning, and iteration

## Featured Project

### [mini-llm-lab](https://github.com/FU-max-boop/mini-llm-lab)

`mini-llm-lab` is a controlled mini-benchmark for studying when tiny causal transformers genuinely use earlier context, and when they fall into shortcut regimes.

The current result studies a two-clue synthetic task family:

```text
0 clues visible -> local guessing
1 clue visible  -> stable single-clue shortcut regime
2 clues visible -> near-compositional use of both clues
```

The project includes:

- runnable experiment scripts
- saved JSON results
- result cards and technical memos
- a regenerated main figure
- a first bridge to a more LLM-like tiny backbone using RoPE, RMSNorm, and SwiGLU

### [Spider2-DBT Preflight Analysis](research/spider2-dbt-preflight)

A small research-engineering contribution around Spider2-DBT reproducibility and agent evaluation.

I reproduced the Spider2-DBT setup/evaluation path, found that only 61/68 tasks appear evaluation-ready after local setup due to asset/metadata mismatches, and built preflight tooling plus agent-facing DBT task briefs to separate benchmark packaging failures from genuine agent failures.

Artifacts include:

- a pushed Spider2 fork branch with docs/preflight commits
- a PR-ready upstream compare view
- task-level preflight CSV and Markdown summary
- scripts for DBT asset checks, static task analysis, and task brief generation
- generated briefs for `playbook001`, `jira001`, `quickbooks001`, and `gitcoin001`

### [Claw-Eval Static Task Preflight](research/claw-eval-preflight)

A small contribution around trustworthy autonomous-agent evaluation. I scanned
all 300 public Claw-Eval task definitions and added a static preflight utility
that separates setup, asset, and metadata readiness issues from model-side
agent failures before expensive benchmark runs.

Published branch: https://github.com/FU-max-boop/claw-eval/tree/docs/claw-eval-preflight-anatomy

### [LightRAG Evaluation Preflight](research/lightrag-evaluation-preflight)

A small contribution around HKUDS LightRAG evaluation reproducibility. I added a
zero-API-call preflight utility for the RAGAS evaluation workflow so users can
catch dataset, dependency, API-key, numeric-env, and endpoint configuration
issues before spending time or model budget.

Published branch: https://github.com/FU-max-boop/LightRAG/tree/docs/eval-readiness-preflight

## How I Work

I like turning a research idea into a visible artifact:

1. write the question clearly
2. build the smallest controlled setting
3. run experiments across seeds and variants
4. summarize results in result cards
5. publish code, figures, limitations, and next steps

## Direction

I am especially interested in the space between AI research and research engineering: evaluation, interpretability-adjacent experiments, agentic workflows, and tools that make model behavior easier to reason about.
