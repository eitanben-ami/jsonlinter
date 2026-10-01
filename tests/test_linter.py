from __future__ import annotations

from jsonlinter.linter import _lint_text

def test_trailing_comma_issue() -> None:
    issues = list(_lint_text("sample.json", '{"a": 1,}'))
    assert any("Trailing comma" in issue.message for issue in issues)


def test_excess_blank_lines_inside_object() -> None:
    text = '{\n\n\n"a": 1\n}'
    issues = list(_lint_text("sample.json", text))
    assert any("excess blank line(s) inside JSON block" in issue.message for issue in issues)


def test_parse_error_reported() -> None:
    issues = list(_lint_text("sample.json", '{"a": }'))
    assert any(issue.kind == "parse" for issue in issues)


def test_output_sorting_stable() -> None:
    text = '{"a"\t: 1,}'
    issues = list(_lint_text("sample.json", text))
    assert issues == sorted(issues, key=lambda issue: (issue.lineno, issue.col, issue.message, issue.kind))
