"""Controlled ingestion boundary for Hato AI knowledge sessions.

Phase 2.1 only accepts and validates session-produced knowledge. It does not
interpret natural language, classify items, write memory, or create checkpoints.
Those responsibilities remain in later phases.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO


@dataclass(frozen=True)
class KnowledgeInput:
    """Validated session payload ready for the next Consolidator stage."""

    source: str
    timestamp: str
    session: str | None
    items: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "source": self.source,
            "timestamp": self.timestamp,
            "items": self.items,
        }
        if self.session is not None:
            payload["session"] = self.session
        return payload


def _validate_timestamp(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO-8601 string")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be a valid ISO-8601 datetime") from exc
    return value


def ingest(payload: dict[str, Any]) -> KnowledgeInput:
    """Validate a knowledge-session payload without changing its content."""
    if not isinstance(payload, dict):
        raise ValueError("knowledge input must be a JSON object")

    source = payload.get("source")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("source must be a non-empty string")

    timestamp = _validate_timestamp(payload.get("timestamp"))

    session = payload.get("session")
    if session is not None and (not isinstance(session, str) or not session.strip()):
        raise ValueError("session must be a non-empty string when provided")

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("items must be a non-empty list")
    if not all(isinstance(item, dict) for item in items):
        raise ValueError("each item must be a JSON object")

    return KnowledgeInput(
        source=source,
        timestamp=timestamp,
        session=session,
        items=[dict(item) for item in items],
    )


def ingest_json(text: str) -> KnowledgeInput:
    """Parse and validate a JSON session payload."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc.msg}") from exc
    return ingest(payload)


def ingest_file(path: str | Path) -> KnowledgeInput:
    """Read, parse, and validate a JSON knowledge-session file."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return ingest_json(handle.read())


def ingest_stream(stream: TextIO | None = None) -> KnowledgeInput:
    """Read, parse, and validate JSON from a text stream."""
    return ingest_json((stream or sys.stdin).read())


def utc_timestamp() -> str:
    """Return a canonical UTC timestamp for producers creating new sessions."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
