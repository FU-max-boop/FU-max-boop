#!/usr/bin/env python3
"""
Static preflight checks for DeepResearch-ReportEval.

This script validates dependencies, environment variables, JSONL input schema,
and output paths before running report scoring or fact-checking. It does not
call LLMs, Firecrawl, or Jina.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REQUIRED_PACKAGES = {
    "openai": "openai",
    "json_repair": "json-repair",
    "dotenv": "python-dotenv",
    "tqdm": "tqdm",
    "requests": "requests",
    "dashscope": "dashscope",
    "firecrawl": "firecrawl-python",
}

PLACEHOLDERS = {"", "your-openai-api-key", "your api key", "your api base", "your-firecrawl-key", "your-jina-api-key", "your firecrawl api key", "your jina api key"}


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str


@dataclass
class PreflightReport:
    task: str
    input_path: str | None
    output_path: str | None
    provider: str
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    checks: list[CheckResult] = field(default_factory=list)
    scanned_records: int = 0

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
            "task": self.task,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "provider": self.provider,
            "scanned_records": self.scanned_records,
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
            "# DeepResearch-ReportEval Preflight Report",
            "",
            f"- Generated at: `{self.generated_at}`",
            f"- Status: `{status}`",
            f"- Task: `{self.task}`",
            f"- Provider: `{self.provider}`",
            f"- Input path: `{self.input_path or ''}`",
            f"- Output path: `{self.output_path or ''}`",
            f"- Records scanned: {self.scanned_records}",
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
            f"DeepResearch-ReportEval preflight: {status}",
            f"Task: {self.task}",
            f"Provider: {self.provider}",
            f"Records scanned: {self.scanned_records}",
            "",
        ]
        for check in self.checks:
            lines.append(f"[{check.status.upper()}] {check.name}: {check.detail}")
        return "\n".join(lines)


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def env_get(values: dict[str, str], key: str) -> str | None:
    return os.getenv(key, values.get(key))


def is_placeholder(value: str | None) -> bool:
    return (value or "").strip().lower() in PLACEHOLDERS


def resolve_path(path_text: str | None) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text).expanduser()
    return path if path.is_absolute() else path.resolve()


def check_dependencies(report: PreflightReport) -> None:
    missing = [
        package
        for module, package in REQUIRED_PACKAGES.items()
        if importlib.util.find_spec(module) is None
    ]
    if missing:
        report.add(
            "dependencies",
            "fail",
            "Missing package(s): " + ", ".join(missing),
        )
    else:
        report.add("dependencies", "pass", "All documented Python packages are importable")


def check_environment(values: dict[str, str], provider: str, report: PreflightReport) -> None:
    if is_placeholder(env_get(values, "OPENAI_API_KEY")):
        report.add("openai_api_key", "fail", "OPENAI_API_KEY is missing or a placeholder")
    else:
        report.add("openai_api_key", "pass", "OPENAI_API_KEY is configured")

    base = env_get(values, "OPENAI_API_BASE")
    if base and not is_placeholder(base):
        parsed = urlparse(base)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            report.add("openai_api_base", "fail", "OPENAI_API_BASE is not an absolute http(s) URL")
        else:
            report.add("openai_api_base", "pass", "OPENAI_API_BASE URL format is valid")
    else:
        report.add("openai_api_base", "warn", "OPENAI_API_BASE is unset or a placeholder; default OpenAI endpoint will be used")

    firecrawl_key = env_get(values, "FIRECRAWL_KEY")
    legacy_firecrawl_key = env_get(values, "FIRECRAWL_API_KEY")
    if provider == "firecrawl":
        if is_placeholder(firecrawl_key):
            if legacy_firecrawl_key and not is_placeholder(legacy_firecrawl_key):
                report.add(
                    "firecrawl_key",
                    "fail",
                    "FIRECRAWL_API_KEY is set, but the code reads FIRECRAWL_KEY",
                )
            else:
                report.add("firecrawl_key", "fail", "FIRECRAWL_KEY is missing or a placeholder")
        else:
            report.add("firecrawl_key", "pass", "FIRECRAWL_KEY is configured")
    elif legacy_firecrawl_key and not firecrawl_key:
        report.add(
            "firecrawl_env_alias",
            "warn",
            "Found FIRECRAWL_API_KEY, but Atools.py reads FIRECRAWL_KEY",
        )

    if provider == "jina":
        if is_placeholder(env_get(values, "JINA_API_KEY")):
            report.add("jina_api_key", "fail", "JINA_API_KEY is missing or a placeholder")
        else:
            report.add("jina_api_key", "pass", "JINA_API_KEY is configured")


def check_input_schema(task: str, input_path: Path | None, report: PreflightReport) -> None:
    if input_path is None:
        report.add("input_path", "warn", "No input file provided")
        return

    if not input_path.exists() or not input_path.is_file():
        report.add("input_path", "fail", f"Input file does not exist: {input_path}")
        return

    if input_path.suffix.lower() != ".jsonl":
        report.add("input_path", "fail", "Input must be a .jsonl file")
        return

    malformed: list[str] = []
    schema_errors: list[str] = []
    count = 0
    with input_path.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, 1):
            line = raw_line.strip()
            if not line:
                continue
            count += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                malformed.append(f"line {line_no}: {exc}")
                continue
            validate_record(task, obj, line_no, schema_errors)

    report.scanned_records = count
    if malformed:
        report.add("jsonl_parse", "fail", "; ".join(malformed[:8]))
    else:
        report.add("jsonl_parse", "pass", f"Parsed {count} JSONL record(s)")

    if schema_errors:
        report.add("input_schema", "fail", "; ".join(schema_errors[:10]))
    else:
        report.add("input_schema", "pass", f"`{task}` input schema looks valid")


def validate_record(task: str, obj: Any, line_no: int, errors: list[str]) -> None:
    if task == "score":
        if not isinstance(obj, dict):
            errors.append(f"line {line_no}: record is not an object")
            return
        if not isinstance(obj.get("topic"), str) or not obj.get("topic", "").strip():
            errors.append(f"line {line_no}: missing string `topic`")
        if not isinstance(obj.get("report"), str) or not obj.get("report", "").strip():
            errors.append(f"line {line_no}: missing string `report`")
        elif "## " not in obj["report"]:
            errors.append(f"line {line_no}: report has no `## ` headings for redundancy sampling")
        return

    if task == "fact":
        if not isinstance(obj, dict) or len(obj) != 1:
            errors.append(f"line {line_no}: fact record must contain exactly one URL key")
            return
        (url, payload), = obj.items()
        parsed = urlparse(str(url))
        if parsed.scheme not in {"http", "https"}:
            errors.append(f"line {line_no}: URL key is not http(s)")
        if not isinstance(payload, dict):
            errors.append(f"line {line_no}: URL payload is not an object")
            return
        contexts = payload.get("contexts")
        if not isinstance(contexts, list) or not contexts:
            errors.append(f"line {line_no}: missing non-empty `contexts` list")
        elif not all(isinstance(context, str) and context.strip() for context in contexts):
            errors.append(f"line {line_no}: every context must be a non-empty string")


def check_output_path(output_path: Path | None, report: PreflightReport) -> None:
    if output_path is None:
        report.add("output_path", "warn", "No output path provided")
        return

    parent = output_path if output_path.exists() and output_path.is_dir() else output_path.parent
    existing = parent
    while not existing.exists() and existing != existing.parent:
        existing = existing.parent

    if existing.exists() and os.access(existing, os.W_OK):
        if parent.exists():
            report.add("output_path", "pass", f"Output parent is writable: {parent}")
        else:
            report.add("output_path", "pass", f"Output parent can be created under writable directory: {existing}")
    else:
        report.add("output_path", "fail", f"Output parent is missing or not writable: {parent}")


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
    parser = argparse.ArgumentParser(description="Preflight DeepResearch-ReportEval inputs and environment.")
    parser.add_argument("--task", choices=["score", "fact"], default="score")
    parser.add_argument("--inputpath", help="Input JSONL file to validate.")
    parser.add_argument("--outputpath", help="Output file or directory to validate.")
    parser.add_argument("--provider", choices=["firecrawl", "jina"], default="jina")
    parser.add_argument("--env-file", default=".env", help="Optional env file to inspect.")
    parser.add_argument("--output-json", help="Optional path for a JSON report.")
    parser.add_argument("--output-md", help="Optional path for a Markdown report.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on blocking failures.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    env_values = load_env_file(resolve_path(args.env_file) or Path(".env"))

    input_path = resolve_path(args.inputpath)
    output_path = resolve_path(args.outputpath)
    report = PreflightReport(
        task=args.task,
        input_path=str(input_path) if input_path else None,
        output_path=str(output_path) if output_path else None,
        provider=args.provider,
    )

    check_dependencies(report)
    check_environment(env_values, args.provider, report)
    check_input_schema(args.task, input_path, report)
    check_output_path(output_path, report)

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
