# AgentNetBench Preflight Report

- Generated at: `2026-05-04T14:23:22.535075+00:00`
- Status: `ready`
- Data directory: `/Users/fu/Desktop/ai study/builds/hku-ai-papers/OpenCUA/evaluation/agentnetbench/sample_data`
- Image directory: `/Users/fu/Desktop/ai study/builds/hku-ai-papers/OpenCUA/evaluation/agentnetbench/sample_data/images`
- Model: `opencua-7b`
- Base URL: `http://localhost:8000/v1`
- Trajectories scanned: 5
- Steps scanned: 54

## Summary

- Passed checks: 12
- Warnings: 1
- Blockers: 0

## Checks

| Status | Check | Detail |
| --- | --- | --- |
| `pass` | trajectory_json | Parsed 5 JSON file(s) |
| `pass` | image_dir | Image directory exists: /Users/fu/Desktop/ai study/builds/hku-ai-papers/OpenCUA/evaluation/agentnetbench/sample_data/images |
| `pass` | trajectory_required_fields | All required trajectory fields are present |
| `pass` | trajectory_step_shapes | Step and alternative-option shapes look valid |
| `pass` | trajectory_images | Every step image exists in the image directory |
| `pass` | action_coordinates | Relative coordinates are within [0, 1] |
| `pass` | action_types | All action types are recognized by the static checker |
| `pass` | duplicate_task_ids | No duplicate task_id values |
| `pass` | runtime_dependencies | All AgentNetBench runtime packages are importable: openai>=1.0.0, pillow |
| `warn` | optional_dependencies | Missing optional package(s): editdistance. The evaluator can install editdistance on demand, but preinstalling it avoids runtime side effects. |
| `pass` | agent_selection | `opencua-7b` selects the OpenCUA agent |
| `pass` | base_url | Base URL has a valid http(s) format |
| `pass` | api_key | API key is configured |
