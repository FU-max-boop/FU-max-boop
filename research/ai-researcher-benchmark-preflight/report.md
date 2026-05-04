# AI-Researcher Preflight Report

- Generated at: `2026-05-04T14:46:05.569471+00:00`
- Status: `blocked`
- Env file: `/Users/fu/Desktop/ai study/builds/hku-ai-papers/AI-Researcher/.env.template`
- Benchmark records scanned: 1

| Status | Check | Detail |
| --- | --- | --- |
| `pass` | env_file | Loaded 17 key(s) from .env.template |
| `warn` | env_file_name | Using non-default env file: .env.template |
| `pass` | required_env | All required runtime env keys are present |
| `fail` | openrouter_api_key | OPENROUTER_API_KEY is missing or a placeholder for openrouter/* model(s) |
| `pass` | openrouter_api_base | OPENROUTER_API_BASE URL format is valid |
| `pass` | port | PORT is valid: 7020 |
| `pass` | max_iter_times | MAX_ITER_TIMES is valid: 0 |
| `pass` | task_level | TASK_LEVEL is `task1` |
| `pass` | cache_path | CACHE_PATH can be created under writable directory: /Users/fu/Desktop/ai study/builds/hku-ai-papers/AI-Researcher |
| `pass` | workplace_name | WORKPLACE_NAME can be created under writable directory: /Users/fu/Desktop/ai study/builds/hku-ai-papers/AI-Researcher |
| `pass` | benchmark_category | Benchmark category exists: vq |
| `pass` | benchmark_schema | Benchmark instance schema looks valid: /Users/fu/Desktop/ai study/builds/hku-ai-papers/AI-Researcher/benchmark/final/vq/one_layer_vq.json |
| `pass` | source_papers | 8 source paper(s) include reference and usage |
| `pass` | category_metaprompt | Dataset metaprompt exists for category `vq` |
| `fail` | python_dependencies | Missing package(s): litellm, loguru, browsergym, gradio, arxiv |
| `fail` | docker_command | Docker command is not available on PATH |
