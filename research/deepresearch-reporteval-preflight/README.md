# DeepResearch-ReportEval Preflight

This is a small research-engineering contribution for HKUDS DeepResearch-Eval. I added a static preflight utility for report scoring and fact-checking, and corrected the README quality-scoring example to use report JSONL input instead of topic-only JSONL input.

Published branch: https://github.com/FU-max-boop/DeepResearch-Eval/tree/docs/reporteval-preflight

## What It Checks

- documented Python dependencies
- OpenAI-compatible environment variables
- Firecrawl/Jina provider key configuration
- score-task JSONL schema: `topic` and `report`
- fact-task JSONL schema: URL key and `contexts`
- output path writability or creatability

## Validation Result

The preflight caught a meaningful reproduction issue: `judge_score.py` requires each JSONL row to contain both `topic` and `report`, while the topic dataset only contains topics. The contribution updates the quick-start path to `data/report/qwen-reports.jsonl`, which matches the scoring script.

Local reports:

- score preflight scanned 100 report records and validated the score input schema
- fact preflight scanned 1 example record and validated the fact-checking input schema
- remaining blockers are expected local setup issues: missing dependencies and missing API keys

## Files

- `preflight_reporteval.py`: proposed utility
- `score-preflight.md` / `score-preflight.json`: local score-task validation
- `fact-preflight.md` / `fact-preflight.json`: local fact-task validation
- `0001-add-reporteval-preflight-checks.patch`: patch for review
