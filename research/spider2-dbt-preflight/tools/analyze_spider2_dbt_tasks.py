#!/usr/bin/env python3
"""Static preflight analyzer for Spider2-DBT tasks.

The goal is to turn a DBT benchmark folder into a task-level table that helps
researchers decide which tasks are actually reproducible and which tasks are
worth using for agent failure analysis.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


SOURCE_RE = re.compile(
    r"source\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
)
REF_RE = re.compile(r"ref\(\s*['\"]([^'\"]+)['\"]\s*\)")
JINJA_RE = re.compile(r"\{\{|\{%")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open() as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
    return rows


def collect_sql_files(task_dir: Path) -> list[Path]:
    models_dir = task_dir / "models"
    if not models_dir.exists():
        return []
    return sorted(
        p
        for p in models_dir.rglob("*.sql")
        if "dbt_packages" not in p.parts and "dbt_modules" not in p.parts
    )


def count_files(root: Path, pattern: str) -> int:
    if not root.exists():
        return 0
    return sum(1 for _ in root.rglob(pattern))


def duckdb_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.glob("*.duckdb"))


def longest_ref_chain(model_names: set[str], refs_by_model: dict[str, set[str]]) -> int:
    cache: dict[str, int] = {}
    visiting: set[str] = set()

    def depth(model: str) -> int:
        if model in cache:
            return cache[model]
        if model in visiting:
            return 1
        visiting.add(model)
        children = [ref for ref in refs_by_model.get(model, set()) if ref in model_names]
        result = 1 + max((depth(child) for child in children), default=0)
        visiting.remove(model)
        cache[model] = result
        return result

    return max((depth(model) for model in model_names), default=0)


def complexity_bucket(score: int) -> str:
    if score >= 80:
        return "high"
    if score >= 35:
        return "medium"
    return "low"


def analyze_task(
    instance_id: str,
    instruction: str,
    task_dir: Path,
    gold_dir: Path,
    eval_row: dict[str, Any] | None,
) -> dict[str, Any]:
    sql_files = collect_sql_files(task_dir)
    model_names = {p.stem for p in sql_files}
    refs_by_model: dict[str, set[str]] = defaultdict(set)
    source_calls: set[str] = set()
    ref_calls: set[str] = set()
    total_sql_lines = 0
    total_jinja_blocks = 0
    max_sql_lines = 0

    for sql_file in sql_files:
        text = sql_file.read_text(errors="ignore")
        lines = text.splitlines()
        total_sql_lines += len(lines)
        max_sql_lines = max(max_sql_lines, len(lines))
        total_jinja_blocks += len(JINJA_RE.findall(text))
        for source_name, table_name in SOURCE_RE.findall(text):
            source_calls.add(f"{source_name}.{table_name}")
        refs = set(REF_RE.findall(text))
        ref_calls.update(refs)
        refs_by_model[sql_file.stem].update(refs)

    eval_func = ""
    eval_tables: list[str] = []
    eval_gold_files: list[str] = []
    eval_condition_cols = 0

    if eval_row:
        eval_metadata = eval_row.get("evaluation", {})
        if not isinstance(eval_metadata, list):
            eval_metadatas = [eval_metadata]
        else:
            eval_metadatas = eval_metadata
        for metadata in eval_metadatas:
            eval_func = metadata.get("func", eval_func)
            params = metadata.get("parameters", {})
            gold = params.get("gold")
            if isinstance(gold, list):
                eval_gold_files.extend(str(item) for item in gold)
            elif gold:
                eval_gold_files.append(str(gold))
            eval_tables.extend(str(item) for item in params.get("condition_tabs", []))
            for cols in params.get("condition_cols", []):
                eval_condition_cols += len(cols)

    start_duckdb = duckdb_files(task_dir)
    gold_task_dir = gold_dir / instance_id
    gold_duckdb = duckdb_files(gold_task_dir)
    missing_expected_gold_files = [
        filename for filename in eval_gold_files if not (gold_task_dir / filename).exists()
    ]

    package_files = count_files(task_dir, "packages.yml")
    seed_files = count_files(task_dir / "seeds", "*.csv")
    macro_files = count_files(task_dir / "macros", "*.sql")
    yaml_files = count_files(task_dir / "models", "*.yml") + count_files(
        task_dir / "models", "*.yaml"
    )
    dag_depth = longest_ref_chain(model_names, refs_by_model)

    complexity_score = (
        len(sql_files) * 4
        + total_sql_lines // 8
        + max_sql_lines // 15
        + len(source_calls) * 2
        + len(ref_calls) * 3
        + dag_depth * 5
        + len(eval_tables) * 3
        + eval_condition_cols // 4
        + total_jinja_blocks
        + package_files * 4
        + seed_files
        + macro_files * 2
    )

    asset_status_parts: list[str] = []
    if not task_dir.exists():
        asset_status_parts.append("missing_task_dir")
    if not start_duckdb:
        asset_status_parts.append("missing_start_duckdb")
    if not gold_task_dir.exists():
        asset_status_parts.append("missing_gold_dir")
    if not gold_duckdb:
        asset_status_parts.append("missing_gold_duckdb")
    if missing_expected_gold_files:
        asset_status_parts.append("missing_expected_gold_file")
    if not asset_status_parts:
        asset_status_parts.append("ready")

    return {
        "instance_id": instance_id,
        "instruction": instruction,
        "asset_status": "|".join(asset_status_parts),
        "is_evaluation_ready": asset_status_parts == ["ready"],
        "sql_files": len(sql_files),
        "total_sql_lines": total_sql_lines,
        "max_sql_lines": max_sql_lines,
        "source_calls": len(source_calls),
        "ref_calls": len(ref_calls),
        "dag_depth": dag_depth,
        "jinja_blocks": total_jinja_blocks,
        "package_files": package_files,
        "seed_files": seed_files,
        "macro_files": macro_files,
        "yaml_files": yaml_files,
        "eval_func": eval_func,
        "eval_tables": len(set(eval_tables)),
        "eval_condition_cols": eval_condition_cols,
        "eval_gold_files": ",".join(eval_gold_files),
        "actual_start_duckdb": ",".join(p.name for p in start_duckdb),
        "actual_gold_duckdb": ",".join(p.name for p in gold_duckdb),
        "missing_expected_gold_files": ",".join(missing_expected_gold_files),
        "complexity_score": complexity_score,
        "complexity_bucket": complexity_bucket(complexity_score),
        "sources_preview": ",".join(sorted(source_calls)[:8]),
        "refs_preview": ",".join(sorted(ref_calls)[:8]),
        "eval_tables_preview": ",".join(sorted(set(eval_tables))[:8]),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    out = []
    out.append("| " + " | ".join(columns) + " |")
    out.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for row in rows:
        values = [str(row.get(col, "")).replace("|", "/") for col in columns]
        out.append("| " + " | ".join(values) + " |")
    return "\n".join(out)


def write_summary(rows: list[dict[str, Any]], output_md: Path, spider2_dbt_dir: Path) -> None:
    total = len(rows)
    ready = [row for row in rows if row["is_evaluation_ready"]]
    blocked = [row for row in rows if not row["is_evaluation_ready"]]
    by_bucket = {
        bucket: sum(1 for row in rows if row["complexity_bucket"] == bucket)
        for bucket in ["low", "medium", "high"]
    }
    top_complex = sorted(
        [row for row in rows if row["is_evaluation_ready"]],
        key=lambda row: row["complexity_score"],
        reverse=True,
    )[:10]
    blocked_focus = sorted(
        blocked,
        key=lambda row: (row["asset_status"], row["instance_id"]),
    )
    starter_candidates = sorted(
        [
            row
            for row in rows
            if row["is_evaluation_ready"] and row["complexity_bucket"] in {"medium", "high"}
        ],
        key=lambda row: row["complexity_score"],
        reverse=True,
    )[:8]

    text = f"""# Spider2-DBT Preflight Analysis

