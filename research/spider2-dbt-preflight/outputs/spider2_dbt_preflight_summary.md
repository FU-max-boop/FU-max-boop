# Spider2-DBT Preflight Analysis

Generated from a local checkout of `xlang-ai/Spider2` after running `spider2-dbt/setup.py`.

## Why this matters

Spider2-DBT is an agent benchmark, not just a SQL string benchmark. Before running an agent, a researcher needs to know whether a task has the required start database, gold database, evaluation metadata, DBT model structure, and enough complexity to be meaningful for failure analysis.

This preflight analyzer converts the benchmark folder into a task-level reproducibility and complexity table.

## Aggregate Results

- Total JSONL tasks: 68
- Evaluation-ready tasks: 61
- Blocked or metadata-inconsistent tasks: 7
- Low-complexity tasks: 5
- Medium-complexity tasks: 8
- High-complexity tasks: 55

## Blocked / Metadata-Inconsistent Tasks

| instance_id | asset_status | eval_gold_files | actual_gold_duckdb | missing_expected_gold_files |
| --- | --- | --- | --- | --- |
| social_media001 | missing_expected_gold_file | social_media_reporting__rollup_report.duckdb | social_media.duckdb | social_media_reporting__rollup_report.duckdb |
| xero_new001 | missing_expected_gold_file | xero.duckdb | xero_new.duckdb | xero.duckdb |
| xero_new002 | missing_expected_gold_file | xero.duckdb | xero_new.duckdb | xero.duckdb |
| airbnb002 | missing_gold_dir/missing_gold_duckdb/missing_expected_gold_file | airbnb.duckdb |  | airbnb.duckdb |
| biketheft001 | missing_gold_dir/missing_gold_duckdb/missing_expected_gold_file | biketheft.duckdb |  | biketheft.duckdb |
| google_ads001 | missing_gold_dir/missing_gold_duckdb/missing_expected_gold_file | google_ads.duckdb |  | google_ads.duckdb |
| gitcoin001 | missing_start_duckdb/missing_gold_dir/missing_gold_duckdb/missing_expected_gold_file | gitcoin.duckdb |  | gitcoin.duckdb |

## Highest-Complexity Evaluation-Ready Tasks

| instance_id | complexity_score | complexity_bucket | sql_files | total_sql_lines | source_calls | ref_calls | dag_depth | eval_tables |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthea001 | 1265 | high | 91 | 2539 | 37 | 41 | 6 | 1 |
| quickbooks003 | 1121 | high | 33 | 3089 | 0 | 53 | 5 | 2 |
| workday001 | 1039 | high | 57 | 2733 | 0 | 45 | 5 | 1 |
| workday002 | 1023 | high | 57 | 2712 | 0 | 43 | 5 | 1 |
| quickbooks001 | 962 | high | 29 | 2620 | 0 | 50 | 3 | 1 |
| hubspot001 | 755 | high | 36 | 1308 | 1 | 16 | 4 | 2 |
| quickbooks002 | 707 | high | 24 | 2086 | 0 | 32 | 1 | 1 |
| jira001 | 662 | high | 18 | 1451 | 1 | 16 | 8 | 1 |
| shopify001 | 593 | high | 27 | 1604 | 0 | 8 | 4 | 2 |
| shopify002 | 586 | high | 27 | 1604 | 0 | 8 | 4 | 1 |

## Recommended Mini Research Slice

Use these tasks for a first failure-analysis batch because they are evaluation-ready and structurally non-trivial:

| instance_id | complexity_score | sql_files | total_sql_lines | source_calls | ref_calls | eval_tables | eval_tables_preview |
| --- | --- | --- | --- | --- | --- | --- | --- |
| synthea001 | 1265 | 91 | 2539 | 37 | 41 | 1 | cost |
| quickbooks003 | 1121 | 33 | 3089 | 0 | 53 | 2 | quickbooks__balance_sheet,quickbooks__general_ledger_by_period |
| workday001 | 1039 | 57 | 2733 | 0 | 45 | 1 | workday__organization_overview |
| workday002 | 1023 | 57 | 2712 | 0 | 43 | 1 | workday__job_overview |
| quickbooks001 | 962 | 29 | 2620 | 0 | 50 | 1 | quickbooks__general_ledger |
| hubspot001 | 755 | 36 | 1308 | 1 | 16 | 2 | hubspot__contacts,hubspot__email_campaigns |
| quickbooks002 | 707 | 24 | 2086 | 0 | 32 | 1 | quickbooks__ap_ar_enhanced |
| jira001 | 662 | 18 | 1451 | 1 | 16 | 1 | jira__project_enhanced |

## Research Contribution Claim

This turns a vague reproduction attempt into a concrete research-engineering contribution:

1. It detects whether the benchmark package is internally consistent before expensive agent runs.
2. It separates benchmark/data blockers from model/agent failures.
3. It ranks DBT tasks by static complexity, which helps choose meaningful tasks for targeted failure analysis.
4. It creates a path toward a more systematic Spider2-DBT study: run agents on evaluation-ready tasks, tag failures by preflight features, then test whether DBT-aware context construction improves success.
