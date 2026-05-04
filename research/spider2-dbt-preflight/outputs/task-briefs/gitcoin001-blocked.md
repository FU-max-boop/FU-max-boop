# DBT Task Brief: gitcoin001

## Instruction

Transform and clean the raw application, project, and application answer data by renaming fields, extracting metadata, and linking answers to their respective questions and projects.

## Preflight Status

- `missing_start_duckdb`
- `missing_gold_dir`
- `missing_gold_duckdb`
- `missing_expected_gold_file:gitcoin.duckdb`

## Evaluation Target

- funcs: `duckdb_match`
- gold files: `gitcoin.duckdb`
- condition tables: `allo_applications`, `allo_projects`
- condition columns referenced: 22

## DBT Project Shape

- SQL model files: 9
- total SQL lines: 185
- unique `source()` calls: 9
- unique `ref()` calls: 0

## Suggested Reading Order

- `allo_deployments`
- `allo_donations`
- `allo_prices`
- `allo_rounds`
- `allo_subscriptions`
- `chain_metadata`
- `gitcoin_passport_scores`
- `giveth_projects`
- `karmahq_details`

## Source Tables

- `main.raw_allo_deployments`
- `main.raw_allo_donations`
- `main.raw_allo_prices`
- `main.raw_allo_rounds`
- `main.raw_allo_subscriptions`
- `main.raw_chain_metadata`
- `main.raw_gitcoin_passport_scores`
- `main.raw_giveth_projects`
- `main.raw_karmahq_attestations`

## Internal Model Refs

- none

## Model Table

| model | lines | sources | refs |
| --- | ---: | --- | --- |
| `models/allo_rounds.sql` | 41 | `main.raw_allo_rounds` |  |
| `models/allo_donations.sql` | 24 | `main.raw_allo_donations` |  |
| `models/gitcoin_passport_scores.sql` | 22 | `main.raw_gitcoin_passport_scores` |  |
| `models/allo_subscriptions.sql` | 21 | `main.raw_allo_subscriptions` |  |
| `models/chain_metadata.sql` | 20 | `main.raw_chain_metadata` |  |
| `models/allo_prices.sql` | 17 | `main.raw_allo_prices` |  |
| `models/karmahq_details.sql` | 14 | `main.raw_karmahq_attestations` |  |
| `models/allo_deployments.sql` | 13 | `main.raw_allo_deployments` |  |
| `models/giveth_projects.sql` | 13 | `main.raw_giveth_projects` |  |

## Agent Use

Before editing or generating DBT code, an agent should:

1. Check that the preflight status is `ready`.
2. Inspect the condition tables first, because evaluation only checks those outputs.
3. Read models in dependency order instead of raw filesystem order.
4. Track whether a failure is caused by missing assets, wrong DBT model selection, source/ref misunderstanding, or final SQL/table mismatch.
