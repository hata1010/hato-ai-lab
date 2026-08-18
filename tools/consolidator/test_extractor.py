"""Tests for Consolidator Phase 2.2 semantic extraction."""

from __future__ import annotations

import unittest

from tools.consolidator.extractor import extract, extract_text
from tools.consolidator.input import ingest


class SemanticExtractorTests(unittest.TestCase):
    def test_extracts_decision(self) -> None:
        category, evidence = extract_text("Decidimos mantener el Scheduler sin modificarlo.")
        self.assertEqual(category, "decision")
        self.assertEqual(evidence, "decidimos")

    def test_extracts_fact(self) -> None:
        category, _ = extract_text("Está confirmado que la prueba E2E pasó.")
        self.assertEqual(category, "fact")

    def test_extracts_change(self) -> None:
        category, _ = extract_text("Actualizamos el workflow de continuidad.")
        self.assertEqual(category, "change")

    def test_extracts_objective(self) -> None:
        category, _ = extract_text("Objetivo: cerrar la Fase 2 con E2E PASS.")
        self.assertEqual(category, "objective")

    def test_extracts_constraint(self) -> None:
        category, _ = extract_text("No debemos modificar componentes que ya funcionan.")
        self.assertEqual(category, "constraint")

    def test_falls_back_to_relevant_knowledge(self) -> None:
        category, _ = extract_text("El repositorio es la fuente de verdad del proyecto.")
        self.assertEqual(category, "relevant_knowledge")

    def test_extracts_all_items_from_phase_2_1_input(self) -> None:
        session = ingest(
            {
                "source": "session",
                "timestamp": "2026-08-18T12:00:00Z",
                "session": "phase-2-2-test",
                "items": [
                    {"id": "d-1", "text": "Decidimos mantener el contrato."},
                    {"id": "f-1", "text": "Está confirmado que Integrity pasó."},
                ],
            }
        )
        result = extract(session)
        self.assertEqual([item.category for item in result], ["decision", "fact"])
        self.assertEqual([item.id for item in result], ["d-1", "f-1"])
        self.assertTrue(all(item.relevant for item in result))

    def test_rejects_empty_text(self) -> None:
        with self.assertRaises(ValueError):
            extract_text("   ")


if __name__ == "__main__":
    unittest.main()
