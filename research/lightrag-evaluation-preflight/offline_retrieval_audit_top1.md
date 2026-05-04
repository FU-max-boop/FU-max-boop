# LightRAG Offline Retrieval Audit

- Generated at: `2026-05-04T15:31:05.970776+00:00`
- Dataset: `/Users/fu/Desktop/ai study/builds/hkuds-ra/LightRAG/lightrag/evaluation/sample_dataset.json`
- Documents: `/Users/fu/Desktop/ai study/builds/hkuds-ra/LightRAG/lightrag/evaluation/sample_documents`
- Oracle: `/Users/fu/Desktop/ai study/builds/hkuds-ra/LightRAG/lightrag/evaluation/sample_retrieval_oracle.json`
- Top-k: 1
- Queries: 6
- Average recall@k: 0.917
- Mean reciprocal rank: 1.000
- Full-recall queries: 5/6
- No-hit queries: 0
- Multi-document queries: 1

## Query Results

| # | Recall@k | MRR | Expected | Top Documents | Question |
| ---: | ---: | ---: | --- | --- | --- |
| 1 | 1.000 | 1.000 | `01_lightrag_overview.md` | 01_lightrag_overview.md (9.17) | How does LightRAG solve the hallucination problem in large language models? |
| 2 | 1.000 | 1.000 | `02_rag_architecture.md` | 02_rag_architecture.md (8.19) | What are the three main components required in a RAG system? |
| 3 | 1.000 | 1.000 | `03_lightrag_improvements.md` | 03_lightrag_improvements.md (7.06) | How does LightRAG's retrieval performance compare to traditional RAG approaches? |
| 4 | 1.000 | 1.000 | `04_supported_databases.md` | 04_supported_databases.md (4.68) | What vector databases does LightRAG support and what are their key characteristics? |
| 5 | 1.000 | 1.000 | `05_evaluation_and_deployment.md` | 05_evaluation_and_deployment.md (9.70) | What are the four key metrics for evaluating RAG system quality and what does each metric measure? |
| 6 | 0.500 | 1.000 | `01_lightrag_overview.md, 03_lightrag_improvements.md` | 03_lightrag_improvements.md (6.73) | What are the core benefits of LightRAG and how does it improve upon traditional RAG systems? |
