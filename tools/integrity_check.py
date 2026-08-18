"""Validate the Hato AI Lab continuity subsystem without changing project data."""
from __future__ import annotations

import hashlib
from pathlib import Path

REQUIRED = (
    "memory",
    "docs/memory",
    "tools/checkpoint.py",
    "tools/daily_commit.py",
    "tools/consolidator",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
    return h.hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing: list[str] = []
    checks: list[str] = []
    for rel in REQUIRED:
        p = root / rel
        if not p.exists():
            missing.append(rel)
        elif p.is_file():
            checks.append(f"{rel} sha256={sha256(p)}")
        else:
            checks.append(f"{rel} present")

    print("INTEGRITY_CHECK: START")
    for item in checks:
        print(f"INTEGRITY_CHECK: OK {item}")
    for item in missing:
        print(f"INTEGRITY_CHECK: MISSING {item}")

    if missing:
        print(f"INTEGRITY_CHECK: FAIL missing={len(missing)}")
        return 1
    print("INTEGRITY_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
