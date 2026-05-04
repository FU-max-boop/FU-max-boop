#!/usr/bin/env python3
"""
Offline corpus audit for DeepResearch-ReportEval reports.

The official judge scripts use LLM calls for quality and repeatability scoring.
This script reproduces the static, data-level part of the pipeline on the
released report corpus and adds deterministic diagnostics for structure,
citations, references, and cross-section redundancy risk. It does not call LLMs,
Jina, Firecrawl, or any external service.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
CITATION_RE = re.compile(r"\[(\d+)\]")
REFERENCE_LINE_RE = re.compile(r"^\[(\d+)\]\s*,?\s*(.*)\s*$")
TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")

STOPWORDS = {
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "also",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "her",
    "here",
    "hers",
    "him",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "itself",
    "more",
    "most",
    "no",
    "nor",
    "not",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "our",
    "out",
    "over",
    "own",
    "same",
    "she",
    "should",
    "so",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "theirs",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "whom",
    "why",
    "will",
    "with",
    "would",
    "you",
    "your",
}


@dataclass
class Section:
    title: str
    body: str
    start: int
    end: int

    @property
    def text(self) -> str:
        if self.title == "Beginning of the report":
            return self.body
        return f"## {self.title}\n{self.body}".strip()


def read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            records.append(json.loads(line))
            if limit is not None and len(records) >= limit:
                break
    return records


def load_topic_categories(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    topic_to_category: dict[str, str] = {}
    for record in read_jsonl(path):
        topic = str(record.get("topic", "")).strip()
        category = str(record.get("category_str", "")).strip()
        if topic and category:
            topic_to_category[topic] = category
    return topic_to_category


def parse_sections(report: str) -> list[Section]:
    matches = list(HEADING_RE.finditer(report))
    if not matches:
        return [Section("Full report", report.strip(), 0, len(report))]

    sections: list[Section] = []
    first = matches[0]
    if first.start() > 0:
        intro = report[: first.start()].strip()
        if intro:
            sections.append(Section("Beginning of the report", intro, 0, first.start()))

    for idx, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(report)
        sections.append(
            Section(
                title=match.group(1).strip(),
                body=report[body_start:body_end].strip(),
                start=match.start(),
                end=body_end,
            )
        )
    return sections


def extract_title(report: str) -> str:
    match = TITLE_RE.search(report)
    return match.group(1).strip() if match else ""


def is_reference_section(section: Section) -> bool:
    normalized = section.title.lower().strip(" :")
    return normalized in {"reference", "references"}


def split_body_and_references(sections: list[Section]) -> tuple[str, Section | None]:
    ref_section = next((section for section in sections if is_reference_section(section)), None)
    if ref_section is None:
        return "\n\n".join(section.text for section in sections), None
    body = "\n\n".join(section.text for section in sections if section.start < ref_section.start)
    return body, ref_section


def parse_references(ref_section: Section | None) -> dict[int, str]:
    if ref_section is None:
        return {}
    refs: dict[int, str] = {}
    for line in ref_section.body.splitlines():
        match = REFERENCE_LINE_RE.match(line.strip())
        if match:
            refs[int(match.group(1))] = match.group(2).strip()
    return refs


def tokenize(text: str) -> list[str]:
    return [
        token.lower()
        for token in TOKEN_RE.findall(text)
        if len(token) > 2 and token.lower() not in STOPWORDS
    ]


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    overlap = set(left) & set(right)
    dot = sum(left[token] * right[token] for token in overlap)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def section_citations(section: Section) -> set[int]:
    return {int(match) for match in CITATION_RE.findall(section.text)}


def topic_keyword_coverage(topic: str, report_title: str, sections: list[Section]) -> float:
    topic_tokens = set(tokenize(topic))
    if not topic_tokens:
        return 0.0
    heading_text = " ".join(
        section.title for section in sections if not is_reference_section(section)
    )
    target_tokens = set(tokenize(f"{report_title} {heading_text}"))
    return len(topic_tokens & target_tokens) / len(topic_tokens)


def redundancy_pairs(
    sections: list[Section],
    min_section_chars: int,
    top_k: int,
) -> list[dict[str, Any]]:
    candidates = [
        section
        for section in sections
        if not is_reference_section(section)
        and len(section.text) >= min_section_chars
        and section.title != "Beginning of the report"
    ]
    token_counters = [Counter(tokenize(section.text)) for section in candidates]
    token_sets = [set(counter) for counter in token_counters]
    citation_sets = [section_citations(section) for section in candidates]

    pairs: list[dict[str, Any]] = []
    for left_idx in range(len(candidates) - 1):
        for right_idx in range(left_idx + 1, len(candidates)):
            lexical_cosine = cosine_similarity(
                token_counters[left_idx],
                token_counters[right_idx],
            )
            lexical_jaccard = jaccard_similarity(token_sets[left_idx], token_sets[right_idx])
            citation_jaccard = jaccard_similarity(citation_sets[left_idx], citation_sets[right_idx])
            risk = max(lexical_cosine, 0.7 * lexical_cosine + 0.3 * citation_jaccard)
            pairs.append(
                {
                    "section_a": candidates[left_idx].title,
                    "section_b": candidates[right_idx].title,
                    "lexical_cosine": round(lexical_cosine, 4),
                    "lexical_jaccard": round(lexical_jaccard, 4),
                    "citation_jaccard": round(citation_jaccard, 4),
                    "redundancy_risk": round(risk, 4),
                }
            )

    pairs.sort(key=lambda item: item["redundancy_risk"], reverse=True)
    return pairs[:top_k]


def count_words(text: str) -> int:
    return len(TOKEN_RE.findall(text))


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(statistics.median(values))


def analyze_record(
    record: dict[str, Any],
    index: int,
    topic_to_category: dict[str, str],
    min_section_chars: int,
    redundancy_threshold: float,
    top_pairs: int,
) -> dict[str, Any]:
    topic = str(record.get("topic", "")).strip()
    report = str(record.get("report", "")).strip()
    sections = parse_sections(report)
    report_title = extract_title(report)
    body_text, ref_section = split_body_and_references(sections)
    refs = parse_references(ref_section)
    body_citations = {int(match) for match in CITATION_RE.findall(body_text)}

    dangling = sorted(citation for citation in body_citations if citation not in refs)
    unused_refs = sorted(ref_id for ref_id in refs if ref_id not in body_citations)
    empty_refs = sorted(ref_id for ref_id, value in refs.items() if not value)

    non_ref_sections = [section for section in sections if not is_reference_section(section)]
    section_lengths = [len(section.text) for section in non_ref_sections]
    word_count = count_words(report)
    table_lines = len(TABLE_LINE_RE.findall(report))
    pairs = redundancy_pairs(sections, min_section_chars=min_section_chars, top_k=top_pairs)
    top_pair = pairs[0] if pairs else {}
    high_risk_pairs = [
        pair for pair in pairs if pair["redundancy_risk"] >= redundancy_threshold
    ]
    keyword_coverage = topic_keyword_coverage(topic, report_title, sections)

    flags: list[str] = []
    if ref_section is None:
        flags.append("missing_reference_section")
    if dangling:
        flags.append("dangling_citations")
    if empty_refs:
        flags.append("empty_references")
    if unused_refs:
        flags.append("unused_references")
    if len(non_ref_sections) < 4:
        flags.append("few_sections")
    if section_lengths and max(section_lengths) > 6500:
        flags.append("very_long_section")
    if word_count and len(body_citations) / max(word_count, 1) * 1000 < 8:
        flags.append("low_citation_density")
    if high_risk_pairs:
        flags.append("high_redundancy_risk")
    if keyword_coverage == 0:
        flags.append("zero_topic_heading_overlap")
    elif keyword_coverage < 0.18:
        flags.append("low_topic_heading_overlap")

    file_id = hashlib.md5(topic.encode("utf-8")).hexdigest()
    return {
        "index": index,
        "file_id": file_id,
        "topic": topic,
        "category": topic_to_category.get(topic, ""),
        "report_title": report_title,
        "topic_keyword_coverage": round(keyword_coverage, 4),
        "word_count": word_count,
        "char_count": len(report),
        "section_count": len(non_ref_sections),
        "median_section_chars": round(median([float(value) for value in section_lengths]), 2),
        "max_section_chars": max(section_lengths) if section_lengths else 0,
        "table_lines": table_lines,
        "citation_count": len(CITATION_RE.findall(body_text)),
        "unique_citations": len(body_citations),
        "reference_count": len(refs),
        "dangling_citation_count": len(dangling),
        "unused_reference_count": len(unused_refs),
        "empty_reference_count": len(empty_refs),
        "citation_density_per_1000_words": round(
            len(CITATION_RE.findall(body_text)) / max(word_count, 1) * 1000,
            2,
        ),
        "top_redundancy_risk": top_pair.get("redundancy_risk", 0.0),
        "top_redundancy_pair": (
            f"{top_pair.get('section_a', '')} <> {top_pair.get('section_b', '')}"
            if top_pair
            else ""
        ),
        "high_redundancy_pair_count": len(high_risk_pairs),
        "audit_risk_score": len(flags),
        "flags": ";".join(flags),
        "top_pairs": pairs,
    }


def aggregate_category(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[row.get("category") or "Uncategorized"].append(row)

    summary: list[dict[str, Any]] = []
    for category, items in sorted(buckets.items()):
        summary.append(
            {
                "category": category,
                "count": len(items),
                "avg_words": round(statistics.mean(item["word_count"] for item in items), 2),
                "avg_sections": round(statistics.mean(item["section_count"] for item in items), 2),
                "avg_citations": round(statistics.mean(item["citation_count"] for item in items), 2),
                "avg_top_redundancy_risk": round(
                    statistics.mean(item["top_redundancy_risk"] for item in items),
                    4,
                ),
                "avg_topic_keyword_coverage": round(
                    statistics.mean(item["topic_keyword_coverage"] for item in items),
                    4,
                ),
                "avg_audit_risk_score": round(
                    statistics.mean(item["audit_risk_score"] for item in items),
                    2,
                ),
            }
        )
    return summary


def compact_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "top_pairs"}


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(compact_row(rows[0]).keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(compact_row(row))


def build_summary(
    rows: list[dict[str, Any]],
    input_path: Path,
    topic_path: Path | None,
    redundancy_threshold: float,
) -> dict[str, Any]:
    top_risk_rows = sorted(
        rows,
        key=lambda row: (row["audit_risk_score"], row["top_redundancy_risk"]),
        reverse=True,
    )[:10]
    low_overlap_rows = [
        row
        for row in sorted(rows, key=lambda row: row["topic_keyword_coverage"])
        if "low_topic_heading_overlap" in row["flags"]
        or "zero_topic_heading_overlap" in row["flags"]
    ][:10]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_path": str(input_path),
        "topic_path": str(topic_path) if topic_path else None,
        "report_count": len(rows),
        "redundancy_threshold": redundancy_threshold,
        "corpus_summary": {
            "avg_words": round(statistics.mean(row["word_count"] for row in rows), 2),
            "median_words": round(statistics.median(row["word_count"] for row in rows), 2),
            "avg_sections": round(statistics.mean(row["section_count"] for row in rows), 2),
            "avg_citations": round(statistics.mean(row["citation_count"] for row in rows), 2),
            "reports_with_dangling_citations": sum(
                1 for row in rows if row["dangling_citation_count"]
            ),
            "reports_with_empty_references": sum(
                1 for row in rows if row["empty_reference_count"]
            ),
            "reports_with_high_redundancy_risk": sum(
                1 for row in rows if row["high_redundancy_pair_count"]
            ),
            "reports_with_low_topic_heading_overlap": sum(
                1 for row in rows if "low_topic_heading_overlap" in row["flags"]
            ),
            "reports_with_zero_topic_heading_overlap": sum(
                1 for row in rows if "zero_topic_heading_overlap" in row["flags"]
            ),
            "max_top_redundancy_risk": max(
                row["top_redundancy_risk"] for row in rows
            ),
        },
        "category_summary": aggregate_category(rows),
        "top_risk_reports": [compact_row(row) for row in top_risk_rows],
        "low_topic_overlap_reports": [compact_row(row) for row in low_overlap_rows],
    }


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def write_markdown(summary: dict[str, Any], path: Path) -> None:
    corpus = summary["corpus_summary"]
    lines = [
        "# DeepResearch-ReportEval Offline Corpus Audit",
        "",
        f"- Generated at: `{summary['generated_at']}`",
        f"- Input path: `{summary['input_path']}`",
        f"- Topic path: `{summary.get('topic_path') or ''}`",
        f"- Reports scanned: {summary['report_count']}",
        f"- Redundancy risk threshold: {summary['redundancy_threshold']}",
        "",
        "## Corpus Summary",
        "",
        f"- Average words per report: {corpus['avg_words']}",
        f"- Median words per report: {corpus['median_words']}",
        f"- Average sections per report: {corpus['avg_sections']}",
        f"- Average citation markers per report: {corpus['avg_citations']}",
        f"- Reports with dangling citations: {corpus['reports_with_dangling_citations']}",
        f"- Reports with empty references: {corpus['reports_with_empty_references']}",
        f"- Reports with high redundancy risk: {corpus['reports_with_high_redundancy_risk']}",
        f"- Reports with low topic-heading overlap: {corpus['reports_with_low_topic_heading_overlap']}",
        f"- Reports with zero topic-heading overlap: {corpus['reports_with_zero_topic_heading_overlap']}",
        f"- Max top redundancy risk: {corpus['max_top_redundancy_risk']}",
        "",
        "## Category Summary",
        "",
    ]
    lines.extend(
        markdown_table(
            summary["category_summary"],
            [
                "category",
                "count",
                "avg_words",
                "avg_sections",
                "avg_citations",
                "avg_top_redundancy_risk",
                "avg_topic_keyword_coverage",
                "avg_audit_risk_score",
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Top Risk Reports",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            summary["top_risk_reports"],
            [
                "index",
                "category",
                "word_count",
                "section_count",
                "reference_count",
                "empty_reference_count",
                "topic_keyword_coverage",
                "top_redundancy_risk",
                "audit_risk_score",
                "flags",
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Low Topic-Heading Overlap Reports",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            summary["low_topic_overlap_reports"],
            [
                "index",
                "category",
                "topic_keyword_coverage",
                "report_title",
                "flags",
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Metric Notes",
            "",
            "- `top_redundancy_risk` is a deterministic lexical/citation-overlap proxy, not an LLM judge score.",
            "- `topic_keyword_coverage` is the fraction of non-stopword topic keywords found in the report title/headings.",
            "- `audit_risk_score` is the number of static flags triggered for a report.",
            "- The audit is meant to triage reports before paid LLM judging and to surface corpus-level failure patterns.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run offline structure/citation/redundancy audit over report JSONL."
    )
    parser.add_argument("--inputpath", default="data/report/qwen-reports.jsonl")
    parser.add_argument("--topicpath", default="data/topic/high_quality_topics.jsonl")
    parser.add_argument("--output-dir", default="example/report_corpus_audit")
    parser.add_argument("--limit", type=int, help="Optional number of reports to scan")
    parser.add_argument("--min-section-chars", type=int, default=200)
    parser.add_argument("--redundancy-threshold", type=float, default=0.42)
    parser.add_argument("--top-pairs", type=int, default=5)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_path = Path(args.inputpath).expanduser()
    topic_path = Path(args.topicpath).expanduser() if args.topicpath else None
    output_dir = Path(args.output_dir).expanduser()

    records = read_jsonl(input_path, limit=args.limit)
    topic_to_category = load_topic_categories(topic_path)
    rows = [
        analyze_record(
            record=record,
            index=index,
            topic_to_category=topic_to_category,
            min_section_chars=args.min_section_chars,
            redundancy_threshold=args.redundancy_threshold,
            top_pairs=args.top_pairs,
        )
        for index, record in enumerate(records, 1)
    ]

    summary = build_summary(
        rows=rows,
        input_path=input_path,
        topic_path=topic_path,
        redundancy_threshold=args.redundancy_threshold,
    )

    write_csv(rows, output_dir / "report_audit_metrics.csv")
    (output_dir / "report_audit_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_markdown(summary, output_dir / "report_audit_summary.md")

    print(f"Scanned {len(rows)} report(s).")
    print(f"Wrote metrics: {output_dir / 'report_audit_metrics.csv'}")
    print(f"Wrote summary: {output_dir / 'report_audit_summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
