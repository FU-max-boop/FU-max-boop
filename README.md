# Fu Xiaonan

**LLM evaluation · agent reliability · post-training research engineering**

Hong Kong · The University of Hong Kong · Mathematics (second major)

[Résumé](./assets/Fu_Xiaonan_LLM_Research_Engineering_Resume.pdf) ·
[Research & engineering portfolio](https://github.com/FU-max-boop/ai-eval-artifacts) ·
[LinkedIn](https://www.linkedin.com/in/xiaonan-fu-734a20339/) ·
[ORCID](https://orcid.org/0009-0000-6423-7814)

I am an HKU undergraduate studying Economics & Finance with a second major in
Mathematics, and a research engineer working on reproducible ways to evaluate
LLM behavior, preserve executable state in agent systems, and test post-training
claims. I currently contribute to AI agent development and evaluation at Tencent
and conduct research at HKU's Centre of AI, Management and Organization.

## Evidence at a glance

- **Research:** two sole-authored papers accepted to non-archival workshops at
  COLM 2026, on post-training trace reliance and executable agent state.
- **Open source:** 15 merged pull requests across 12 AI/software repositories
  as of August 2026, including MLX, OpenAI Agents, OpenAI Node, Pydantic AI,
  OpenCUA, LightRAG, RAG-Anything, LoopGain, Agno, txtai, and xberg.
- **Research engineering:** public, runnable evaluation artifacts with smoke
  checks, result cards, counterfactual controls, and explicit claim boundaries.

## Featured engineering impact

### AgentRunProof: deterministic runtime contracts for OpenAI Agents

I built [AgentRunProof](https://github.com/FU-max-boop/agentrunproof) to reproduce
`Runner` and `RunState` failures without model-provider requests and to preserve
the observations as content-addressed evidence. My RunState isolation report and
AgentRunProof validation were cited by the maintainer-authored fixes
[openai-agents-python#4413](https://github.com/openai/openai-agents-python/pull/4413)
and
[#4414](https://github.com/openai/openai-agents-python/pull/4414), covering the
original sibling-state defect and its recursively nested approval case.

[PyPI](https://pypi.org/project/agentrunproof/) ·
[RunState case study](https://github.com/FU-max-boop/agentrunproof/blob/main/docs/case-study-runstate.md)

The project is also listed in the externally maintained
[awesome-auditable-ai](https://github.com/yzhao062/awesome-auditable-ai#tools-and-platforms)
collection.

This is upstream diagnostic and validation impact—not OpenAI adoption or
endorsement of the library.

### ML systems: Metal reduction correctness in MLX

My merged [MLX #4267](https://github.com/ml-explore/mlx/pull/4267) fixes
incorrect Metal reduction results on negative-stride views by correcting
signed pointer arithmetic, with cross-backend regression coverage.

## Selected research

### StateBind: Evaluating Executable Agent State Across Context Windows and Handoffs

Accepted poster, **Context Beyond the Window — COLM 2026 Workshop**
(sole author; non-archival).

[Paper](https://openreview.net/forum?id=WVZuCW4s1q) ·
[Code](https://github.com/FU-max-boop/statebind-guard)

Tests whether agent handoffs preserve the bindings required to resume work—not
merely identifiers or visible text—and packages the failure cases as an
executable reliability gate.

### Trace-Use Audits as Measurement: Interventional Evaluation of Post-Training Trace Reliance

Accepted, **AIMS — COLM 2026 Workshop** (sole author; non-archival).

[Paper](https://openreview.net/forum?id=SKdjnqHJ8S) ·
[Code](https://github.com/FU-max-boop/traceuse-audit-public)

Uses interventions and controls to distinguish behavioral reliance on supplied
traces from surface-level imitation of trace form.

## Open-source engineering

My contributions focus on evaluator correctness, tool-call identity, multimodal
data handling, retrieval checks, schema behavior, and deterministic tests.

Selected merged work:

- [ml-explore/mlx#4267](https://github.com/ml-explore/mlx/pull/4267) — fix Metal row reductions on negative-stride views.
- [openai/openai-agents-python#4361](https://github.com/openai/openai-agents-python/pull/4361) — honor WAV sample width when decoding audio.
- [pydantic/pydantic-ai#5355](https://github.com/pydantic/pydantic-ai/pull/5355) — preserve xAI tool-result IDs.
- [xlang-ai/OpenCUA#56](https://github.com/xlang-ai/OpenCUA/pull/56) — fix AgentNetBench evaluator scoring edge cases.
- [HKUDS/LightRAG#3038](https://github.com/HKUDS/LightRAG/pull/3038) — add an offline sample-retrieval check for RAGAS evaluation.
- [HKUDS/RAG-Anything#273](https://github.com/HKUDS/RAG-Anything/pull/273) and [#278](https://github.com/HKUDS/RAG-Anything/pull/278) — preserve multimodal aliases and correct duplicate detection.
- [openai/openai-node#1903](https://github.com/openai/openai-node/pull/1903) — sanitize Zod definition references.
- [loopgain-ai/loopgain#14](https://github.com/loopgain-ai/loopgain/pull/14) — exercise its OpenAI Agents adapter through the real Runner offline.

<details>
<summary>All 15 merged upstream pull requests</summary>

- [ml-explore/mlx#4267](https://github.com/ml-explore/mlx/pull/4267) — Metal negative-stride row reductions
- [yzhao062/awesome-auditable-ai#12](https://github.com/yzhao062/awesome-auditable-ai/pull/12) — add AgentRunProof to the curated tooling list
- [loopgain-ai/loopgain#14](https://github.com/loopgain-ai/loopgain/pull/14) — real OpenAI Agents Runner regression test
- [HKUDS/RAG-Anything#327](https://github.com/HKUDS/RAG-Anything/pull/327) — configurable recursive batch scanning
- [openai/openai-agents-python#4361](https://github.com/openai/openai-agents-python/pull/4361) — audio sample-width handling
- [xberg-io/xberg#1413](https://github.com/xberg-io/xberg/pull/1413) — slide page-number preservation
- [neuml/txtai#1183](https://github.com/neuml/txtai/pull/1183) — OpenAI chat-model selection
- [openai/openai-node#1903](https://github.com/openai/openai-node/pull/1903) — Zod definition-reference sanitization
- [agno-agi/agno#8145](https://github.com/agno-agi/agno/pull/8145) — RemoteTeam knowledge-filter attributes
- [pydantic/pydantic-ai#5533](https://github.com/pydantic/pydantic-ai/pull/5533) — deterministic `Retry-After` testing
- [HKUDS/RAG-Anything#278](https://github.com/HKUDS/RAG-Anything/pull/278) — duplicate detection
- [pydantic/pydantic-ai#5355](https://github.com/pydantic/pydantic-ai/pull/5355) — xAI tool-result identity
- [HKUDS/RAG-Anything#273](https://github.com/HKUDS/RAG-Anything/pull/273) — multimodal content-list aliases
- [HKUDS/LightRAG#3038](https://github.com/HKUDS/LightRAG/pull/3038) — offline retrieval evaluation
- [xlang-ai/OpenCUA#56](https://github.com/xlang-ai/OpenCUA/pull/56) — evaluator scoring boundaries

</details>

[View all of my merged pull requests](https://github.com/pulls?q=is%3Apr+author%3AFU-max-boop+is%3Amerged)

## What I build

- Evaluation harnesses for LLM and agent behavior
- Reliability checks for tool use, state transfer, and data pipelines
- Post-training diagnostics with intervention-based controls
- Reproducible Python research infrastructure and regression tests

The standard I aim for is simple: a concrete failure mode, a minimal
reproduction, a meaningful control, a runnable check, and a precise statement
of what the evidence does—and does not—establish.

## Contact

The best public way to reach me is
[LinkedIn](https://www.linkedin.com/in/xiaonan-fu-734a20339/). I do not publish
personal email or phone details on this profile.
