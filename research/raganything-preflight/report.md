# RAG-Anything Preflight Report

- Generated at: `2026-05-04T14:25:42.653840+00:00`
- Status: `blocked`
- Parser: `mineru`
- Parse method: `auto`
- Input paths: `README.md, docs`
- Supported files: 6
- Unsupported files: 0

## Checks

| Status | Check | Detail |
| --- | --- | --- |
| `pass` | input_paths | All input paths exist or are valid URLs |
| `pass` | supported_inputs | Found 6 supported file(s) |
| `pass` | unsupported_inputs | No unsupported files found |
| `fail` | core_dependencies | Missing package(s): lightrag. Install with `pip install -e .`. |
| `pass` | parser_selection | MinerU parser; Office files may also require LibreOffice/soffice. |
| `pass` | parse_method | Parse method is `auto` |
| `fail` | parser_runtime | missing package(s): mineru; missing command(s): mineru |
| `warn` | text_conversion | Text/Markdown inputs are present. Install `reportlab` if using MinerU text-to-PDF conversion. |
| `pass` | llm_binding | llm binding is `openai` |
| `warn` | llm_host | llm host is not set |
| `fail` | llm_api_key | llm API key is missing or still a placeholder |
| `pass` | embedding_binding | embedding binding is `openai` |
| `warn` | embedding_host | embedding host is not set |
| `fail` | embedding_api_key | embedding API key is missing or still a placeholder |
| `pass` | numeric_environment | Numeric environment variables look valid |
| `pass` | output_dir | output_dir parent is writable: /Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything |
| `pass` | working_dir | working_dir parent is writable: /Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything |

## Supported Files

- `/Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything/README.md`
- `/Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything/docs/offline_setup.md`
- `/Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything/docs/batch_processing.md`
- `/Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything/docs/enhanced_markdown.md`
- `/Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything/docs/vllm_integration.md`
- `/Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything/docs/context_aware_processing.md`