Generated from: `{spider2_dbt_dir}`

## Why this matters

Spider2-DBT is an agent benchmark, not just a SQL string benchmark. Before running an agent, a researcher needs to know whether a task has the required start database, gold database, evaluation metadata, DBT model structure, and enough complexity to be meaningful for failure analysis.

This preflight analyzer converts the benchmark folder into a task-level reproducibility and complexity table.

## Aggregate Results

- Total JSONL tasks: {total}
- Evaluation-ready tasks: {len(ready)}
- Blocked or metadata-inconsistent tasks: {len(blocked)}
- Low-complexity tasks: {by_bucket["low"]}
- Medium-complexity tasks: {by_bucket["medium"]}
- High-complexity tasks: {by_bucket["high"]}

## Blocked / Metadata-Inconsistent Tasks

{markdown_table(blocked_focus, ["instance_id", "asset_status", "eval_gold_files", "actual_gold_duckdb", "missing_expected_gold_files"])}

## Highest-Complexity Evaluation-Ready Tasks

{markdown_table(top_complex, ["instance_id", "complexity_score", "complexity_bucket", "sql_files", "total_sql_lines", "source_calls", "ref_calls", "dag_depth", "eval_tables"])}

## Recommended Mini Research Slice

Use these tasks for a first failure-analysis batch because they are evaluation-ready and structurally non-trivial:

{markdown_table(starter_candidates, ["instance_id", "complexity_score", "sql_files", "total_sql_lines", "source_calls", "ref_calls", "eval_tables", "eval_tables_preview"])}

## Research Contribution Claim

This turns a vague reproduction attempt into a concrete research-engineering contribution:

1. It detects whether the benchmark package is internally consistent before expensive agent runs.
2. It separates benchmark/data blockers from model/agent failures.
3. It ranks DBT tasks by static complexity, which helps choose meaningful tasks for targeted failure analysis.
4. It creates a path toward a more systematic Spider2-DBT study: run agents on evaluation-ready tasks, tag failures by preflight features, then test whether DBT-aware context construction improves success.
"""
    output_md.write_text(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spider2_dbt_dir", type=Path)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    base = args.spider2_dbt_dir.resolve()
    examples_jsonl = base / "examples" / "spider2-dbt.jsonl"
    gold_jsonl = base / "evaluation_suite" / "gold" / "spider2_eval.jsonl"
    gold_dir = base / "evaluation_suite" / "gold"

    examples = read_jsonl(examples_jsonl)
    eval_rows = {row["instance_id"]: row for row in read_jsonl(gold_jsonl)}

    rows = [
        analyze_task(
            row["instance_id"],
            row.get("instruction", ""),
            base / "examples" / row["instance_id"],
            gold_dir,
            eval_rows.get(row["instance_id"]),
        )
        for row in examples
    ]

    fieldnames = list(rows[0].keys()) if rows else []
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    write_summary(rows, args.output_md, base)

    print(f"Wrote {args.output_csv}")
    print(f"Wrote {args.output_md}")
    print(f"tasks={len(rows)} ready={sum(row['is_evaluation_ready'] for row in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
