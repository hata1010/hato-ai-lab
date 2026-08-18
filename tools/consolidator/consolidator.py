"""Command-line runner for the deterministic Hato AI consolidator."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import KnowledgeItem
from .rules import consolidate_item


def load_payload(source: str) -> dict[str, Any]:
    if source == "-":
        return json.load(sys.stdin)
    return json.loads(Path(source).read_text(encoding="utf-8"))


def build_result(payload: dict[str, Any]) -> dict[str, Any]:
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError("'items' must be a list")

    results = []
    for raw in items:
        if not isinstance(raw, dict):
            raise ValueError("Every item must be an object")
        item = KnowledgeItem(
            id=str(raw["id"]),
            text=str(raw["text"]),
            classification=str(raw["classification"]),
            relevant=bool(raw.get("relevant", True)),
            existing_matches=list(raw.get("existing_matches", [])),
            confidence=raw.get("confidence"),
            source=raw.get("source", payload.get("source")),
        )
        results.append(consolidate_item(item).to_dict())

    return {
        "schema": "hato-ai-consolidation-result/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": payload.get("source"),
        "session": payload.get("session"),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Hato AI deterministic consolidator")
    parser.add_argument("input", help="JSON input path, or '-' for stdin")
    args = parser.parse_args()

    try:
        result = build_result(load_payload(args.input))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
