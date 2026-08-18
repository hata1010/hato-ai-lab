"""Deterministic semantic extraction for Consolidator Phase 2.2.

This stage identifies a primary knowledge category from session text using
explicit linguistic cues. It does not write memory or make persistence decisions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .input import KnowledgeInput


CATEGORIES = (
    "decision",
    "fact",
    "change",
    "objective",
    "constraint",
    "relevant_knowledge",
)

_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("decision", ("decidimos", "se decidió", "hemos decidido", "decision:", "decisión:", "we decided", "decided to")),
    ("change", ("cambiamos", "cambio:", "modificamos", "actualizamos", "se modificó", "changed:", "updated:", "modified:")),
    ("objective", ("objetivo", "meta:", "queremos", "necesitamos lograr", "goal:", "objective:", "we need to achieve")),
    ("constraint", ("restricción", "restriccion", "no se puede", "no debemos", "debe mantenerse", "limitación", "limitacion", "constraint:", "must not")),
    ("fact", ("es cierto que", "se confirmó", "está confirmado", "esta confirmado", "confirmado:", "fact:", "verified:", "it is confirmed")),
)


@dataclass(frozen=True)
class ExtractedKnowledge:
    """One semantic observation extracted from a session item."""

    id: str
    text: str
    category: str
    relevant: bool
    source: str
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "category": self.category,
            "relevant": self.relevant,
            "source": self.source,
            "evidence": self.evidence,
        }


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def extract_text(text: str) -> tuple[str, str]:
    """Return (category, evidence) using deterministic linguistic cues."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("knowledge text must be a non-empty string")

    normalized = _normalize(text)
    for category, patterns in _PATTERNS:
        for pattern in patterns:
            if pattern in normalized:
                return category, pattern
    return "relevant_knowledge", "fallback: non-empty session knowledge"


def extract(session: KnowledgeInput) -> list[ExtractedKnowledge]:
    """Extract primary semantic categories from every ingested session item."""
    extracted: list[ExtractedKnowledge] = []
    for index, item in enumerate(session.items):
        text = item.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"item {index} must contain non-empty text")
        item_id = str(item.get("id") or f"item-{index + 1}")
        category, evidence = extract_text(text)
        extracted.append(
            ExtractedKnowledge(
                id=item_id,
                text=text,
                category=category,
                relevant=True,
                source=session.source,
                evidence=evidence,
            )
        )
    return extracted
