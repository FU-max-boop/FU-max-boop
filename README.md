# Fu Xiaonan

HKU mathematics undergraduate building toward AI evaluation and research
engineering.

I work on small, runnable audits for places where AI systems look correct on
the surface but may be relying on the wrong thing: traces that are imitated but
not used, agent handoffs that expose identifiers but lose executable state, and
code-review feedback whose utility claim is broader than the evidence supports.

**Current direction:** AI eval, agent reliability, post-training behavior, and
research engineering.

**Fast proof check:** the repositories below are meant to be run, not just read.
Each flagship artifact has a quickstart, a smoke/public check, generated result
cards, and an explicit claim boundary.

## Public Research Artifacts

| Artifact | What it tests | Runnable gate |
| --- | --- | --- |
| [TraceUseAudit](https://github.com/FU-max-boop/traceuse-audit-public) | Whether final answers behaviorally depend on supplied traces, rather than only matching trace form. | `make public-check` |
| [StateBind Guard](https://github.com/FU-max-boop/statebind-guard) | Whether coding-agent handoffs preserve executable state bindings, not just visible names. | `bash scripts/check_public_ready.sh` |
| [Claim-Boundary Audit](https://github.com/FU-max-boop/claim-boundary-audit-public) | Whether code-review feedback supports local utility, transfer utility, or only a narrower claim. | `make public-check` |

Portfolio landing page:
[ai-eval-artifacts](https://github.com/FU-max-boop/ai-eval-artifacts)

One-page pitch:
[Internship / Research Engineering Pitch](https://github.com/FU-max-boop/ai-eval-artifacts/blob/main/docs/internship_research_engineering_pitch.md)

If you are scanning for internship / research-engineering fit, start with
`StateBind Guard` for coding-agent reliability and `TraceUseAudit` for LLM
trace-use evaluation. Those are the two flagship proof assets.

## Open-Source Engineering Signal

Merged upstream PRs:

- [xlang-ai/OpenCUA#56](https://github.com/xlang-ai/OpenCUA/pull/56):
  fixed AgentNetBench evaluator scoring edge cases.
- [HKUDS/LightRAG#3038](https://github.com/HKUDS/LightRAG/pull/3038):
  added an offline sample retrieval check for RAGAS evaluation.
- [HKUDS/RAG-Anything#273](https://github.com/HKUDS/RAG-Anything/pull/273):
  preserved content-list aliases in multimodal chunks.
- [HKUDS/RAG-Anything#278](https://github.com/HKUDS/RAG-Anything/pull/278):
  fixed content-list duplicate detection.
- [pydantic/pydantic-ai#5355](https://github.com/pydantic/pydantic-ai/pull/5355):
  preserved xAI tool result IDs and updated the xAI SDK constraint.

Open / review-stage PRs include work in
[pydantic-ai](https://github.com/pydantic/pydantic-ai/pulls?q=is%3Apr+author%3AFU-max-boop),
[modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk/pulls?q=is%3Apr+author%3AFU-max-boop),
[microsoft/markitdown](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+author%3AFU-max-boop),
[browser-use](https://github.com/browser-use/browser-use/pulls?q=is%3Apr+author%3AFU-max-boop),
and [claw-eval](https://github.com/claw-eval/claw-eval/pulls?q=is%3Apr+author%3AFU-max-boop).

## Research Engineering Taste

I try to make each artifact pass five gates:

1. concrete failure mode or evaluation risk
2. minimal reproducible example
3. baseline or counterfactual control
4. generated result card
5. explicit claim boundary: what the evidence proves and what it does not

The work I want more of: compact evaluations, agent reliability tooling,
post-training diagnostics, and OSS infrastructure where careful measurement
changes engineering decisions.
