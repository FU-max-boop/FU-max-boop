# RAG-Anything Preflight

This is a small research-engineering contribution for HKUDS RAG-Anything. I added a zero-API-call preflight utility so users can catch setup and configuration blockers before running multimodal document parsing and retrieval.

Published branch: https://github.com/FU-max-boop/RAG-Anything/tree/docs/raganything-preflight

## What It Checks

- input files, directories, and URLs
- supported and unsupported file extensions
- local `lightrag` install state
- selected parser runtime, including MinerU package/CLI
- LLM binding, host, and API-key environment variables
- embedding binding, host, and API-key environment variables
- numeric environment variables
- output and working directory writability

## Validation Result

The local dry run found real setup blockers without calling a model or parser:

- 6 supported files found
- missing editable/local `lightrag` install
- missing MinerU package/CLI
- missing LLM and embedding API keys
- text-to-PDF conversion warning for MinerU text/Markdown inputs

## Files

- `preflight_raganything.py`: proposed utility
- `report.md`: local validation report
- `report.json`: machine-readable report
- `0001-add-raganything-preflight-checks.patch`: patch for review
