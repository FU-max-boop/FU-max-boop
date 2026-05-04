# DeepCode Preflight Report

- Generated at: `2026-05-04T14:38:49.343902+00:00`
- Status: `blocked`
- Config path: `/Users/fu/Desktop/ai study/builds/hku-ai-papers/DeepCode/deepcode_config.json.example`

| Status | Check | Detail |
| --- | --- | --- |
| `pass` | config_json | Configuration JSON parsed successfully |
| `warn` | config_name | Using non-default config file: deepcode_config.json.example |
| `fail` | env_refs | Unset environment reference(s): OPENAI_API_KEY |
| `pass` | providers | Configured provider entries: anthropic, dashscope, deepseek, gemini, ollama, openai, openrouter, vllm, zhipu |
| `fail` | active_provider_keys | Missing or placeholder API key for active provider(s): openai |
| `pass` | provider_api_base | Configured provider apiBase values look valid |
| `fail` | python_dependencies | Missing package(s): aiofiles, aiohttp, fastapi, json-repair, loguru, mcp, pydantic-settings, uvicorn |
| `fail` | mcp_commands | Missing command(s): fetch:uvx |
| `pass` | mcp_script_files | Configured Python MCP server scripts exist |
| `pass` | default_search_server | defaultSearchServer `filesystem` is configured |
| `pass` | workspace_root | Workspace root can be created under writable directory: /Users/fu/Desktop/ai study/builds/hku-ai-papers/DeepCode |
| `pass` | workspace_max_input | workspace.maxInputMb is 100 |
