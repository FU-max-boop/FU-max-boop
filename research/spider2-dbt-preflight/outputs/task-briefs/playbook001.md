# DBT Task Brief: playbook001

## Instruction

Complete the project of this database to show the metrics of each traffic source, I believe every touchpoint in the conversion path is equally important, please choose the most suitable attribution method.

## Preflight Status

- `ready`

## Evaluation Target

- funcs: `duckdb_match`
- gold files: `playbook.duckdb`
- condition tables: `attribution_touches`
- condition columns referenced: 4

## DBT Project Shape

- SQL model files: 1
- total SQL lines: 54
- unique `source()` calls: 2
- unique `ref()` calls: 0

## Suggested Reading Order

- `attribution_touches`

## Source Tables

- `playbook.customer_conversions`
- `playbook.sessions`

## Internal Model Refs

- none

## Model Table

| model | lines | sources | refs |
| --- | ---: | --- | --- |
| `models/attribution_touches.sql` | 54 | `playbook.customer_conversions`, `playbook.sessions` |  |

## Agent Use

Before editing or generating DBT code, an agent should:

1. Check that the preflight status is `ready`.
2. Inspect the condition tables first, because evaluation only checks those outputs.
3. Read models in dependency order instead of raw filesystem order.
4. Track whether a failure is caused by missing assets, wrong DBT model selection, source/ref misunderstanding, or final SQL/table mismatch.
