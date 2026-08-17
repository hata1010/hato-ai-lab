"""Helpers for creating deterministic MEMORY_CHECKPOINT documents."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def build_checkpoint(
    *,
    checkpoint_id: str,
    timestamp: datetime,
    project: str,
    source: str,
    status: str,
    context: str,
    decisions: list[str],
    current_state: list[str],
    next_steps: list[str],
    commit_sha: str | None = None,
    thread: str | None = None,
    parent_checkpoint: str | None = None,
) -> str:
    """Build a human-readable checkpoint from explicit structured inputs.

    ``commit_sha`` is intentionally supplied by the persistence layer. This
    keeps checkpoint generation independent from GitHub while preserving the
    contract's traceability requirement.
    """
    if not checkpoint_id.startswith("MC-"):
        raise ValueError("checkpoint_id must start with MC-")
    if not context.strip():
        raise ValueError("context cannot be empty")
    if status not in {"draft", "consolidated", "persisted", "superseded"}:
        raise ValueError("invalid checkpoint status")

    def bullets(values: list[str]) -> str:
        return "\n".join(f"- {value}" for value in values) or "- None"

    lines = [
        f"# MEMORY_CHECKPOINT: {checkpoint_id}",
        "",
        f"**Timestamp:** {timestamp.isoformat()}",
        f"**Timezone:** {timestamp.tzinfo}",
        f"**Project:** {project}",
        f"**Status:** {status}",
        f"**Source:** {source}",
        f"**Thread:** {thread or 'not specified'}",
        f"**Parent checkpoint:** {parent_checkpoint or 'none'}",
        f"**Commit SHA:** {commit_sha or 'pending persistence'}",
        "",
        "## Context",
        context.strip(),
        "",
        "## Decisions",
        bullets(decisions),
        "",
        "## Current state",
        bullets(current_state),
        "",
        "## Next steps",
        bullets(next_steps),
        "",
    ]
    return "\n".join(lines)


def write_checkpoint(path: str | Path, content: str) -> None:
    """Persist a generated checkpoint locally; Git persistence is external."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
