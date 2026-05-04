# DeepCode Config Preflight

This is a small research-engineering contribution for HKUDS DeepCode. I added a static preflight utility that checks whether a local DeepCode configuration is ready before launching the CLI/UI, MCP servers, or model calls.

Published branch: https://github.com/FU-max-boop/DeepCode/tree/docs/deepcode-config-preflight

## What It Checks

- `deepcode_config.json` parseability
- `${ENV_VAR}` references
- active provider and API-key readiness
- provider `apiBase` URL format
- core Python dependencies
- MCP server command availability
- MCP Python script paths
- `defaultSearchServer` consistency
- workspace path writability and `maxInputMb`

## Validation Result

Running the preflight on `deepcode_config.json.example` caught expected local setup blockers:

- `OPENAI_API_KEY` is referenced but unset
- active OpenAI provider key is missing
- several core packages are not installed in this local shell
- `uvx` is missing for the fetch MCP server
- workspace path is creatable
- MCP Python server scripts exist

## Files

- `preflight_deepcode.py`: proposed utility
- `report.md`: local validation report
- `report.json`: machine-readable report
- `0001-add-deepcode-config-preflight-checks.patch`: patch for review
