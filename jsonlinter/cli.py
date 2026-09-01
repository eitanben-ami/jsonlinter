from __future__ import annotations

import argparse
import json as stdlib_json
import sys
from typing import Iterable, List, Optional, Sequence

from jsonlinter.linter import Issue, lint_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jsonlinter", description="Lint JSON files for common formatting issues.")
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to lint")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recurse into directories")
    parser.add_argument("--format", choices=["plain", "json"], default="plain", help="Output format")
    parser.add_argument("--max-issues", type=int, default=200, help="Stop after this many issues")
    return parser


def collect_issues(paths: Sequence[str], recursive: bool) -> List[Issue]:
    issues: List[Issue] = []
    for path in paths:
        for issue in lint_path(path, recursive=recursive):
            issues.append(issue)
    return issues


def render_plain(issues: Iterable[Issue]) -> str:
    return "\n".join(f"{issue.path}:{issue.lineno}:{issue.col}: {issue.message}" for issue in issues)


def render_json(issues: Iterable[Issue]) -> str:
    return stdlib_json.dumps([issue.to_dict() for issue in issues], indent=2)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 1

    issues = collect_issues(args.paths, args.recursive)
    if issues:
        issues = sorted(issues, key=lambda issue: (issue.lineno, issue.col, issue.path, issue.message))[: args.max_issues]
        text = render_plain(issues) if args.format == "plain" else render_json(issues)
        sys.stdout.write(text + "\n" if not text.endswith("\n") else text)
        return 1
    return 0
