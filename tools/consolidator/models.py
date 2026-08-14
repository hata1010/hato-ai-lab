"""Data models for the deterministic Hato AI memory consolidator."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


VALID_CLASSIFICATIONS = {
    "fact",
    "observation",
    "proposal",
    "decision",
    "discovery",
    "architecture",
    "implementation",
    "problem",
    "solution",
    "experiment",
    "learning",
    "state",
    "next_step",
    "open_question",
}

VALID_COMPARISON_STATES = {
    "new",
    "update",
    "duplicate",
    "contradiction",
    "obsolete",
    "unverified",
}


@dataclass(frozen=True)
class KnowledgeItem:
    """A previously extracted unit of project knowledge."""

    id: str
    text: str
    classification: str
    relevant: bool = True
    existing_matches: list[str] = field(default_factory=list)
    confidence: float | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        if self.classification not in VALID_CLASSIFICATIONS:
            raise ValueError(f"Unknown classification: {self.classification}")
        if not self.text.strip():
            raise ValueError("Knowledge item text cannot be empty")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")


@dataclass(frozen=True)
class ConsolidationResult:
    """Deterministic classification result for one knowledge item."""

    id: str
    classification: str
    comparison: str
    destination: str
    action: str
    requires_validation: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
