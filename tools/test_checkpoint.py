"""Executable checks for deterministic MEMORY_CHECKPOINT generation."""

import unittest
from datetime import datetime, timezone

from tools.checkpoint import build_checkpoint


class CheckpointBuilderTest(unittest.TestCase):
    def test_builds_traceable_checkpoint(self) -> None:
        content = build_checkpoint(
            checkpoint_id="MC-2026-08-17-001",
            timestamp=datetime(2026, 8, 17, 10, 0, tzinfo=timezone.utc),
            project="Hato AI Architect",
            source="conversation",
            status="consolidated",
            context="The memory cycle was audited.",
            decisions=["GitHub remains the persistent source of truth."],
            current_state=["Historical memory audited."],
            next_steps=["Implement daily commit automation."],
            commit_sha="abc123",
        )
        self.assertIn("MC-2026-08-17-001", content)
        self.assertIn("abc123", content)
        self.assertIn("GitHub remains the persistent source of truth.", content)

    def test_rejects_invalid_checkpoint_id(self) -> None:
        with self.assertRaises(ValueError):
            build_checkpoint(
                checkpoint_id="INVALID",
                timestamp=datetime.now(timezone.utc),
                project="Hato AI Architect",
                source="conversation",
                status="draft",
                context="x",
                decisions=[],
                current_state=[],
                next_steps=[],
            )

    def test_rejects_empty_context(self) -> None:
        with self.assertRaises(ValueError):
            build_checkpoint(
                checkpoint_id="MC-2026-08-17-002",
                timestamp=datetime.now(timezone.utc),
                project="Hato AI Architect",
                source="conversation",
                status="draft",
                context="",
                decisions=[],
                current_state=[],
                next_steps=[],
            )


if __name__ == "__main__":
    unittest.main()
