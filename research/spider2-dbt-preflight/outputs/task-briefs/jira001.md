# DBT Task Brief: jira001

## Instruction

Retrieve information about Jira projects, including project lead details, associated epics, components, and metrics like the average and median time for closing issues, both in days and seconds.

## Preflight Status

- `ready`

## Evaluation Target

- funcs: `duckdb_match`
- gold files: `jira.duckdb`
- condition tables: `jira__project_enhanced`
- condition columns referenced: 14

## DBT Project Shape

- SQL model files: 18
- total SQL lines: 1451
- unique `source()` calls: 1
- unique `ref()` calls: 16

## Suggested Reading Order

- `int_jira__issue_comments`
- `int_jira__issue_field_history`
- `int_jira__issue_multiselect_history`
- `int_jira__issue_assign_resolution`
- `int_jira__issue_epic`
- `int_jira__issue_sprint`
- `int_jira__issue_versions`
- `int_jira__pivot_daily_field_history`
- `int_jira__issue_type_parents`
- `int_jira__field_history_scd`
- `int_jira__issue_users`
- `int_jira__issue_calendar_spine`
- `int_jira__issue_join`
- `jira__daily_issue_field_history`
- `jira__issue_enhanced`
- `int_jira__project_metrics`
- `int_jira__user_metrics`
- `jira__user_enhanced`

## Source Tables

- `jira.issue`

## Internal Model Refs

- `int_jira__field_history_scd`
- `int_jira__issue_assign_resolution`
- `int_jira__issue_calendar_spine`
- `int_jira__issue_comments`
- `int_jira__issue_epic`
- `int_jira__issue_field_history`
- `int_jira__issue_join`
- `int_jira__issue_multiselect_history`
- `int_jira__issue_sprint`
- `int_jira__issue_type_parents`
- `int_jira__issue_users`
- `int_jira__issue_versions`
- `int_jira__pivot_daily_field_history`
- `int_jira__user_metrics`
- `jira__daily_issue_field_history`
- `jira__issue_enhanced`

## Model Table

| model | lines | sources | refs |
| --- | ---: | --- | --- |
| `models/jira__daily_issue_field_history.sql` | 242 |  | `int_jira__field_history_scd`, `int_jira__issue_calendar_spine` |
| `models/intermediate/field_history/int_jira__pivot_daily_field_history.sql` | 178 |  | `int_jira__issue_field_history`, `int_jira__issue_multiselect_history` |
| `models/intermediate/int_jira__issue_join.sql` | 141 |  | `int_jira__issue_assign_resolution`, `int_jira__issue_comments`, `int_jira__issue_sprint`, `int_jira__issue_users`, `int_jira__issue_versions` |
| `models/intermediate/int_jira__project_metrics.sql` | 111 |  | `jira__issue_enhanced` |
| `models/intermediate/field_history/int_jira__issue_calendar_spine.sql` | 99 | `jira.issue` | `int_jira__field_history_scd` |
| `models/intermediate/int_jira__user_metrics.sql` | 85 |  | `jira__issue_enhanced` |
| `models/intermediate/int_jira__issue_versions.sql` | 75 |  | `int_jira__issue_multiselect_history` |
| `models/intermediate/int_jira__issue_sprint.sql` | 71 |  | `int_jira__issue_multiselect_history` |
| `models/jira__user_enhanced.sql` | 66 |  | `int_jira__user_metrics`, `jira__issue_enhanced` |
| `models/intermediate/int_jira__issue_type_parents.sql` | 64 |  | `int_jira__issue_epic` |
| `models/jira__issue_enhanced.sql` | 61 |  | `int_jira__issue_join`, `jira__daily_issue_field_history` |
| `models/intermediate/field_history/int_jira__field_history_scd.sql` | 56 |  | `int_jira__pivot_daily_field_history` |
| `models/intermediate/int_jira__issue_users.sql` | 45 |  | `int_jira__issue_type_parents` |
| `models/intermediate/int_jira__issue_epic.sql` | 35 |  | `int_jira__issue_field_history` |
| `models/intermediate/int_jira__issue_assign_resolution.sql` | 33 |  | `int_jira__issue_field_history` |
| `models/intermediate/int_jira__issue_comments.sql` | 33 |  |  |
| `models/intermediate/field_history/int_jira__issue_field_history.sql` | 28 |  |  |
| `models/intermediate/field_history/int_jira__issue_multiselect_history.sql` | 28 |  |  |

## Agent Use

Before editing or generating DBT code, an agent should:

1. Check that the preflight status is `ready`.
2. Inspect the condition tables first, because evaluation only checks those outputs.
3. Read models in dependency order instead of raw filesystem order.
4. Track whether a failure is caused by missing assets, wrong DBT model selection, source/ref misunderstanding, or final SQL/table mismatch.
