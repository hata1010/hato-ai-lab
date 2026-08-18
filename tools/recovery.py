"""Non-destructive continuity recovery checks.

Recovery never deletes or rewrites memory automatically. It identifies the
latest checkpoint and produces a deterministic recovery recommendation.
"""
from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    checkpoint_dir = root / "docs" / "memory" / "checkpoints"
    checkpoints = sorted(checkpoint_dir.glob("MC-*.md")) if checkpoint_dir.exists() else []

    print("RECOVERY: START")
    if not checkpoints:
        print("RECOVERY: NO_CHECKPOINT_FOUND")
        print("RECOVERY: ACTION=CREATE_CHECKPOINT_BEFORE_RESTORE")
        return 1

    latest = checkpoints[-1]
    print(f"RECOVERY: LATEST_CHECKPOINT={latest.relative_to(root)}")
    print("RECOVERY: MODE=NON_DESTRUCTIVE")
    print("RECOVERY: ACTION=REVIEW_LATEST_CHECKPOINT_AND_RESTORE_EXPLICITLY")
    print("RECOVERY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
