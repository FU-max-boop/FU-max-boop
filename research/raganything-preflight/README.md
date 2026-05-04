# RAG-Anything Content-List Audit + Preflight

This is a research-engineering contribution for HKUDS RAG-Anything. I first added a zero-API-call preflight utility so users can catch setup and configuration blockers before running multimodal document parsing and retrieval.

I then extended the contribution into the direct `content_list` insertion path: an offline integrity audit plus small schema/context fixes for multimodal chunks.

Published branch: https://github.com/FU-max-boop/RAG-Anything/tree/docs/raganything-preflight

## Content-List Contribution

The new audit checks pre-parsed `content_list` files before parser, LightRAG,
LLM, embedding, or VLM calls:

- required fields for text, image, table, and equation items
- image path existence, extension, size, symlink, and placeholder risk
- caption availability for multimodal items
- `table_body` / `table_data` compatibility
- `latex`, `text`, and `text_format` preservation for equation chunks
- page-index validity and nearby text-context availability

I also fixed a context-index issue: after `separate_content()` extracts only
multimodal items, chunk-mode context extraction now keeps each multimodal
item's original `content_list` index instead of using its compressed
multimodal-list index.

## Audit Finding

Running the audit on a sample direct-insertion list found real issues:

- 7 total items: 3 text, 1 image, 2 tables, 1 equation
- 2 blockers: placeholder image path and missing local image file
- 2 warnings: one table with no page-window text context, one equation missing `text_format`
- 1 multimodal item with no nearby text context

## Preflight Checks

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
- `audit_content_list.py`: offline content-list integrity audit
- `sample_content_list.json`: direct-insertion sample
- `content_list_audit_summary.md/json`: generated audit report
- `content_list_audit_items.csv`: item-level audit output
- `0002-add-content-list-integrity-audit.patch`: patch for review
