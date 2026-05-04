#!/usr/bin/env python3
"""Check whether Spider2-DBT JSONL ids match downloaded DuckDB assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_jsonl_ids(path: Path) -> list[str]:
    ids: list[str] = []
    with path.open() as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            instance_id = row.get("instance_id")
            if not instance_id:
                raise ValueError(f"{path}:{line_no} missing instance_id")
            ids.append(instance_id)
    return ids


def duckdb_dirs(root: Path) -> set[str]:
    if not root.exists():
        return set()
    return {
        child.name
        for child in root.iterdir()
        if child.is_dir() and any(child.glob("*.duckdb"))
    }


def gold_expected_files(gold_jsonl: Path) -> dict[str, str]:
    expected: dict[str, str] = {}
    with gold_jsonl.open() as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            instance_id = row.get("instance_id")
            gold_name = (
                row.get("evaluation", {})
                .get("parameters", {})
                .get("gold")
            )
            if not instance_id:
                raise ValueError(f"{gold_jsonl}:{line_no} missing instance_id")
            if gold_name:
                expected[instance_id] = gold_name
    return expected


def print_list(title: str, items: list[str]) -> None:
    print(f"{title}: {len(items)}")
    for item in items:
        print(f"  - {item}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "spider2_dbt_dir",
        type=Path,
        help="Path to the spider2-dbt directory after running setup.py.",
    )
    args = parser.parse_args()

    base = args.spider2_dbt_dir.resolve()
    examples_jsonl = base / "examples" / "spider2-dbt.jsonl"
    gold_jsonl = base / "evaluation_suite" / "gold" / "spider2_eval.jsonl"
    examples_dir = base / "examples"
    gold_dir = base / "evaluation_suite" / "gold"

    example_ids = set(load_jsonl_ids(examples_jsonl))
    eval_ids = set(load_jsonl_ids(gold_jsonl))
    start_duckdb_dirs = duckdb_dirs(examples_dir)
    gold_duckdb_dirs = duckdb_dirs(gold_dir)
    expected_gold = gold_expected_files(gold_jsonl)

    missing_start_dirs = sorted(example_ids - start_duckdb_dirs)
    extra_start_dirs = sorted(start_duckdb_dirs - example_ids)
    missing_gold_dirs = sorted(eval_ids - gold_duckdb_dirs)
    extra_gold_dirs = sorted(gold_duckdb_dirs - eval_ids)
    jsonl_id_mismatch = sorted(example_ids ^ eval_ids)
    missing_expected_gold_files = sorted(
        instance_id
        for instance_id, filename in expected_gold.items()
        if not (gold_dir / instance_id / filename).exists()
    )

    print(f"Spider2-DBT dir: {base}")
    print(f"example JSONL ids: {len(example_ids)}")
    print(f"eval JSONL ids: {len(eval_ids)}")
    print(f"start DuckDB dirs: {len(start_duckdb_dirs)}")
    print(f"gold DuckDB dirs: {len(gold_duckdb_dirs)}")

    print_list("JSONL id mismatch", jsonl_id_mismatch)
    print_list("Missing start DuckDB dirs", missing_start_dirs)
    print_list("Extra start DuckDB dirs", extra_start_dirs)
    print_list("Missing gold DuckDB dirs", missing_gold_dirs)
    print_list("Extra gold DuckDB dirs", extra_gold_dirs)
    print_list("Missing expected gold files", missing_expected_gold_files)

    has_issue = any(
        [
            jsonl_id_mismatch,
            missing_start_dirs,
            extra_start_dirs,
            missing_gold_dirs,
            extra_gold_dirs,
            missing_expected_gold_files,
        ]
    )
    return 1 if has_issue else 0


if __name__ == "__main__":
    raise SystemExit(main())
