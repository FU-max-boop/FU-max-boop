# LightRAG Evaluation Preflight

This is a small research-engineering contribution around LightRAG, an HKUDS RAG
project associated with Professor Chao Huang.

I added a zero-API-call preflight utility for the RAGAS evaluation workflow. The
goal is to catch local readiness problems before users spend time or model API
budget on evaluation runs.

## Published Code

- Fork branch: https://github.com/FU-max-boop/LightRAG/tree/docs/eval-readiness-preflight
- Upstream compare view: https://github.com/HKUDS/LightRAG/compare/main...FU-max-boop:LightRAG:docs/eval-readiness-preflight

## What It Checks

- Dataset JSON exists and has a `test_cases` list.
- Each test case has non-empty `question` and `ground_truth` fields.
- Duplicate questions and template placeholders are surfaced as warnings.
- Sample documents are present and non-empty.
- RAGAS evaluation dependencies are importable.
- Required LLM and embedding API keys are configured.
- Numeric environment variables and the LightRAG endpoint URL are valid.

## Local Snapshot

The sample dataset and sample documents passed structural checks. My local
environment was correctly reported as blocked because evaluation dependencies
and API keys were not configured.

## Files

- `report.md`: mini contribution report
- `tools/preflight_eval_readiness.py`: proposed preflight utility
- `docs/README_EVALUATION_PREFLIGHT.md`: proposed documentation
- `outputs/`: JSON and Markdown preflight reports
- `patches/`: patch generated from the pushed fork branch
