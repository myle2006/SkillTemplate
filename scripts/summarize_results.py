#!/usr/bin/env python3
"""Summarize normalized test-result and defect CSV files as Markdown."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"Missing CSV header: {path.name}")
        headers = [key.strip().lower() for key in reader.fieldnames]
        if len(headers) != len(set(headers)):
            raise ValueError(f"Duplicate CSV headers: {path.name}")
        records = list(reader)
        if any(None in row or any(value is None for value in row.values()) for row in records):
            raise ValueError(f"Inconsistent CSV row width: {path.name}")
        return records


def pick(row: dict[str, str], names: tuple[str, ...]) -> str:
    lowered = {key.strip().lower(): (value or "").strip() for key, value in row.items() if key}
    return next((lowered[name] for name in names if name in lowered), "")


def table(counter: Counter[str]) -> list[str]:
    return ["| Category | Count |", "|---|---:|"] + [f"| {key} | {value} |" for key, value in sorted(counter.items())]


def summarize(result_path: Path, defect_path: Path | None, title: str) -> str:
    result_rows = read_rows(result_path)
    identifiers = [pick(row, ("test case id",)) for row in result_rows]
    if any(not identifier for identifier in identifiers) or len(identifiers) != len(set(identifiers)):
        raise ValueError("Each result requires a unique Test Case ID; select one run and use dataset-specific IDs.")
    aliases = {"PASSED": "PASS", "FAILED": "FAIL", "NOT_RUN": "NOT RUN"}
    statuses = Counter()
    for row in result_rows:
        raw = pick(row, ("status", "result", "test status")).upper()
        status = aliases.get(raw, raw)
        if status not in {"PASS", "FAIL", "BLOCKED", "ERROR", "NOT RUN"}:
            raise ValueError(f"Unknown or missing status {raw!r}; map it explicitly before summarizing.")
        statuses[status] += 1
    executed = sum(statuses.get(key, 0) for key in ("PASS", "PASSED", "FAIL", "FAILED", "BLOCKED", "ERROR"))
    passed = statuses.get("PASS", 0) + statuses.get("PASSED", 0)
    failed = statuses.get("FAIL", 0) + statuses.get("FAILED", 0)
    denominator = passed + failed
    pass_rate = f"{passed / denominator:.1%}" if denominator else "n.a."
    lines = [
        f"# {title}", "", "## Execution summary", "",
        f"- Supplied test records: {len(result_rows)}",
        f"- Attempted records (including BLOCKED and ERROR): {executed}",
        f"- Pass rate (PASS / PASS+FAIL): {pass_rate}", "",
        "BLOCKED, ERROR, and NOT RUN are excluded from the pass-rate denominator.",
        "Coverage and total planned scope cannot be inferred from this CSV alone.", "",
    ] + table(statuses)
    if defect_path:
        defect_rows = read_rows(defect_path)
        defect_ids = [pick(row, ("defect id",)) for row in defect_rows]
        if any(not value for value in defect_ids) or len(defect_ids) != len(set(defect_ids)):
            raise ValueError("Each defect requires a unique Defect ID.")
        severities = Counter((pick(row, ("severity",)) or "UNSPECIFIED").upper() for row in defect_rows)
        lines += ["", "## Defect summary", "", f"- Defects: {len(defect_rows)}", ""] + table(severities)
    lines += [
        "", "## Required review", "",
        "- Confirm scope, build, environment, and excluded tests.",
        "- Review failed, blocked, and error records individually.",
        "- Record residual risks and any release recommendation separately.", "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="CSV with a Status or Result column")
    parser.add_argument("--defects", type=Path, help="CSV with a Severity column")
    parser.add_argument("--title", default="Test summary")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        text = summarize(args.results, args.defects, args.title)
    except (ValueError, OSError, csv.Error) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
