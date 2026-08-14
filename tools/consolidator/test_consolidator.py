"""Basic executable checks for the deterministic consolidator."""

import unittest

from tools.consolidator.models import KnowledgeItem
from tools.consolidator.rules import consolidate_item


class ConsolidatorRulesTest(unittest.TestCase):
    def test_new_observation_goes_to_evolutionary_memory(self) -> None:
        result = consolidate_item(
            KnowledgeItem(
                id="obs-001",
                text="An external reviewer suggested a context file.",
                classification="observation",
            )
        )
        self.assertEqual(result.comparison, "new")
        self.assertEqual(result.destination, "evolutionary_memory")
        self.assertFalse(result.requires_validation)

    def test_proposal_requires_validation(self) -> None:
        result = consolidate_item(
            KnowledgeItem(
                id="prop-001",
                text="Create a new context file.",
                classification="proposal",
            )
        )
        self.assertEqual(result.destination, "review")
        self.assertTrue(result.requires_validation)

    def test_duplicate_is_not_rewritten(self) -> None:
        result = consolidate_item(
            KnowledgeItem(
                id="obs-002",
                text="The repository has persistent memory.",
                classification="fact",
                existing_matches=["duplicate:PROJECT_HISTORY.md"],
            )
        )
        self.assertEqual(result.comparison, "duplicate")
        self.assertEqual(result.action, "skip")

    def test_contradiction_requires_review(self) -> None:
        result = consolidate_item(
            KnowledgeItem(
                id="obs-003",
                text="The project has no memory protocol.",
                classification="observation",
                existing_matches=["contradiction:CONSOLIDATOR_CONTRACT.md"],
            )
        )
        self.assertEqual(result.comparison, "contradiction")
        self.assertTrue(result.requires_validation)

    def test_irrelevant_item_is_discarded(self) -> None:
        result = consolidate_item(
            KnowledgeItem(
                id="off-topic-001",
                text="A topic unrelated to Hato.",
                classification="observation",
                relevant=False,
            )
        )
        self.assertEqual(result.destination, "discarded")
        self.assertEqual(result.action, "discard")


if __name__ == "__main__":
    unittest.main()
