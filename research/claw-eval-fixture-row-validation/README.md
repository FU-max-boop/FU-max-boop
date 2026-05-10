# claw-eval Fixture Row Validation

Upstream PR: https://github.com/claw-eval/claw-eval/pull/44

This contribution makes `scripts/validate_tasks.py` validate required fixture
fields on every row of each JSON fixture array, rather than only checking the
first row.

## Finding

The task validator is meant to catch task and fixture integrity problems before
benchmark runs. The previous required-field check inspected only `data[0]`, so a
later malformed fixture record could silently pass validation if the first
record was complete.

That can hide fixture drift in multi-record datasets and make task failures
harder to reproduce.

## Fix

The PR:

- checks each fixture item instead of only the first item
- reports the row index when a required field is missing
- reports a clear error if a fixture array contains a non-object item
- adds an offline regression test for a second Gmail fixture row missing `body`

## Validation

From the upstream repo root:

```bash
python3 -m py_compile scripts/validate_tasks.py tests/test_validate_tasks.py
python3 -m unittest tests/test_validate_tasks.py
python3 scripts/validate_tasks.py --pattern 'T024*'
git diff --check
```

Scope: this does not change task data, required-field definitions, service
logic, or scoring behavior.
