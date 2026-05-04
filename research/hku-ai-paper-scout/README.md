# HKU AI Paper Contribution Scout

I scanned recent HKU AI-adjacent repositories across HKUDS, HKUNLP, and XLang, then prioritized projects where a student research engineer could provide visible value quickly: reproducibility, static validation, benchmark readiness, and experiment hygiene.

## Selection Rule

I prioritized projects that were:

- recent or actively maintained
- connected to agentic AI, RAG, deep research, GUI agents, or evaluation
- likely to have high setup cost for new users
- suitable for a small, reviewable contribution with no model/API calls

## Completed Contribution Batch

| Project | Contribution | Published branch |
| --- | --- | --- |
| DeepCode | Config preflight for provider keys, MCP commands, dependency readiness, workspace paths, and model-run setup | https://github.com/FU-max-boop/DeepCode/tree/docs/deepcode-config-preflight |
| AI-Researcher | Benchmark/env preflight plus README Docker image typo correction for autonomous research-agent runs | https://github.com/FU-max-boop/AI-Researcher/tree/docs/researcher-benchmark-preflight |
| OpenCUA / AgentNetBench | Static preflight plus evaluator-validity fixes for runtime package mutation, scroll scoring, key-sequence matching, and extra predicted actions | https://github.com/FU-max-boop/OpenCUA/tree/docs/agentnetbench-preflight |
| RAG-Anything | Zero-API-call preflight plus direct `content_list` integrity audit for image paths, captions/context, table/equation aliases, and chunk context indexing | https://github.com/FU-max-boop/RAG-Anything/tree/docs/raganything-preflight |
| DeepResearch-Eval | ReportEval preflight plus offline audit over 100 released Qwen reports, surfacing empty references, redundancy-risk pairs, and a zero topic-heading overlap candidate | https://github.com/FU-max-boop/DeepResearch-Eval/tree/docs/reporteval-preflight |
| LightRAG | RAGAS evaluation preflight plus offline retrieval audit showing top-k=1 partial coverage for the multi-document sample question and top-k=2 full recovery | https://github.com/FU-max-boop/LightRAG/tree/docs/eval-readiness-preflight |
| Spider2 | DBT benchmark preflight and agent-facing task briefs to separate setup failures from agent failures | https://github.com/FU-max-boop/Spider2/tree/docs/spider2-dbt-repro-clarity |
| Claw-Eval | Static scan over 300 autonomous-agent tasks to separate task readiness issues from model failures | https://github.com/FU-max-boop/claw-eval/tree/docs/claw-eval-preflight-anatomy |

## Candidate Queue

Strong next targets from the scan:

- AutoAgent / Auto-Deep-Research: autonomous research pipeline reproducibility
- GUIOdyssey / OSWorld-G / AgentTrek: GUI-agent benchmark readiness
- VideoRAG / MiniRAG: retrieval benchmark setup and evaluation hygiene

## Why This Matters

For many AI systems papers, the gap between "paper exists" and "new user can reproduce the benchmark or demo" is large. A useful research-engineering contribution is to make that gap visible and smaller: validate assumptions before expensive runs, produce clear blocker reports, and distinguish packaging/setup failures from real model or method failures.
