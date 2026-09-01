from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator


@dataclass(frozen=True)
class Issue:
    path: str
    lineno: int
    col: int
    message: str
    kind: str = field(default="lint")

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "lineno": self.lineno,
            "col": self.col,
            "message": self.message,
            "kind": self.kind,
        }
