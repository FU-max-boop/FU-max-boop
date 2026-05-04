# LightRAG Evaluation Preflight Contribution

## Target

- Professor / lab: Chao Huang, HKUDS, The University of Hong Kong
- Project: LightRAG: Simple and Fast Retrieval-Augmented Generation
- Official repository: https://github.com/HKUDS/LightRAG
- Paper: https://arxiv.org/abs/2410.05779

## Problem

LightRAG now includes a RAGAS-based evaluation workflow. Before users can run
the evaluator, several setup assumptions must all be true:

- The evaluation dataset must follow the expected `test_cases` schema.
- Sample or user documents should already be indexed into a LightRAG instance.
- RAGAS-related dependencies must be installed.
- LLM and embedding API keys must be configured correctly.
- Numeric environment variables and the LightRAG endpoint URL must be valid.

Without a lightweight readiness check, many users discover these issues only
after launching an expensive or long-running RAGAS evaluation.

## Contribution

I added a static preflight utility for the evaluation workflow:

- `lightrag/evaluation/preflight_eval_readiness.py`
- `lightrag/evaluation/README_EVALUATION_PREFLIGHT.md`
- A short preflight entry in `lightrag/evaluation/README_EVALUASTION_RAGAS.md`

The preflight tool does not call the LightRAG API, start a server, or call LLM
and embedding models. It checks the local readiness surface before users spend
time or API budget on evaluation.

## Local Result

Command:

```bash
python3 lightrag/evaluation/preflight_eval_readiness.py \
  --output-json /Users/fu/Desktop/ai\ study/research/hkuds-ra/lightrag-preflight/lightrag_eval_preflight.json \
  --output-md /Users/fu/Desktop/ai\ study/research/hkuds-ra/lightrag-preflight/lightrag_eval_preflight.md
```

Observed result in my local environment:

- Dataset structure: pass
- Required `question` and `ground_truth` fields: pass
- Empty required fields: pass
- Duplicate questions: pass
- Placeholder content: pass
- Project labels: pass
- Sample documents: 6 non-empty files found
- Endpoint URL format: pass
- Blockers surfaced early:
  - Missing local evaluation packages: `datasets`, `ragas`, `langchain-openai`
  - Missing LLM evaluation API key
  - Missing embedding evaluation API key

## Why This Helps

This is a small research-engineering contribution, but it targets a real
maintenance and reproducibility bottleneck:

- It gives new users a safer path into LightRAG evaluation.
- It makes configuration failures explicit and machine-readable.
- It can be used in CI with `--strict`.
- It creates JSON/Markdown reports that are easier to attach to issues,
  reproduction notes, or benchmark runs.

## Next Possible Extension

If the maintainers find this useful, the next extension would be an optional
`--check-server` mode that performs a lightweight `/health` or `/query` dry-run
against a local LightRAG server. I intentionally left network/API calls out of
the first version to keep the default preflight safe and zero-cost.
