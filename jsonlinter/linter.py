from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterator

from jsonlinter.model import Issue


def lint_path(path: str, *, recursive: bool = False) -> Iterator[Issue]:
    p = Path(path)
    if p.is_dir():
        if not recursive:
            return
        for child in sorted(p.rglob("*.json")):
            yield from _lint_file(child)
    elif p.is_file() and p.suffix.lower() == ".json":
        yield from _lint_file(p)


def _lint_file(path: Path) -> Iterator[Issue]:
    text = path.read_text(encoding="utf-8")
    yield from _lint_text(str(path), text)


def _lint_text(path: str, text: str) -> Iterator[Issue]:
    issues = list(_collect_issues(path, text))
    issues.sort(key=lambda issue: (issue.lineno, issue.col, issue.message, issue.kind))
    seen: set[tuple[object, ...]] = set()
    for issue in issues:
        key = (issue.path, issue.lineno, issue.col, issue.message, issue.kind)
        if key not in seen:
            seen.add(key)
            yield issue


def _collect_issues(path: str, text: str) -> Iterator[Issue]:
    lines = text.splitlines()
    if not lines and text == "":
        return

    parse_error: Issue | None = None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        parse_error = Issue(
            path=path,
            lineno=max(1, exc.lineno or 1),
            col=max(1, exc.colno or 1),
            message=f"JSON parse error: {exc.msg}",
            kind="parse",
        )
        data = None

    depth = 0
    blank_run = 0
    blank_start = 0
    for lineno, line in enumerate(lines, start=1):
        if "\t" in line:
            col = line.index("\t") + 1
            yield Issue(path, lineno, col, "Tab character found", kind="format")

        stripped = line.rstrip("\r\n")
        trailing = len(stripped) - len(stripped.rstrip())
        if trailing:
            col = len(stripped.rstrip()) + 1
            yield Issue(path, lineno, col, "Trailing whitespace", kind="format")

        if re.search(r",\s*[}\]]", stripped):
            col = stripped.rindex(",") + 1
            yield Issue(path, lineno, col, "Trailing comma found", kind="format")

        if stripped == "":
            if depth > 0:
                blank_run += 1
                if blank_start == 0:
                    blank_start = lineno
            continue
        if blank_start and blank_run:
            excess = blank_run - 1
            if excess > 0:
                yield Issue(path, blank_start, 1, f"{excess} excess blank line(s) inside JSON block", kind="format")
            blank_start = 0
            blank_run = 0
        depth += stripped.count("{") + stripped.count("[")
        depth -= stripped.count("}") + stripped.count("]")

    if blank_start and blank_run:
        excess = blank_run - 1
        if excess > 0:
            yield Issue(path, blank_start, 1, f"{excess} excess blank line(s) inside JSON block", kind="format")

    if data is not None and isinstance(data, dict):
        seen_keys: set[str] = set()
        for key in data.keys():
            if key in seen_keys:
                lineno = _key_line(lines, key)
                yield Issue(path, lineno, 1, f"Duplicate top-level key: {key!r}", kind="structure")
            else:
                seen_keys.add(key)

    if parse_error is not None:
        yield parse_error


def _key_line(lines: list[str], key: str) -> int:
    for lineno, line in enumerate(lines, start=1):
        if f'"{key}"' in line or f"'{key}'" in line:
            return lineno
    return 1
