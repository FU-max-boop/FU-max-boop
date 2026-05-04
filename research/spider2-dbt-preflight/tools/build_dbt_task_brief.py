#!/usr/bin/env python3
"""Build an agent-facing brief for one Spider2-DBT task."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


SOURCE_RE = re.compile(
    r"source\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
)
REF_RE = re.compile(r"ref\(\s*['\"]([^'\"]+)['\"]\s*\)")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sql_summary(path: Path) -> dict[str, Any]:
    text = path.read_text(errors="ignore")
    return {
        "model": path.stem,
        "path": path,
        "lines": len(text.splitlines()),
        "sources": sorted(f"{a}.{b}" for a, b in SOURCE_RE.findall(text)),
        "refs": sorted(set(REF_RE.findall(text))),
    }


def topological_reading_order(models: list[dict[str, Any]]) -> list[str]:
    model_names = {m["model"] for m in models}
    dependencies = {
        m["model"]: {ref for ref in m["refs"] if ref in model_names}
        for m in models
    }
    reverse_edges: dict[str, set[str]] = defaultdict(set)
    indegree = {model: len(refs) for model, refs in dependencies.items()}
    for model, refs in dependencies.items():
        for ref in refs:
            reverse_edges[ref].add(model)

    queue = deque(sorted(model for model, degree in indegree.items() if degree == 0))
    order = []
    while queue:
        model = queue.popleft()
        order.append(model)
        for child in sorted(reverse_edges[model]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    remaining = sorted(model for model in model_names if model not in order)
    return order + remaining


def evaluation_summary(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {"funcs": [], "gold_files": [], "tables": [], "condition_cols": 0}
    metadata = row.get("evaluation", {})
    metadatas = metadata if isinstance(metadata, list) else [metadata]
    funcs = []
    gold_files = []
    tables = []
    condition_cols = 0
    for item in metadatas:
        funcs.append(item.get("func", ""))
        params = item.get("parameters", {})
        gold = params.get("gold")
        if isinstance(gold, list):
            gold_files.extend(str(x) for x in gold)
        elif gold:
            gold_files.append(str(gold))
        tables.extend(str(x) for x in params.get("condition_tabs", []))
        for cols in params.get("condition_cols", []):
            condition_cols += len(cols)
    return {
        "funcs": sorted(set(funcs)),
        "gold_files": gold_files,
        "tables": sorted(set(tables)),
        "condition_cols": condition_cols,
    }


def asset_status(task_dir: Path, gold_task_dir: Path, gold_files: list[str]) -> list[str]:
    status = []
    if not any(task_dir.glob("*.duckdb")):
        status.append("missing_start_duckdb")
    if not gold_task_dir.exists():
        status.append("missing_gold_dir")
    if not any(gold_task_dir.glob("*.duckdb")):
        status.append("missing_gold_duckdb")
    missing_files = [
        filename for filename in gold_files if not (gold_task_dir / filename).exists()
    ]
    if missing_files:
        status.append("missing_expected_gold_file:" + ",".join(missing_files))
    return status or ["ready"]


def bullet(items: list[str]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- `{item}`" for item in items)


def model_table(models: list[dict[str, Any]], task_dir: Path) -> str:
    lines = [
        "| model | lines | sources | refs |",
        "| --- | ---: | --- | --- |",
    ]
    for model in sorted(models, key=lambda m: (-m["lines"], m["model"])):
        rel = model["path"].relative_to(task_dir)
        sources = ", ".join(f"`{x}`" for x in model["sources"]) or ""
        refs = ", ".join(f"`{x}`" for x in model["refs"]) or ""
        lines.append(f"| `{rel}` | {model['lines']} | {sources} | {refs} |")
    return "\n".join(lines)


def build_brief(spider2_dbt_dir: Path, instance_id: str) -> str:
    base = spider2_dbt_dir.resolve()
    task_dir = base / "examples" / instance_id
    gold_dir = base / "evaluation_suite" / "gold"
    examples = {
        row["instance_id"]: row
        for row in read_jsonl(base / "examples" / "spider2-dbt.jsonl")
    }
    eval_rows = {
        row["instance_id"]: row
        for row in read_jsonl(gold_dir / "spider2_eval.jsonl")
    }
    if instance_id not in examples:
        raise ValueError(f"Unknown Spider2-DBT instance: {instance_id}")

    models = [
        sql_summary(path)
        for path in sorted((task_dir / "models").rglob("*.sql"))
        if "dbt_packages" not in path.parts and "dbt_modules" not in path.parts
    ]
    eval_info = evaluation_summary(eval_rows.get(instance_id))
    status = asset_status(task_dir, gold_dir / instance_id, eval_info["gold_files"])
    read_order = topological_reading_order(models)
    all_sources = sorted({source for model in models for source in model["sources"]})
    all_refs = sorted({ref for model in models for ref in model["refs"]})

    return f"""# DBT Task Brief: {instance_id}

## Instruction

{examples[instance_id].get("instruction", "")}

## Preflight Status

{bullet(status)}

## Evaluation Target

- funcs: {", ".join(f"`{x}`" for x in eval_info["funcs"]) or "none"}
- gold files: {", ".join(f"`{x}`" for x in eval_info["gold_files"]) or "none"}
- condition tables: {", ".join(f"`{x}`" for x in eval_info["tables"]) or "none"}
- condition columns referenced: {eval_info["condition_cols"]}

## DBT Project Shape

- SQL model files: {len(models)}
- total SQL lines: {sum(model["lines"] for model in models)}
- unique `source()` calls: {len(all_sources)}
- unique `ref()` calls: {len(all_refs)}

## Suggested Reading Order

{bullet(read_order)}

## Source Tables

{bullet(all_sources)}

## Internal Model Refs

{bullet(all_refs)}

## Model Table

{model_table(models, task_dir)}

## Agent Use

Before editing or generating DBT code, an agent should:

1. Check that the preflight status is `ready`.
2. Inspect the condition tables first, because evaluation only checks those outputs.
3. Read models in dependency order instead of raw filesystem order.
4. Track whether a failure is caused by missing assets, wrong DBT model selection, source/ref misunderstanding, or final SQL/table mismatch.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spider2_dbt_dir", type=Path)
    parser.add_argument("instance_id")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    brief = build_brief(args.spider2_dbt_dir, args.instance_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(brief)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
