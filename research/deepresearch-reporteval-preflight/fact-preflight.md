# DeepResearch-ReportEval Preflight Report

- Generated at: `2026-05-04T14:31:26.111027+00:00`
- Status: `blocked`
- Task: `fact`
- Provider: `jina`
- Input path: `/Users/fu/Desktop/ai study/builds/hku-ai-papers/DeepResearch-Eval/example/judge_fact_result/example_fact_judge_input.jsonl`
- Output path: `/Users/fu/Desktop/ai study/builds/hku-ai-papers/DeepResearch-Eval/example/judge_fact_result/example_fact_judge_output.jsonl`
- Records scanned: 1

| Status | Check | Detail |
| --- | --- | --- |
| `fail` | dependencies | Missing package(s): json-repair, dashscope, firecrawl-python |
| `fail` | openai_api_key | OPENAI_API_KEY is missing or a placeholder |
| `warn` | openai_api_base | OPENAI_API_BASE is unset or a placeholder; default OpenAI endpoint will be used |
| `warn` | firecrawl_env_alias | Found FIRECRAWL_API_KEY, but Atools.py reads FIRECRAWL_KEY |
| `fail` | jina_api_key | JINA_API_KEY is missing or a placeholder |
| `pass` | jsonl_parse | Parsed 1 JSONL record(s) |
| `pass` | input_schema | `fact` input schema looks valid |
| `pass` | output_path | Output parent is writable: /Users/fu/Desktop/ai study/builds/hku-ai-papers/DeepResearch-Eval/example/judge_fact_result |
