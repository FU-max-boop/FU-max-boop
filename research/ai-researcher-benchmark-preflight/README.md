# AI-Researcher Benchmark Preflight

This is a small research-engineering contribution for HKUDS AI-Researcher. I added a static preflight utility for benchmark runs and corrected a Docker image typo in the README.

Published branch: https://github.com/FU-max-boop/AI-Researcher/tree/docs/researcher-benchmark-preflight

## What It Checks

- `.env` required runtime keys
- OpenRouter model/API-key consistency
- OpenRouter base URL format
- port, task level, and iteration count
- cache/workspace path writability
- benchmark category and instance existence
- benchmark JSON schema
- `source_papers` structure
- category metaprompt availability
- core Python dependencies
- Docker command availability

## Validation Result

Running the preflight on `.env.template` validated the default `vq/one_layer_vq` benchmark path and caught expected local blockers:

- `OPENROUTER_API_KEY` is still a placeholder
- benchmark schema is valid
- 8 source papers include reference and usage fields
- category metaprompt exists
- several optional/runtime packages are not installed in this local shell
- Docker is not available on PATH

## Files

- `preflight_ai_researcher.py`: proposed utility
- `report.md`: local validation report
- `report.json`: machine-readable report
- `0001-add-ai-researcher-benchmark-preflight-checks.patch`: patch for review
