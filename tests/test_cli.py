from __future__ import annotations

from pathlib import Path

import pytest

from jsonlinter.cli import main


@pytest.fixture()
def sample(tmp_path: Path) -> Path:
    path = tmp_path / "sample.json"
    path.write_text('{"a": 1}', encoding="utf-8")
    return path


def test_main_zero_on_clean(sample: Path) -> None:
    assert main([str(sample)]) == 0


def test_main_nonzero_on_whitespace(sample: Path) -> None:
    sample.write_text('{"a"\t: 1,}', encoding="utf-8")
    assert main([str(sample)]) == 1


def test_main_help_exits_zero() -> None:
    assert main(["--help"]) == 0
