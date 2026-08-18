"""Tests for Phase 2.1 knowledge-session ingestion."""

from __future__ import annotations

import json
import unittest

from tools.consolidator.input import ingest, ingest_json, utc_timestamp


class KnowledgeInputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = {
            "source": "session",
            "timestamp": "2026-08-18T20:00:00Z",
            "session": "phase-2-1-test",
            "items": [
                {
                    "id": "obs-001",
                    "text": "Phase 2.1 accepts knowledge produced by a session.",
                }
            ],
        }

    def test_ingest_accepts_valid_payload_without_reinterpreting_items(self) -> None:
        result = ingest(self.payload)
        self.assertEqual(result.source, "session")
        self.assertEqual(result.session, "phase-2-1-test")
        self.assertEqual(result.items, self.payload["items"])

    def test_ingest_json_accepts_json_text(self) -> None:
        result = ingest_json(json.dumps(self.payload))
        self.assertEqual(result.to_dict(), self.payload)

    def test_ingest_rejects_missing_source(self) -> None:
        payload = dict(self.payload)
        payload.pop("source")
        with self.assertRaises(ValueError):
            ingest(payload)

    def test_ingest_rejects_invalid_timestamp(self) -> None:
        payload = dict(self.payload)
        payload["timestamp"] = "not-a-timestamp"
        with self.assertRaises(ValueError):
            ingest(payload)

    def test_ingest_rejects_empty_items(self) -> None:
        payload = dict(self.payload)
        payload["items"] = []
        with self.assertRaises(ValueError):
            ingest(payload)

    def test_utc_timestamp_is_iso8601_utc(self) -> None:
        timestamp = utc_timestamp()
        self.assertTrue(timestamp.endswith("Z"))
        self.assertIn("T", timestamp)


if __name__ == "__main__":
    unittest.main()
