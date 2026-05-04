#!/usr/bin/env python3
"""
Audit pre-parsed RAG-Anything content_list files before insertion.

The audit is intentionally offline: it does not call parsers, LightRAG, LLMs,
embedding models, or VLMs. It catches schema, image-path, caption, page index,
and context-availability issues that otherwise tend to surface late during
direct content-list insertion.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff",
    ".tif",
}
MULTIMODAL_TYPES = {"image", "table", "equation"}
PLACEHOLDER_MARKERS = {
    "/absolute/path",
    "your/",
    "your-",
    "path/to/",
    "example.",
    "placeholder",
}


@dataclass
class Finding:
    severity: str
    item_index: int | None
    content_type: str
    field: str
    message: str
    recommendation: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "item_index": self.item_index,
            "content_type": self.content_type,
            "field": self.field,
            "message": self.message,
            "recommendation": self.recommendation,
        }


@dataclass
class ItemAudit:
    index: int
    content_type: str
    page_idx: int | None
    text_chars: int = 0
    caption_count: int = 0
    context_chars: int = 0
    context_items: int = 0
    image_path: str = ""
    table_rows: int = 0
    table_columns: int = 0
    findings: list[Finding] = field(default_factory=list)

    @property
    def status(self) -> str:
        severities = {finding.severity for finding in self.findings}
        if "fail" in severities:
            return "fail"
        if "warn" in severities:
            return "warn"
        return "pass"

    def as_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "content_type": self.content_type,
            "page_idx": self.page_idx,
            "status": self.status,
            "text_chars": self.text_chars,
            "caption_count": self.caption_count,
            "context_chars": self.context_chars,
            "context_items": self.context_items,
            "image_path": self.image_path,
            "table_rows": self.table_rows,
            "table_columns": self.table_columns,
            "findings": [finding.as_dict() for finding in self.findings],
        }


@dataclass
class ContentListAudit:
    input_path: str
    generated_at: str
    context_mode: str
    context_window: int
    context_types: list[str]
    items: list[ItemAudit]
    findings: list[Finding]

    @property
    def blockers(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "fail"]

    @property
    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "warn"]

    @property
    def status(self) -> str:
        if self.blockers:
            return "blocked"
        if self.warnings:
            return "ready_with_warnings"
        return "ready"

    def type_distribution(self) -> dict[str, int]:
        distribution: dict[str, int] = {}
        for item in self.items:
            distribution[item.content_type] = distribution.get(item.content_type, 0) + 1
        return distribution

    def as_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "input_path": self.input_path,
            "status": self.status,
            "context": {
                "mode": self.context_mode,
                "window": self.context_window,
                "types": self.context_types,
            },
            "summary": {
                "total_items": len(self.items),
                "blockers": len(self.blockers),
                "warnings": len(self.warnings),
                "type_distribution": self.type_distribution(),
                "multimodal_items": len(
                    [item for item in self.items if item.content_type != "text"]
                ),
                "multimodal_without_context": len(
                    [
                        item
                        for item in self.items
                        if item.content_type != "text" and item.context_items == 0
                    ]
                ),
                "text_chars": sum(item.text_chars for item in self.items),
            },
            "findings": [finding.as_dict() for finding in self.findings],
            "items": [item.as_dict() for item in self.items],
        }

    def to_text(self) -> str:
        summary = self.as_dict()["summary"]
        lines = [
            f"RAG-Anything content_list audit: {self.status.upper()}",
            f"Input: {self.input_path}",
            f"Items: {summary['total_items']}",
            f"Blockers: {summary['blockers']}",
            f"Warnings: {summary['warnings']}",
            f"Type distribution: {summary['type_distribution']}",
            f"Multimodal items without context: {summary['multimodal_without_context']}",
            "",
        ]
        for finding in self.findings:
            location = (
                f"item {finding.item_index}"
                if finding.item_index is not None
                else "global"
            )
            lines.append(
                f"[{finding.severity.upper()}] {location} "
                f"{finding.content_type}.{finding.field}: {finding.message}"
            )
            lines.append(f"  -> {finding.recommendation}")
        return "\n".join(lines)

    def to_markdown(self) -> str:
        summary = self.as_dict()["summary"]
        lines = [
            "# RAG-Anything Content List Audit",
            "",
            f"- Generated at: `{self.generated_at}`",
            f"- Input: `{self.input_path}`",
            f"- Status: `{self.status}`",
            f"- Context mode: `{self.context_mode}`",
            f"- Context window: `{self.context_window}`",
            f"- Context types: `{', '.join(self.context_types)}`",
            f"- Total items: {summary['total_items']}",
            f"- Blockers: {summary['blockers']}",
            f"- Warnings: {summary['warnings']}",
            f"- Multimodal items without context: {summary['multimodal_without_context']}",
            "",
            "## Type Distribution",
            "",
            "| Type | Count |",
            "| --- | ---: |",
        ]
        for content_type, count in sorted(summary["type_distribution"].items()):
            lines.append(f"| `{content_type}` | {count} |")

        lines.extend(
            [
                "",
                "## Findings",
                "",
                "| Severity | Item | Type | Field | Finding | Recommendation |",
                "| --- | ---: | --- | --- | --- | --- |",
            ]
        )
        if self.findings:
            for finding in self.findings:
                item_index = "" if finding.item_index is None else str(finding.item_index)
                message = finding.message.replace("|", "\\|")
                recommendation = finding.recommendation.replace("|", "\\|")
                lines.append(
                    f"| `{finding.severity}` | {item_index} | "
                    f"`{finding.content_type}` | `{finding.field}` | "
                    f"{message} | {recommendation} |"
                )
        else:
            lines.append("| `pass` |  | `all` | `all` | No findings | No action needed |")

        lines.extend(
            [
                "",
                "## Item Audit",
                "",
                "| Index | Type | Page | Status | Text Chars | Captions | Context Items | Context Chars |",
                "| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for item in self.items:
            page = "" if item.page_idx is None else str(item.page_idx)
            lines.append(
                f"| {item.index} | `{item.content_type}` | {page} | `{item.status}` | "
                f"{item.text_chars} | {item.caption_count} | "
                f"{item.context_items} | {item.context_chars} |"
            )
        lines.append("")
        return "\n".join(lines)


def add_finding(
    findings: list[Finding],
    severity: str,
    item_index: int | None,
    content_type: str,
    field: str,
    message: str,
    recommendation: str,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            item_index=item_index,
            content_type=content_type,
            field=field,
            message=message,
            recommendation=recommendation,
        )
    )


def load_content_list(input_path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("content_list"), list):
        return payload["content_list"]
    raise ValueError("Expected a JSON list or an object with a content_list list")


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def joined_caption_count(item: dict[str, Any], content_type: str) -> int:
    if content_type == "image":
        captions = normalize_list(item.get("image_caption")) + normalize_list(
            item.get("img_caption")
        )
        return len(captions)
    if content_type == "table":
        return len(normalize_list(item.get("table_caption")))
    if content_type == "equation":
        captions = normalize_list(item.get("equation_caption"))
        return len(captions)
    return 0


def text_for_context(item: dict[str, Any], context_types: set[str]) -> str:
    content_type = str(item.get("type", "text"))
    if content_type not in context_types:
        return ""
    if content_type == "text":
        return str(item.get("text", "")).strip()
    if content_type == "image":
        captions = normalize_list(item.get("image_caption")) + normalize_list(
            item.get("img_caption")
        )
        return " ".join(captions)
    if content_type == "table":
        return " ".join(normalize_list(item.get("table_caption")))
    if content_type == "equation":
        return str(item.get("text", "") or item.get("latex", "")).strip()
    return str(item.get("content", "")).strip()


def table_shape(table_body: Any) -> tuple[int, int]:
    if isinstance(table_body, list):
        rows = len(table_body)
        columns = max((len(row) for row in table_body if isinstance(row, list)), default=0)
        return rows, columns

    lines = [line.strip() for line in str(table_body).splitlines() if line.strip()]
    data_lines = [line for line in lines if not set(line.replace("|", "").strip()) <= {"-", ":"}]
    rows = len(data_lines)
    columns = 0
    for line in data_lines:
        if "|" in line:
            cells = [cell for cell in line.strip("|").split("|")]
            columns = max(columns, len(cells))
    return rows, columns


def is_placeholder_path(path_text: str) -> bool:
    normalized = path_text.lower().replace("\\", "/")
    return any(marker in normalized for marker in PLACEHOLDER_MARKERS)


def audit_schema_item(
    item: Any,
    index: int,
    max_image_size_mb: int,
) -> ItemAudit:
    findings: list[Finding] = []

    if not isinstance(item, dict):
        add_finding(
            findings,
            "fail",
            index,
            "unknown",
            "item",
            "Content item is not a JSON object.",
            "Use a dictionary for each content_list entry.",
        )
        return ItemAudit(index=index, content_type="unknown", page_idx=None, findings=findings)

    content_type = str(item.get("type", "text") or "text")
    page_idx_value = item.get("page_idx")
    page_idx = page_idx_value if isinstance(page_idx_value, int) and not isinstance(page_idx_value, bool) else None

    if not isinstance(item.get("type", "text"), str):
        add_finding(
            findings,
            "fail",
            index,
            content_type,
            "type",
            "The type field must be a string.",
            "Set type to text, image, table, equation, or a custom string.",
        )

    if page_idx is None:
        add_finding(
            findings,
            "fail",
            index,
            content_type,
            "page_idx",
            "Missing or non-integer page_idx.",
            "Set a 0-based integer page_idx so page context extraction is reliable.",
        )
    elif page_idx < 0:
        add_finding(
            findings,
            "fail",
            index,
            content_type,
            "page_idx",
            "page_idx is negative.",
            "Use 0-based non-negative page indexes.",
        )

    text_chars = 0
    caption_count = joined_caption_count(item, content_type)
    image_path = ""
    table_rows = 0
    table_columns = 0

    if content_type == "text":
        text = str(item.get("text", "")).strip()
        text_chars = len(text)
        if not text:
            add_finding(
                findings,
                "fail",
                index,
                content_type,
                "text",
                "Text item has empty text.",
                "Add non-empty text or remove the item before insertion.",
            )

    elif content_type == "image":
        image_path = str(item.get("img_path", "")).strip()
        if not image_path:
            add_finding(
                findings,
                "fail",
                index,
                content_type,
                "img_path",
                "Image item has no img_path.",
                "Provide an absolute path to an existing local image file.",
            )
        else:
            path = Path(image_path).expanduser()
            if is_placeholder_path(image_path):
                add_finding(
                    findings,
                    "fail",
                    index,
                    content_type,
                    "img_path",
                    "Image path looks like a placeholder.",
                    "Replace the placeholder with a real absolute image path.",
                )
            if not path.is_absolute():
                add_finding(
                    findings,
                    "fail",
                    index,
                    content_type,
                    "img_path",
                    "Image path is not absolute.",
                    "Use an absolute path because direct insertion validates local image files.",
                )
            if path.suffix.lower() not in IMAGE_EXTENSIONS:
                add_finding(
                    findings,
                    "fail",
                    index,
                    content_type,
                    "img_path",
                    "Image extension is not in the supported image extension set.",
                    "Use jpg, jpeg, png, gif, bmp, webp, tiff, or tif.",
                )
            if path.exists():
                if path.is_symlink():
                    add_finding(
                        findings,
                        "fail",
                        index,
                        content_type,
                        "img_path",
                        "Image path is a symlink.",
                        "Use a direct file path; image validation blocks symlinks.",
                    )
                elif path.stat().st_size > max_image_size_mb * 1024 * 1024:
                    add_finding(
                        findings,
                        "fail",
                        index,
                        content_type,
                        "img_path",
                        f"Image file is larger than {max_image_size_mb} MB.",
                        "Compress the image or increase the limit intentionally.",
                    )
            else:
                add_finding(
                    findings,
                    "fail",
                    index,
                    content_type,
                    "img_path",
                    "Image path does not exist locally.",
                    "Create the file, fix the path, or remove the image item.",
                )
        if caption_count == 0:
            add_finding(
                findings,
                "warn",
                index,
                content_type,
                "image_caption",
                "Image item has no caption.",
                "Add image_caption or img_caption to improve multimodal context and citations.",
            )

    elif content_type == "table":
        table_body = item.get("table_body", item.get("text", ""))
        if not str(table_body).strip():
            add_finding(
                findings,
                "fail",
                index,
                content_type,
                "table_body",
                "Table item has empty table_body.",
                "Add a markdown/string table_body or remove the item.",
            )
        else:
            table_rows, table_columns = table_shape(table_body)
            text_chars = len(str(table_body))
            if table_rows <= 1 or table_columns <= 1:
                add_finding(
                    findings,
                    "warn",
                    index,
                    content_type,
                    "table_body",
                    "Table body does not look like a multi-row, multi-column table.",
                    "Check whether the parser produced a usable table representation.",
                )
        if caption_count == 0:
            add_finding(
                findings,
                "warn",
                index,
                content_type,
                "table_caption",
                "Table item has no caption.",
                "Add table_caption so retrieval can preserve table meaning.",
            )

    elif content_type == "equation":
        equation_text = str(item.get("text", "")).strip()
        latex_text = str(item.get("latex", "")).strip()
        text_chars = len(equation_text or latex_text)
        if not equation_text and not latex_text:
            add_finding(
                findings,
                "fail",
                index,
                content_type,
                "text",
                "Equation item has neither text nor latex.",
                "Provide text and optionally latex/text_format for equation processing.",
            )
        if latex_text and not item.get("text_format"):
            add_finding(
                findings,
                "warn",
                index,
                content_type,
                "text_format",
                "Equation has latex but no text_format.",
                "Set text_format to LaTeX so downstream prompts can preserve notation.",
            )
        if latex_text and not equation_text:
            add_finding(
                findings,
                "warn",
                index,
                content_type,
                "text",
                "Equation has latex but no text description.",
                "Add text because current equation chunk generation reads the text field.",
            )

    else:
        generic_text = str(item.get("content", item.get("text", ""))).strip()
        text_chars = len(generic_text)
        if not generic_text:
            add_finding(
                findings,
                "warn",
                index,
                content_type,
                "content",
                "Custom content item has neither content nor text.",
                "Add a serializable content or text field for generic processing.",
            )

    return ItemAudit(
        index=index,
        content_type=content_type,
        page_idx=page_idx,
        text_chars=text_chars,
        caption_count=caption_count,
        image_path=image_path,
        table_rows=table_rows,
        table_columns=table_columns,
        findings=findings,
    )


def add_context_findings(
    content_list: list[dict[str, Any]],
    items: list[ItemAudit],
    context_mode: str,
    context_window: int,
    context_types: set[str],
) -> None:
    for audited_item in items:
        if audited_item.content_type == "text":
            continue

        source_item = content_list[audited_item.index]
        if not isinstance(source_item, dict):
            continue
        context_texts: list[str] = []

        if context_mode == "page":
            if audited_item.page_idx is None:
                continue
            start_page = max(0, audited_item.page_idx - context_window)
            end_page = audited_item.page_idx + context_window
            for candidate_index, candidate in enumerate(content_list):
                if candidate_index == audited_item.index:
                    continue
                if not isinstance(candidate, dict):
                    continue
                candidate_page = candidate.get("page_idx")
                if not isinstance(candidate_page, int) or isinstance(candidate_page, bool):
                    continue
                if start_page <= candidate_page <= end_page:
                    text = text_for_context(candidate, context_types)
                    if text:
                        context_texts.append(text)
        else:
            start_index = max(0, audited_item.index - context_window)
            end_index = min(len(content_list) - 1, audited_item.index + context_window)
            for candidate_index in range(start_index, end_index + 1):
                if candidate_index == audited_item.index:
                    continue
                if not isinstance(content_list[candidate_index], dict):
                    continue
                text = text_for_context(content_list[candidate_index], context_types)
                if text:
                    context_texts.append(text)

        audited_item.context_items = len(context_texts)
        audited_item.context_chars = sum(len(text) for text in context_texts)

        if not context_texts:
            add_finding(
                audited_item.findings,
                "warn",
                audited_item.index,
                audited_item.content_type,
                "context",
                f"No {context_mode}-window context was found for this multimodal item.",
                "Add nearby text/captions or increase the context window before insertion.",
            )


def build_audit(args: argparse.Namespace) -> ContentListAudit:
    input_path = Path(args.input).expanduser().resolve()
    content_list = load_content_list(input_path)

    items = [
        audit_schema_item(item, index, args.max_image_size_mb)
        for index, item in enumerate(content_list)
    ]
    context_types = {item.strip() for item in args.context_types.split(",") if item.strip()}
    add_context_findings(
        content_list,
        items,
        args.context_mode,
        args.context_window,
        context_types,
    )

    findings = [finding for item in items for finding in item.findings]
    if not content_list:
        add_finding(
            findings,
            "fail",
            None,
            "global",
            "content_list",
            "The content list is empty.",
            "Provide at least one text or multimodal content item.",
        )

    return ContentListAudit(
        input_path=str(input_path),
        generated_at=datetime.now(timezone.utc).isoformat(),
        context_mode=args.context_mode,
        context_window=args.context_window,
        context_types=sorted(context_types),
        items=items,
        findings=findings,
    )


def write_outputs(audit: ContentListAudit, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "content_list_audit_summary.json").write_text(
        json.dumps(audit.as_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "content_list_audit_summary.md").write_text(
        audit.to_markdown(),
        encoding="utf-8",
    )

    with (output_dir / "content_list_audit_items.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "index",
                "content_type",
                "page_idx",
                "status",
                "text_chars",
                "caption_count",
                "context_items",
                "context_chars",
                "image_path",
                "table_rows",
                "table_columns",
            ],
        )
        writer.writeheader()
        for item in audit.items:
            row = item.as_dict()
            row.pop("findings")
            writer.writerow(row)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a RAG-Anything content_list JSON file before insertion."
    )
    parser.add_argument("--input", required=True, help="Path to content_list JSON.")
    parser.add_argument(
        "--output-dir",
        default="content_list_audit",
        help="Directory for markdown, JSON, and CSV audit outputs.",
    )
    parser.add_argument(
        "--context-mode",
        choices=["page", "chunk"],
        default="page",
        help="Context mode to simulate for multimodal items.",
    )
    parser.add_argument(
        "--context-window",
        type=int,
        default=1,
        help="Page or chunk window to use when checking context availability.",
    )
    parser.add_argument(
        "--context-types",
        default="text",
        help="Comma-separated content types considered usable context.",
    )
    parser.add_argument(
        "--max-image-size-mb",
        type=int,
        default=50,
        help="Maximum accepted image size, matching runtime image validation.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when blockers are found.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.context_window < 0:
        print("context-window must be non-negative", file=sys.stderr)
        return 2

    try:
        audit = build_audit(args)
    except (OSError, ValueError) as exc:
        print(f"Failed to audit content list: {exc}", file=sys.stderr)
        return 2

    write_outputs(audit, Path(args.output_dir).expanduser())
    print(audit.to_text())
    if args.strict and audit.blockers:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
