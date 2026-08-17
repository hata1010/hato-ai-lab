"""Create the Hato AI Lab daily memory commit.

The command intentionally operates only on the memory/continuity paths and
never commits unrelated working-tree or pre-staged changes. It can optionally
push the result to the configured upstream branch.

Usage:
    python tools/daily_commit.py
    python tools/daily_commit.py --push
    python tools/daily_commit.py --dry-run

Environment variables:
    HATO_DAILY_COMMIT_BRANCH  Branch to commit on (default: current branch)
    HATO_DAILY_COMMIT_PATHS   Comma-separated paths to stage. If omitted,
                              the default memory/continuity paths are used.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PATHS = (
    "memory",
    "docs/memory",
    "tools/checkpoint.py",
    "tools/consolidator",
    "tools/daily_commit.py",
)


def run(*args: str) -> str:
    result = subprocess.run(
        args,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def repo_root() -> Path:
    return Path(run("git", "rev-parse", "--show-toplevel"))


def current_branch() -> str:
    return run("git", "branch", "--show-current")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Hato AI Lab daily memory commit")
    parser.add_argument("--push", action="store_true", help="push the commit to its upstream branch")
    parser.add_argument("--dry-run", action="store_true", help="show what would be committed without committing")
    args = parser.parse_args()

    root = repo_root()
    os.chdir(root)

    branch = os.getenv("HATO_DAILY_COMMIT_BRANCH") or current_branch()
    if not branch:
        raise SystemExit("ERROR: repository is in detached HEAD state")

    configured = os.getenv("HATO_DAILY_COMMIT_PATHS")
    paths = tuple(p.strip() for p in configured.split(",") if p.strip()) if configured else DEFAULT_PATHS

    # Stage only the continuity subsystem. Existing staged changes outside
    # these paths are deliberately ignored and can never enter this commit.
    subprocess.run(["git", "add", "--", *paths], check=True)
    staged = run("git", "diff", "--cached", "--name-status", "--", *paths)

    if not staged:
        print("DAILY_COMMIT: NO_CHANGES")
        return 0

    print(f"DAILY_COMMIT: BRANCH={branch}")
    print("DAILY_COMMIT: CHANGES")
    print(staged)

    if args.dry_run:
        # Restore only the paths managed by this runner. Unrelated staged
        # changes are untouched.
        subprocess.run(["git", "reset", "--", *paths], check=True)
        print("DAILY_COMMIT: DRY_RUN")
        return 0

    today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    message = f"chore(memory): daily continuity commit {today}"
    # --only is the safety boundary: unrelated staged files are excluded.
    run("git", "commit", "--only", "-m", message, "--", *paths)
    sha = run("git", "rev-parse", "HEAD")
    print(f"DAILY_COMMIT: COMMITTED={sha}")

    if args.push:
        run("git", "push", "--set-upstream", "origin", branch)
        print(f"DAILY_COMMIT: PUSHED={branch}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
