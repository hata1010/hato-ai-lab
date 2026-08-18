"""Append a compact, UTC-stamped continuity audit record."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument("--status", choices=("PASS", "FAIL", "INFO"), required=True)
    parser.add_argument("--detail", default="")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    target = root / "memory" / "audit" / "continuity.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": args.event,
        "status": args.status,
        "detail": args.detail,
    }
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"AUDIT_TRAIL: {json.dumps(record, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
