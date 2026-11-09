#!/usr/bin/env python3
"""Create a read-only metadata inventory of common QA artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "target", "build", "dist", ".idea", ".vscode", "__pycache__"}
QA_EXTENSIONS = {".xlsx", ".xlsm", ".csv", ".tsv", ".docx", ".pdf", ".md", ".java", ".py", ".js", ".ts", ".xml"}
NAME_TAGS = {
    "requirements": re.compile(r"srs|prd|requirement|user.?story|acceptance", re.I),
    "test_cases": re.compile(r"test.?case|testcase|scenario|kich.?ban|kịch.?bản", re.I),
    "defects": re.compile(r"defect|bug|lỗi", re.I),
    "reports": re.compile(r"report|summary|result|evidence|báo.?cáo", re.I),
    "automation": re.compile(r"selenium|testng|playwright|cypress|appium|autotest|automation", re.I),
}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def classify(name: str) -> list[str]:
    return [tag for tag, pattern in NAME_TAGS.items() if pattern.search(name)] or ["other"]


def workbook_metadata(path: Path) -> dict:
    result = {"sheets": [], "error": None}
    try:
        with zipfile.ZipFile(path) as archive:
            root = ET.fromstring(archive.read("xl/workbook.xml"))
            for sheet in root.findall("m:sheets/m:sheet", NS):
                result["sheets"].append(sheet.attrib.get("name", ""))
    except Exception as exc:
        result["error"] = type(exc).__name__
    return result


def test_result_metadata(path: Path) -> dict | None:
    if path.name not in {"testng-results.xml", "junit.xml"} and "surefire" not in str(path).lower():
        return None
    try:
        attrs = ET.parse(path).getroot().attrib
        keys = ("total", "passed", "failed", "skipped", "ignored", "errors", "tests", "failures")
        return {key: attrs[key] for key in keys if key in attrs}
    except Exception as exc:
        return {"error": type(exc).__name__}


def inventory(root: Path) -> dict:
    files = []
    ext_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(names):
            path = Path(current) / name
            suffix = path.suffix.lower()
            if suffix not in QA_EXTENSIONS:
                continue
            tags = classify(name)
            item = {
                "path": path.relative_to(root).as_posix(),
                "type": suffix.lstrip("."),
                "tags": tags,
                "size_bytes": path.stat().st_size,
            }
            if suffix in {".xlsx", ".xlsm"}:
                item["workbook"] = workbook_metadata(path)
            if suffix == ".xml":
                metadata = test_result_metadata(path)
                if metadata is not None:
                    item["test_results"] = metadata
            files.append(item)
            ext_counts[suffix.lstrip(".")] += 1
            tag_counts.update(tags)
    return {
        "root": str(root.resolve()),
        "file_count": len(files),
        "by_type": dict(sorted(ext_counts.items())),
        "by_tag": dict(sorted(tag_counts.items())),
        "files": files,
    }


def to_markdown(data: dict) -> str:
    lines = ["# QA artifact inventory", "", f"Root: `{data['root']}`", f"Files: {data['file_count']}", ""]
    lines += ["## Counts by type", ""] + [f"- {key}: {value}" for key, value in data["by_type"].items()]
    lines += ["", "## Counts by tag", ""] + [f"- {key}: {value}" for key, value in data["by_tag"].items()]
    lines += ["", "## Files", ""]
    for item in data["files"]:
        detail = f" ({', '.join(item['tags'])})"
        if "workbook" in item and item["workbook"]["sheets"]:
            detail += f"; sheets: {', '.join(item['workbook']['sheets'])}"
        if "test_results" in item:
            detail += f"; results: {item['test_results']}"
        lines.append(f"- `{item['path']}`{detail}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"not a directory: {args.root}")
    data = inventory(args.root)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(data)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
