"""Deterministic memory consolidation for Hato AI."""

from .models import ConsolidationResult, KnowledgeItem
from .rules import consolidate_item

__all__ = ["ConsolidationResult", "KnowledgeItem", "consolidate_item"]
