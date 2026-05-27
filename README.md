# Hi, I'm Fu

I am building toward work as a student AI researcher / research engineer.

My strongest current signal is research engineering for AI evaluation systems:
I inspect benchmarks and RAG pipelines, find concrete failure modes, and turn
them into small, reviewable patches with offline validation.


## Current Research Artifact Track

I am staging a set of AI-evaluation research artifacts for public release after
the current review/anonymity gate clears. The common theme is claim-boundary
discipline: turning model and agent behavior claims into small runnable audits
with controls, smoke tests, result cards, and explicit limitations.

Current private artifact line:

- behavioral audits for whether model answers genuinely depend on supplied reasoning traces;
- executable-state diagnostics for coding-agent handoffs;
- claim-boundary audits for code-review feedback utility.

I am keeping the repositories private for now, but each is being prepared with a
README, quickstart, smoke test, result card, source/license notes, and privacy
scan before public release.

## Selected Evidence

### [OpenCUA AgentNetBench Evaluator Validity](research/opencua-agentnetbench-preflight)

I fixed evaluator-validity issues in a GUI-agent benchmark path. The evaluator
previously risked giving misleading scores for scroll direction, key-sequence
matching, extra predicted actions, and runtime package installation.

- Finding: opposite-direction scrolls could receive full credit; hotkey order
  and repeated keys were ignored; extra predicted actions were not penalized.
- Fix: added direction/amount-aware scroll scoring, sequence-preserving key
  matching, extra-action penalty, and a no-install edit-distance fallback.
- Validation: 6 offline regression tests plus sample AgentNetBench preflight.
- Upstream PR: https://github.com/xlang-ai/OpenCUA/pull/56
- Branch: https://github.com/FU-max-boop/OpenCUA/tree/docs/agentnetbench-preflight

### [DeepResearch-ReportEval Offline Audit](research/deepresearch-reporteval-preflight)

I audited all 100 released Qwen reports in HKUDS DeepResearch-Eval without LLM
or API calls, then surfaced corpus-level quality risks before paid judge calls.

- Finding: 79/100 reports contain empty reference entries; 82/100 trigger high
  redundancy-risk pairs; one report has zero topic-heading overlap.
- Example: a photosynthesis topic maps to a Tesla/BYD charging report title.
- Validation: deterministic CSV/JSON/Markdown audit outputs over the full
  released report corpus.
- Branch: https://github.com/FU-max-boop/DeepResearch-Eval/tree/docs/reporteval-preflight

### [RAG-Anything Content-List Alias Handling](research/raganything-content-list-aliases)

I split RAG-Anything's direct `content_list` insertion audit into a small
upstream behavior/schema fix for multimodal chunks.

- Finding: list processing could lose original content indexes and miss common
  table/equation aliases such as `table_data` and `latex`.
- Fix: preserved original content-list indexes, normalized captions/footnotes,
  and supported table/equation alias fields.
- Validation: offline regression tests for ordering, alias handling, and
  multimodal chunk preservation.
- Upstream PR: https://github.com/HKUDS/RAG-Anything/pull/273
- Branch: https://github.com/FU-max-boop/RAG-Anything/tree/docs/raganything-preflight

### [LightRAG Offline Retrieval Audit](research/lightrag-evaluation-preflight)

I added a deterministic retrieval sanity audit for the LightRAG RAGAS sample
questions before running LightRAG, RAGAS, embeddings, or LLM calls.

- Finding: top-k=1 only partially covers the single multi-document sample
  question; top-k=2 recovers all expected sample documents.
- Validation: BM25-style offline audit with recall@k, MRR, and generated
  top-1/top-2 reports.
- Upstream PR: https://github.com/HKUDS/LightRAG/pull/3038
- Branch: https://github.com/FU-max-boop/LightRAG/tree/docs/eval-readiness-preflight

### [claw-eval Fixture Row Validation](research/claw-eval-fixture-row-validation)

I tightened task fixture validation so benchmark setup problems are caught
before an agent run.

- Finding: `scripts/validate_tasks.py` checked required fixture fields only on
  the first fixture row.
- Fix: validate every fixture row and fail clearly on non-object rows.
- Validation: offline unit test plus targeted `T024*` validation.
- Upstream PR: https://github.com/claw-eval/claw-eval/pull/44

## Independent Research

### [mini-llm-lab](https://github.com/FU-max-boop/mini-llm-lab)

`mini-llm-lab` is my controlled mini-benchmark for studying when tiny causal
transformers genuinely use earlier context, and when they fall into shortcut
regimes.

Current result:

```text
0 clues visible -> local guessing
1 clue visible  -> stable single-clue shortcut regime
2 clues visible -> near-compositional use of both clues
```

It includes runnable experiment scripts, saved JSON results, result cards,
technical memos, a regenerated figure, and a public claim-audit script that
checks the result-card numbers against saved JSON artifacts.

Audited Stage 1 result over 5 seeds:

- visibility ladder: `0.016 -> 0.500 -> 0.980` held-out accuracy as the model
  sees `0`, `1`, then `2` clues
- shortcut diagnostic: shortcut failure drops from `1.000` with one clue to
  `0.041` with both clues visible
- bridge: a tiny `RoPE + RMSNorm + SwiGLU` decoder reaches `1.000` accuracy
  when both clues are visible

## Contribution Batch

I also scanned recent HKU AI-adjacent projects and built small, reviewable
research-engineering contributions where setup reliability, benchmark
readiness, and evaluation hygiene matter.

[HKU AI Paper Contribution Scout](research/hku-ai-paper-scout) summarizes the
batch across DeepCode, AI-Researcher, OpenCUA, RAG-Anything,
DeepResearch-Eval, LightRAG, Spider2, and Claw-Eval.

Additional work samples:

- [Spider2-DBT Preflight Analysis](research/spider2-dbt-preflight): found
  61/68 Spider2-DBT tasks evaluation-ready after local setup and generated
  agent-facing DBT task briefs.
- [Claw-Eval Static Task Preflight](research/claw-eval-preflight): scanned
  300 autonomous-agent task definitions to separate setup/task readiness issues
  from model-side failures.
- [DeepCode Config Preflight](research/deepcode-config-preflight): validated
  provider keys, MCP commands, dependency readiness, workspace paths, and model
  setup before agentic coding runs.
- [AI-Researcher Benchmark Preflight](research/ai-researcher-benchmark-preflight):
  checked benchmark instance schema, category metaprompts, workspace/cache
  paths, Docker availability, and runtime dependencies.

## Quality Bar

I only count a contribution as strong when it has:

1. a concrete failure mode or evaluation risk
2. a minimal reproducible artifact
3. offline validation when possible
4. a small patch or generated report a maintainer can review quickly
5. a written limitation: what the artifact proves and what it does not prove

## Direction

I am especially interested in the space between AI research and research
engineering: evaluation, interpretability-adjacent experiments, agentic
workflows, and tools that make model behavior easier to reason about.
