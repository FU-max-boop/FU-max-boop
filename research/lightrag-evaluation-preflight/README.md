# LightRAG Offline Retrieval Audit + Evaluation Preflight

This is a research-engineering contribution around LightRAG, an HKUDS RAG
project associated with Professor Chao Huang.

I first added a zero-API-call preflight utility for the RAGAS evaluation
workflow. I then added an offline retrieval sanity audit for the bundled sample
questions and documents, so users can check whether the sample evaluation task
itself is retrievable before running LightRAG, RAGAS, embeddings, or LLM calls.

## Published Code

- Fork branch: https://github.com/FU-max-boop/LightRAG/tree/docs/eval-readiness-preflight
- Upstream compare view: https://github.com/HKUDS/LightRAG/compare/main...FU-max-boop:LightRAG:docs/eval-readiness-preflight

## What It Checks

### Offline Retrieval Audit

- maps each sample question to expected sample document(s)
- ranks sample documents with a deterministic BM25-style lexical scorer
- reports recall@k, hit@k, MRR, and first expected-document rank
- identifies multi-document questions that need more than top-1 retrieval

### Evaluation Preflight

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

The offline retrieval audit found:

- top-k=1: average recall@1 = 0.917, with the single multi-document question
  only partially covered
- top-k=2: average recall@2 = 1.000 and full recall for all 6 sample questions
- 0 no-hit queries in both runs

## Files

- `report.md`: mini contribution report
- `offline_retrieval_audit.py`: proposed offline retrieval audit
- `sample_retrieval_oracle.json`: sample question-to-document oracle
- `test_offline_retrieval_audit.py`: regression test for the audit
- `offline_retrieval_audit_top1.md/json`: generated top-1 audit report
- `offline_retrieval_audit_top2.md/json`: generated top-2 audit report
- `0002-add-offline-retrieval-audit.patch`: patch generated from the pushed fork branch
