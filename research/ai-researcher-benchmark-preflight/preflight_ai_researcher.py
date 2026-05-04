#!/usr/bin/env python3
"""
Static preflight checks for AI-Researcher benchmark runs.

The script validates environment configuration, benchmark instance schema,
category support files, cache/workspace paths, Docker command availability, and
core Python dependencies before launching research-agent runs. It does not call
LLMs, pull Docker images, start containers, or run Playwright.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


CORE_PACKAGES = {
    "openai": "openai",
    "litellm": "litellm",
    "pydantic": "pydantic",
    "requests": "requests",
    "tqdm": "tqdm",
    "loguru": "loguru",
    "browsergym": "browsergym",
    "playwright": "playwright",
    "pandas": "pandas",
    "networkx": "networkx",
    "gradio": "gradio",
    "arxiv": "arxiv",
}

REQUIRED_ENV = [
    "DOCKER_WORKPLACE_NAME",
    "BASE_IMAGES",
    "COMPLETION_MODEL",
    "CHEEP_MODEL",
    "CONTAINER_NAME",
    "WORKPLACE_NAME",
    "CACHE_PATH",
    "PORT",
    "PLATFORM",
    "CATEGORY",
    "INSTANCE_ID",
    "TASK_LEVEL",
    "MAX_ITER_TIMES",
]

PLACEHOLDER_RE = re.compile(r"^(|your_.+|sk-.+placeholder.+)$", re.IGNORECASE)
TASK_LEVELS = {"task1", "task2"}


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str


@dataclass
class PreflightReport:
    env_file: str
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    checks: list[CheckResult] = field(default_factory=list)
    benchmark_records_scanned: int = 0

    def add(self, name: str, status: str, detail: str) -> None:
        self.checks.append(CheckResult(name=name, status=status, detail=detail))

    @property
    def blockers(self) -> list[CheckResult]:
        return [check for check in self.checks if check.status == "fail"]

    @property
    def warnings(self) -> list[CheckResult]:
        return [check for check in self.checks if check.status == "warn"]

    @property
    def ready(self) -> bool:
        return not self.blockers

    def as_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "ready": self.ready,
            "env_file": self.env_file,
            "benchmark_records_scanned": self.benchmark_records_scanned,
            "summary": {
                "passed": len([c for c in self.checks if c.status == "pass"]),
                "warnings": len(self.warnings),
                "blockers": len(self.blockers),
            },
            "checks": [check.__dict__ for check in self.checks],
        }

    def to_markdown(self) -> str:
        status = "ready" if self.ready else "blocked"
        lines = [
            "# AI-Researcher Preflight Report",
            "",
            f"- Generated at: `{self.generated_at}`",
            f"- Status: `{status}`",
            f"- Env file: `{self.env_file}`",
            f"- Benchmark records scanned: {self.benchmark_records_scanned}",
            "",
            "| Status | Check | Detail |",
            "| --- | --- | --- |",
        ]
        for check in self.checks:
            detail = check.detail.replace("|", "\\|")
            lines.append(f"| `{check.status}` | {check.name} | {detail} |")
        lines.append("")
        return "\n".join(lines)

    def to_text(self) -> str:
        status = "READY" if self.ready else "BLOCKED"
        lines = [
            f"AI-Researcher preflight: {status}",
            f"Env file: {self.env_file}",
            f"Benchmark records scanned: {self.benchmark_records_scanned}",
            "",
        ]
        for check in self.checks:
            lines.append(f"[{check.status.upper()}] {check.name}: {check.detail}")
        return "\n".join(lines)


def resolve_path(path_text: str | None) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text).expanduser()
    return path if path.is_absolute() else path.resolve()


def load_env_file(path: Path, report: PreflightReport) -> dict[str, str]:
    if not path.exists() or not path.is_file():
        report.add("env_file", "fail", f"Environment file not found: {path}")
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")

    report.add("env_file", "pass", f"Loaded {len(values)} key(s) from {path.name}")
    if path.name != ".env":
        report.add("env_file_name", "warn", f"Using non-default env file: {path.name}")
    return values


def get_value(values: dict[str, str], key: str) -> str | None:
    return os.getenv(key, values.get(key))


def is_placeholder(value: str | None) -> bool:
    return PLACEHOLDER_RE.match((value or "").strip()) is not None


def check_required_env(values: dict[str, str], report: PreflightReport) -> None:
    missing = [key for key in REQUIRED_ENV if not get_value(values, key)]
    if missing:
        report.add("required_env", "fail", "Missing required env key(s): " + ", ".join(missing))
    else:
        report.add("required_env", "pass", "All required runtime env keys are present")

    models = [get_value(values, "COMPLETION_MODEL"), get_value(values, "CHEEP_MODEL")]
    needs_openrouter = any((model or "").startswith("openrouter/") for model in models)
    if needs_openrouter and is_placeholder(get_value(values, "OPENROUTER_API_KEY")):
        report.add("openrouter_api_key", "fail", "OPENROUTER_API_KEY is missing or a placeholder for openrouter/* model(s)")
    elif needs_openrouter:
        report.add("openrouter_api_key", "pass", "OPENROUTER_API_KEY is configured for openrouter/* model(s)")
    else:
        report.add("openrouter_api_key", "warn", "No openrouter/* model detected; provider-specific API keys are not statically validated")

    openrouter_base = get_value(values, "OPENROUTER_API_BASE")
    if openrouter_base:
        parsed = urlparse(openrouter_base)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            report.add("openrouter_api_base", "fail", "OPENROUTER_API_BASE is not an absolute http(s) URL")
        else:
            report.add("openrouter_api_base", "pass", "OPENROUTER_API_BASE URL format is valid")


def check_numeric_env(values: dict[str, str], report: PreflightReport) -> None:
    port_text = get_value(values, "PORT")
    try:
        port = int(port_text or "")
    except ValueError:
        report.add("port", "fail", f"PORT must be an integer, got `{port_text}`")
    else:
        if 1 <= port <= 65535:
            report.add("port", "pass", f"PORT is valid: {port}")
        else:
            report.add("port", "fail", f"PORT is out of range: {port}")

    max_iter_text = get_value(values, "MAX_ITER_TIMES")
    try:
        max_iter = int(max_iter_text or "")
    except ValueError:
        report.add("max_iter_times", "fail", f"MAX_ITER_TIMES must be an integer, got `{max_iter_text}`")
    else:
        if max_iter >= 0:
            report.add("max_iter_times", "pass", f"MAX_ITER_TIMES is valid: {max_iter}")
        else:
            report.add("max_iter_times", "fail", f"MAX_ITER_TIMES must be >= 0, got {max_iter}")

    task_level = get_value(values, "TASK_LEVEL")
    if task_level in TASK_LEVELS:
        report.add("task_level", "pass", f"TASK_LEVEL is `{task_level}`")
    else:
        report.add("task_level", "fail", f"TASK_LEVEL must be one of {sorted(TASK_LEVELS)}, got `{task_level}`")


def check_paths(values: dict[str, str], repo_root: Path, report: PreflightReport) -> None:
    for key in ("CACHE_PATH", "WORKPLACE_NAME"):
        text = get_value(values, key)
        if not text:
            continue
        path = Path(text).expanduser()
        if not path.is_absolute():
            path = (repo_root / path).resolve()
        existing = path if path.exists() else path.parent
        while not existing.exists() and existing != existing.parent:
            existing = existing.parent
        if existing.exists() and os.access(existing, os.W_OK):
            report.add(key.lower(), "pass", f"{key} can be created under writable directory: {existing}")
        else:
            report.add(key.lower(), "fail", f"{key} parent is not writable: {path.parent}")


def check_benchmark(values: dict[str, str], repo_root: Path, report: PreflightReport) -> None:
    category = get_value(values, "CATEGORY")
    instance_id = get_value(values, "INSTANCE_ID")
    task_level = get_value(values, "TASK_LEVEL")
    if not category or not instance_id:
        report.add("benchmark_instance", "fail", "CATEGORY or INSTANCE_ID is missing")
        return

    category_dir = repo_root / "benchmark" / "final" / category
    if not category_dir.exists():
        report.add("benchmark_category", "fail", f"Unknown benchmark category: {category}")
        return
    report.add("benchmark_category", "pass", f"Benchmark category exists: {category}")

    instance_path = category_dir / f"{instance_id}.json"
    if not instance_path.exists():
        available = ", ".join(sorted(path.stem for path in category_dir.glob("*.json")))
        report.add("benchmark_instance", "fail", f"Instance not found: {instance_path}. Available: {available}")
        return

    try:
        instance = json.loads(instance_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.add("benchmark_json", "fail", f"Invalid benchmark JSON: {exc}")
        return

    report.benchmark_records_scanned = 1
    required_fields = ["target", "instance_id", "source_papers", "url"]
    missing = [field for field in required_fields if field not in instance]
    if task_level and task_level not in instance:
        missing.append(task_level)
    if missing:
        report.add("benchmark_schema", "fail", "Missing benchmark field(s): " + ", ".join(missing))
    else:
        report.add("benchmark_schema", "pass", f"Benchmark instance schema looks valid: {instance_path}")

    source_papers = instance.get("source_papers")
    if isinstance(source_papers, list) and source_papers:
        malformed = [
            idx
            for idx, paper in enumerate(source_papers, 1)
            if not isinstance(paper, dict) or not paper.get("reference") or not paper.get("usage")
        ]
        if malformed:
            report.add("source_papers", "fail", "Malformed source_papers entries at index: " + ", ".join(map(str, malformed[:10])))
        else:
            report.add("source_papers", "pass", f"{len(source_papers)} source paper(s) include reference and usage")
    else:
        report.add("source_papers", "fail", "source_papers must be a non-empty list")

    metaprompt = repo_root / "benchmark" / "process" / "dataset_candidate" / category / "metaprompt.py"
    if metaprompt.exists():
        report.add("category_metaprompt", "pass", f"Dataset metaprompt exists for category `{category}`")
    else:
        report.add("category_metaprompt", "fail", f"Missing dataset metaprompt for category `{category}`")


def check_dependencies(report: PreflightReport) -> None:
    missing = [
        package
        for module, package in CORE_PACKAGES.items()
        if importlib.util.find_spec(module) is None
    ]
    if missing:
        report.add("python_dependencies", "fail", "Missing package(s): " + ", ".join(missing))
    else:
        report.add("python_dependencies", "pass", "Core Python packages are importable")


def check_docker(report: PreflightReport) -> None:
    if shutil.which("docker") is None:
        report.add("docker_command", "fail", "Docker command is not available on PATH")
    else:
        report.add("docker_command", "pass", "Docker command is available")


def write_outputs(report: PreflightReport, json_path: Path | None, md_path: Path | None) -> None:
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(report.as_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if md_path:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(report.to_markdown(), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preflight AI-Researcher env and benchmark setup.")
    parser.add_argument("--env-file", default=".env", help="Path to .env file")
    parser.add_argument("--repo-root", default=".", help="Path to repository root")
    parser.add_argument("--output-json", help="Optional path for a JSON report")
    parser.add_argument("--output-md", help="Optional path for a Markdown report")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on blocking failures")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    env_file = resolve_path(args.env_file) or Path(".env").resolve()
    repo_root = resolve_path(args.repo_root) or Path(".").resolve()
    report = PreflightReport(env_file=str(env_file))

    values = load_env_file(env_file, report)
    if values:
        check_required_env(values, report)
        check_numeric_env(values, report)
        check_paths(values, repo_root, report)
        check_benchmark(values, repo_root, report)
    check_dependencies(report)
    check_docker(report)

    write_outputs(
        report,
        resolve_path(args.output_json) if args.output_json else None,
        resolve_path(args.output_md) if args.output_md else None,
    )

    print(report.to_text())
    if args.strict and not report.ready:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
