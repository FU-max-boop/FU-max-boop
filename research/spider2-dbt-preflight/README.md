# Spider2-DBT Preflight Analysis

Small research-engineering contribution around [Spider2](https://github.com/xlang-ai/Spider2), focused on reproducibility and agent-facing context construction for Spider2-DBT.

## Summary

I reproduced the Spider2-DBT setup/evaluation path, found DBT asset/metadata inconsistencies that affect local evaluation, and built lightweight preflight tooling that separates benchmark packaging failures from genuine agent failures before expensive model runs.

## What I Reproduced

- Cloned `xlang-ai/Spider2` at commit `01a4c67c`.
- Downloaded the official Spider2-DBT data zips.
- Ran `python setup.py` under `spider2-dbt`.
- Verified both Spider2-DBT JSONL files contain 68 tasks.
- Ran a DuckDB evaluation smoke test for `playbook001`.
- Evaluator output: `1.0 1 1`.

Limitation: I did not run the full Spider-Agent DBT pipeline because Docker was not installed on my local machine.

## Contribution

### 1. Reproduction Docs Patch

I prepared two local commits on a fork branch:

- `42f3596f Clarify Spider2-DBT reproduction docs`
- `a86ac8c6 Add Spider2-DBT preflight asset checker`

Fork branch:

- [`FU-max-boop/Spider2:docs/spider2-dbt-repro-clarity`](https://github.com/FU-max-boop/Spider2/tree/docs/spider2-dbt-repro-clarity)

Patch files:

- [`patches/0001-Clarify-Spider2-DBT-reproduction-docs.patch`](patches/0001-Clarify-Spider2-DBT-reproduction-docs.patch)
- [`patches/0002-Add-Spider2-DBT-preflight-asset-checker.patch`](patches/0002-Add-Spider2-DBT-preflight-asset-checker.patch)

### 2. Asset Consistency Finding

After setup, I compared JSONL task ids, downloaded start DuckDB directories, gold DuckDB directories, and the exact gold filenames referenced by `spider2_eval.jsonl`.

Aggregate result:

- JSONL tasks: 68
- evaluation-ready tasks: 61
- blocked or metadata-inconsistent tasks: 7

Blocked / inconsistent tasks:

| instance_id | issue |
| --- | --- |
| `gitcoin001` | missing start DuckDB, missing gold dir, missing expected `gitcoin.duckdb` |
| `airbnb002` | missing gold dir / expected `airbnb.duckdb` |
| `biketheft001` | missing gold dir / expected `biketheft.duckdb` |
| `google_ads001` | missing gold dir / expected `google_ads.duckdb` |
| `social_media001` | metadata expects `social_media_reporting__rollup_report.duckdb`, but setup creates `social_media.duckdb` |
| `xero_new001` | metadata expects `xero.duckdb`, but setup creates `xero_new.duckdb` |
| `xero_new002` | metadata expects `xero.duckdb`, but setup creates `xero_new.duckdb` |

Extra asset directory not referenced by JSONL:

- `danish_democracy_data001`

### 3. Preflight Tooling

Tools:

- [`tools/check_spider2_dbt_assets.py`](tools/check_spider2_dbt_assets.py): checks whether JSONL ids and DuckDB assets match.
- [`tools/analyze_spider2_dbt_tasks.py`](tools/analyze_spider2_dbt_tasks.py): creates a task-level CSV and Markdown report with static DBT features.
- [`tools/build_dbt_task_brief.py`](tools/build_dbt_task_brief.py): generates an agent-facing brief for a specific DBT task.

Outputs:

- [`outputs/spider2_dbt_preflight_summary.md`](outputs/spider2_dbt_preflight_summary.md)
- [`outputs/spider2_dbt_preflight_tasks.csv`](outputs/spider2_dbt_preflight_tasks.csv)
- [`outputs/task-briefs/jira001.md`](outputs/task-briefs/jira001.md)
- [`outputs/task-briefs/quickbooks001.md`](outputs/task-briefs/quickbooks001.md)
- [`outputs/task-briefs/playbook001.md`](outputs/task-briefs/playbook001.md)
- [`outputs/task-briefs/gitcoin001-blocked.md`](outputs/task-briefs/gitcoin001-blocked.md)

## Why This Matters

Spider2-DBT is an agent benchmark, not just a SQL generation benchmark. A failed run can come from model reasoning, wrong DBT navigation, evaluation target misunderstanding, missing assets, or metadata/file mismatches.

The preflight layer helps separate environment/package failures from actual model failures. The task brief layer points toward DBT-aware context construction for project-level AI agents.

## Next Research Loop

The next step is to run a baseline agent on a small evaluation-ready DBT subset, tag failures by stage, then test whether a DBT-aware preflight/task brief reduces navigation and target-selection errors.
