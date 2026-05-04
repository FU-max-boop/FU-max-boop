# DeepResearch-ReportEval Offline Audit

This is a research-engineering contribution for HKUDS DeepResearch-Eval. I first added a static preflight utility for report scoring and fact-checking, then extended the work into a full offline audit over the released 100 Qwen reports.

Published branch: https://github.com/FU-max-boop/DeepResearch-Eval/tree/docs/reporteval-preflight

## What It Adds

- static preflight for score/fact tasks
- README correction from topic-only JSONL to report JSONL for quality scoring
- offline corpus audit for all released Qwen reports
- citation/reference consistency checks
- topic-heading overlap diagnostics
- deterministic cross-section redundancy-risk proxy
- CSV, JSON, and Markdown audit outputs

## Full-Corpus Result

The offline audit scanned all 100 released reports without LLM/API calls.

- average report length: 3,633.97 words
- average sections per report: 6.94
- 79/100 reports contain empty reference entries
- 82/100 reports trigger high redundancy-risk pairs under the deterministic proxy
- 8/100 reports have low topic-heading overlap
- 1/100 report has zero topic-heading overlap

One notable candidate: report index 8 has topic “cytochrome complexes in the initial reactions of photosynthesis,” but the report title is “A Comparative Analysis of Tesla and BYD: The Battery and Charging Frontiers.”

The point is not to replace LLM judging. It is to triage the corpus before paid judge calls and surface data-level failure patterns that LLM scores alone may hide.

## Files

- `preflight_reporteval.py`: proposed utility
- `analyze_report_corpus.py`: offline audit script
- `score-preflight.md` / `score-preflight.json`: local score-task validation
- `fact-preflight.md` / `fact-preflight.json`: local fact-task validation
- `report_audit_summary.md` / `report_audit_summary.json`: full-corpus audit summary
- `report_audit_metrics.csv`: per-report metrics
- `0001-add-reporteval-preflight-checks.patch`: patch for review
- `0002-add-offline-report-corpus-audit.patch`: patch for review
