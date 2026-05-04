#!/usr/bin/env python3
"""Static preflight analysis for Claw-Eval task definitions.

This utility intentionally does not run agents, graders, mock services, model
APIs, or sandbox containers. It reads task.yaml metadata and local file
references so contributors can scope reproduction blockers before expensive
multi-trial evaluation.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


SERVICE_FIXTURE_ENV_HINTS = {
    "gmail": "GMAIL_FIXTURES",
    "calendar": "CALENDAR_FIXTURES",
    "contacts": "CONTACTS_FIXTURES",
    "finance": "FINANCE_FIXTURES",
    "helpdesk": "HELPDESK_FIXTURES",
    "kb": "KB_FIXTURES",
    "crm": "CRM_FIXTURES",
    "inventory": "INVENTORY_FIXTURES",
    "rss": "RSS_FIXTURES",
    "scheduler": "SCHEDULER_FIXTURES",
    "config": "CONFIG_FIXTURES",
    "notes": "NOTES_FIXTURES",
    "todo": "TODO_FIXTURES",
    "web": "WEB_SEARCH_FIXTURES",
    "web_real": None,
}


URL_RE = re.compile(r"https?://[^\s)>\"]+")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def load_yaml(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = yaml.safe_load(path.read_text())
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "YAML root is not a mapping"
    return data, None


def split_for_task(task_id: str, tags: list[str], user_agent_enabled: bool) -> str:
    tag_set = set(tags)
    if user_agent_enabled or "user_agent" in tag_set:
        return "multi_turn"
    if "multimodal" in tag_set or task_id.startswith("M"):
        return "multimodal"
    return "general"


def safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def local_ref_exists(repo_root: Path, task_dir: Path, rel: str) -> bool:
    """Return true if a task-local or repo-root-relative reference exists."""
    return (task_dir / rel).exists() or (repo_root / rel).exists()


def analyze_task(task_dir: Path, repo_root: Path) -> dict[str, Any]:
    yaml_path = task_dir / "task.yaml"
    row: dict[str, Any] = {
        "task_dir": safe_rel(task_dir, repo_root),
        "yaml_ok": False,
        "blocking_issues": [],
        "warnings": [],
    }

    if not yaml_path.exists():
        row["task_id"] = task_dir.name
        row["blocking_issues"].append("missing task.yaml")
        return row

    data, error = load_yaml(yaml_path)
    if error:
        row["task_id"] = task_dir.name
        row["blocking_issues"].append(f"task.yaml parse error: {error}")
        return row

    assert data is not None
    task_id = str(data.get("task_id", ""))
    tags = [str(x) for x in as_list(data.get("tags"))]
    prompt = data.get("prompt") if isinstance(data.get("prompt"), dict) else {}
    env = data.get("environment") if isinstance(data.get("environment"), dict) else {}
    user_agent = data.get("user_agent") if isinstance(data.get("user_agent"), dict) else {}
    services = as_list(data.get("services"))
    tools = as_list(data.get("tools"))
    endpoints = as_list(data.get("tool_endpoints"))
    scoring = as_list(data.get("scoring_components"))
    safety = as_list(data.get("safety_checks"))

    row.update(
        {
            "yaml_ok": True,
            "task_id": task_id,
            "task_name": str(data.get("task_name", "")),
            "category": str(data.get("category", "")),
            "difficulty": str(data.get("difficulty", "")),
            "language": str(prompt.get("language", "")),
            "tags": ",".join(tags),
            "split": split_for_task(task_id, tags, bool(user_agent.get("enabled", False))),
            "tool_count": len(tools),
            "endpoint_count": len(endpoints),
            "service_count": len(services),
            "scoring_count": len(scoring),
            "safety_count": len(safety),
            "expected_action_count": len(as_list(data.get("expected_actions"))),
            "primary_dimensions": ",".join(str(x) for x in as_list(data.get("primary_dimensions"))),
            "max_turns": env.get("max_turns", ""),
            "timeout_seconds": env.get("timeout_seconds", ""),
            "fixture_ref_count": 0,
            "missing_fixture_count": 0,
            "sandbox_file_count": len(as_list(data.get("sandbox_files"))),
            "missing_sandbox_file_count": 0,
            "attachment_count": len(as_list(prompt.get("attachments"))),
            "missing_attachment_count": 0,
            "env_snapshot_file_count": len(as_list(data.get("env_snapshot_files"))),
            "env_snapshot_command_count": len(as_list(data.get("env_snapshot_commands"))),
            "url_count": len(URL_RE.findall(str(prompt.get("text", "")))),
            "has_grader": (task_dir / "grader.py").exists(),
            "has_reference_solution": bool(str(data.get("reference_solution", "")).strip()),
            "has_judge_rubric": bool(str(data.get("judge_rubric", "")).strip()),
            "uses_user_agent": bool(user_agent.get("enabled", False)),
            "service_names": ",".join(str(s.get("name", "")) for s in services if isinstance(s, dict)),
        }
    )

    if task_id and task_dir.name != task_id:
        row["warnings"].append(f"task_id differs from directory: {task_id}")
    if not task_id:
        row["blocking_issues"].append("missing task_id")

    if not row["has_grader"]:
        row["blocking_issues"].append("missing grader.py")

    tool_names = {
        str(tool.get("name", ""))
        for tool in tools
        if isinstance(tool, dict) and tool.get("name")
    }
    endpoint_names = {
        str(endpoint.get("tool_name", ""))
        for endpoint in endpoints
        if isinstance(endpoint, dict) and endpoint.get("tool_name")
    }
    missing_endpoints = sorted(
        name for name in tool_names
        if name not in endpoint_names and name not in {"Bash"}
    )
    orphan_endpoints = sorted(name for name in endpoint_names if name not in tool_names)
    if missing_endpoints:
        row["warnings"].append(f"tools without endpoints: {','.join(missing_endpoints)}")
    if orphan_endpoints:
        row["warnings"].append(f"endpoints without tools: {','.join(orphan_endpoints)}")

    weights = []
    for component in scoring:
        if isinstance(component, dict) and "weight" in component:
            try:
                weights.append(float(component["weight"]))
            except (TypeError, ValueError):
                row["warnings"].append(f"non-numeric scoring weight: {component.get('name', '')}")
    if weights and abs(sum(weights) - 1.0) > 0.01:
        row["warnings"].append(f"scoring weights sum to {sum(weights):.3f}")

    if "send" in " ".join(tool_names).lower():
        has_send_safety = any(
            isinstance(check, dict)
            and str(check.get("type", "")) == "tool_not_called"
            and "send" in str(check.get("tool_name", "")).lower()
            for check in safety
        )
        if not has_send_safety:
            row["warnings"].append("task exposes send-like tool without explicit tool_not_called safety check")

    missing_fixtures: list[str] = []
    for service in services:
        if not isinstance(service, dict):
            continue
        service_name = str(service.get("name", ""))
        service_env = service.get("env") if isinstance(service.get("env"), dict) else {}
        hinted_env = SERVICE_FIXTURE_ENV_HINTS.get(service_name)
        if hinted_env and hinted_env not in service_env:
            row["warnings"].append(f"service {service_name} missing expected env var {hinted_env}")
        for key, value in service_env.items():
            if "FIXTURE" not in str(key).upper():
                continue
            row["fixture_ref_count"] += 1
            fixture_path = repo_root / str(value)
            if not fixture_path.exists():
                missing_fixtures.append(str(value))
    row["missing_fixture_count"] = len(missing_fixtures)
    if missing_fixtures:
        row["blocking_issues"].append(f"missing service fixtures: {';'.join(missing_fixtures[:5])}")

    missing_sandbox_files: list[str] = []
    for rel in as_list(data.get("sandbox_files")) + as_list(data.get("sandbox_grader_files")):
        if not local_ref_exists(repo_root, task_dir, str(rel)):
            missing_sandbox_files.append(str(rel))
    row["missing_sandbox_file_count"] = len(missing_sandbox_files)
    if missing_sandbox_files:
        row["blocking_issues"].append(f"missing sandbox files: {';'.join(missing_sandbox_files[:5])}")

    missing_attachments: list[str] = []
    for rel in as_list(prompt.get("attachments")):
        if not local_ref_exists(repo_root, task_dir, str(rel)):
            missing_attachments.append(str(rel))
    row["missing_attachment_count"] = len(missing_attachments)
    if missing_attachments:
        row["blocking_issues"].append(f"missing prompt attachments: {';'.join(missing_attachments[:5])}")

    if row["url_count"] > 0:
        row["warnings"].append("prompt requires external URLs; full reproduction depends on network availability")
    if any("video" in str(x).lower() for x in [task_id, data.get("task_name", ""), prompt.get("text", "")]):
        row["warnings"].append("video/media task may require Hugging Face fixtures not included in GitHub repo")

    row["is_preflight_ready"] = len(row["blocking_issues"]) == 0
    row["blocking_issues"] = " | ".join(row["blocking_issues"])
    row["warnings"] = " | ".join(row["warnings"])
    return row


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fields = [
        "task_id", "task_dir", "split", "category", "difficulty", "language", "tags",
        "is_preflight_ready", "blocking_issues", "warnings",
        "tool_count", "endpoint_count", "service_count", "service_names",
        "fixture_ref_count", "missing_fixture_count", "sandbox_file_count",
        "missing_sandbox_file_count", "attachment_count", "missing_attachment_count",
        "env_snapshot_file_count", "env_snapshot_command_count",
        "scoring_count", "safety_count", "expected_action_count", "primary_dimensions",
        "has_grader", "has_reference_solution", "has_judge_rubric", "uses_user_agent",
        "url_count", "max_turns", "timeout_seconds",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_markdown(rows: list[dict[str, Any]], path: Path) -> None:
    total = len(rows)
    ready = sum(1 for row in rows if row.get("is_preflight_ready"))
    by_split = Counter(str(row.get("split", "")) for row in rows)
    by_category = Counter(str(row.get("category", "")) for row in rows)
    by_language = Counter(str(row.get("language", "")) for row in rows)
    by_difficulty = Counter(str(row.get("difficulty", "")) for row in rows)
    blocking = [row for row in rows if not row.get("is_preflight_ready")]
    warnings = [row for row in rows if row.get("warnings")]

    lines = [
        "# Claw-Eval Static Preflight Summary",
        "",
        "This report is a local static preflight pass over the public Claw-Eval GitHub repository. It does not run agents, graders, mock services, or model APIs. It checks task metadata and local file references so reproduction work can be scoped before expensive benchmark execution.",
        "",
        "## Headline",
        "",
        f"- Tasks scanned: {total}",
        f"- Preflight-ready by local metadata/file-reference checks: {ready}/{total}",
        f"- Blocked by local static issues: {total - ready}/{total}",
        f"- Tasks with caution warnings: {len(warnings)}/{total}",
        "",
        "## Split Counts",
        "",
        "| Split | Count |",
        "|---|---:|",
    ]
    for split, count in sorted(by_split.items()):
        lines.append(f"| {split or '(blank)'} | {count} |")

    lines.extend(["", "## Language Counts", "", "| Language | Count |", "|---|---:|"])
    for lang, count in sorted(by_language.items()):
        lines.append(f"| {lang or '(blank)'} | {count} |")

    lines.extend(["", "## Difficulty Counts", "", "| Difficulty | Count |", "|---|---:|"])
    for difficulty, count in sorted(by_difficulty.items()):
        lines.append(f"| {difficulty or '(blank)'} | {count} |")

    lines.extend(["", "## Top Categories", "", "| Category | Count |", "|---|---:|"])
    for category, count in by_category.most_common(20):
        lines.append(f"| {category or '(blank)'} | {count} |")

    lines.extend(["", "## Blocking Issues", ""])
    if not blocking:
        lines.append("No local static blocking issues found.")
    else:
        lines.extend(["| Task | Split | Issue |", "|---|---|---|"])
        for row in blocking[:80]:
            lines.append(f"| {row.get('task_id')} | {row.get('split')} | {row.get('blocking_issues')} |")
        if len(blocking) > 80:
            lines.append(f"| ... | ... | {len(blocking) - 80} more rows in CSV |")

    lines.extend(["", "## Common Warning Types", ""])
    warning_counter: Counter[str] = Counter()
    for row in warnings:
        for warning in str(row.get("warnings", "")).split(" | "):
            if warning:
                warning_counter[warning] += 1
    if warning_counter:
        lines.extend(["| Warning | Count |", "|---|---:|"])
        for warning, count in warning_counter.most_common(30):
            lines.append(f"| {warning} | {count} |")
    else:
        lines.append("No warnings found.")

    lines.extend([
        "",
        "## Why This Matters",
        "",
        "Claw-Eval's main research value is not only task breadth, but trustworthy agent evaluation through completion, safety, robustness, and trajectory-aware grading. A lightweight preflight layer helps separate benchmark/setup readiness issues from model-side failures before running expensive three-trial evaluations.",
        "",
        "## Suggested Next Contribution",
        "",
        "1. Turn this static preflight into a maintained `scripts/preflight_tasks.py` or docs note for contributors.",
        "2. Add a task anatomy table for category/split/language/difficulty/rubric coverage.",
        "3. Extend the pass to verify Hugging Face fixture coverage once the dataset archive is available locally.",
        "4. Use the warning taxonomy to choose a small subset for actual end-to-end reproduction after confirming dependency/API budget.",
        "",
    ])

    path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out-dir", type=Path, default=Path("preflight_out"))
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [
        analyze_task(task_dir, repo_root)
        for task_dir in sorted((repo_root / "tasks").iterdir())
        if task_dir.is_dir()
    ]

    write_csv(rows, out_dir / "claw_eval_task_preflight.csv")
    write_markdown(rows, out_dir / "claw_eval_static_preflight_summary.md")
    (out_dir / "claw_eval_task_preflight.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False)
    )

    print(f"Scanned {len(rows)} tasks")
    print(f"Preflight-ready: {sum(1 for row in rows if row.get('is_preflight_ready'))}/{len(rows)}")
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
