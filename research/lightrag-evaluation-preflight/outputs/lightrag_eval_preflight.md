# LightRAG Evaluation Preflight Report

- Generated at: `2026-05-04T14:11:44.236432+00:00`
- Status: `blocked`
- Dataset: `/Users/fu/Desktop/ai study/builds/hkuds-ra/LightRAG/lightrag/evaluation/sample_dataset.json`
- Documents directory: `/Users/fu/Desktop/ai study/builds/hkuds-ra/LightRAG/lightrag/evaluation/sample_documents`
- LightRAG endpoint: `http://localhost:9621`

## Summary

- Passed checks: 9
- Warnings: 0
- Blockers: 3

## Checks

| Status | Check | Detail |
| --- | --- | --- |
| `pass` | dataset_cases | Found 6 test case(s) in sample_dataset.json |
| `pass` | dataset_required_fields | Every test case has `question` and `ground_truth` fields |
| `pass` | dataset_empty_fields | No required fields are empty |
| `pass` | dataset_duplicate_questions | No duplicate questions |
| `pass` | dataset_placeholder_content | No template placeholders |
| `pass` | dataset_project_labels | All cases include project labels |
| `pass` | documents_non_empty | Found 6 non-empty document file(s) |
| `fail` | evaluation_dependencies | Missing package(s): datasets, ragas, langchain-openai. Install with `pip install -e ".[evaluation]"`. |
| `fail` | llm_api_key | Set EVAL_LLM_BINDING_API_KEY or OPENAI_API_KEY before running RAGAS |
| `fail` | embedding_api_key | Set EVAL_EMBEDDING_BINDING_API_KEY, EVAL_LLM_BINDING_API_KEY, or OPENAI_API_KEY |
| `pass` | evaluation_numeric_env | EVAL_MAX_CONCURRENT=2, EVAL_QUERY_TOP_K=10 |
| `pass` | rag_endpoint_format | Endpoint has a valid http(s) URL format. Connectivity is not checked. |
