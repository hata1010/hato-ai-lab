"""Deterministic rules for routing consolidated knowledge."""

from __future__ import annotations

from .models import ConsolidationResult, KnowledgeItem


def compare_item(item: KnowledgeItem) -> str:
    """Determine the relationship with existing knowledge from explicit matches."""
    if not item.relevant:
        return "unverified"
    if not item.existing_matches:
        return "new"

    # The caller can explicitly encode the comparison state in the match marker.
    markers = {match.split(":", 1)[0].lower() for match in item.existing_matches}
    if "contradiction" in markers:
        return "contradiction"
    if "obsolete" in markers:
        return "obsolete"
    if "duplicate" in markers:
        return "duplicate"
    return "update"


def route_item(item: KnowledgeItem, comparison: str) -> ConsolidationResult:
    """Route an item without making semantic assumptions about its text."""
    if not item.relevant:
        return ConsolidationResult(
            id=item.id,
            classification=item.classification,
            comparison=comparison,
            destination="discarded",
            action="discard",
            requires_validation=False,
            reason="Item was explicitly marked as not relevant to Hato AI.",
        )

    if comparison == "contradiction":
        return ConsolidationResult(
            id=item.id,
            classification=item.classification,
            comparison=comparison,
            destination="review",
            action="flag",
            requires_validation=True,
            reason="Existing knowledge was explicitly marked as contradictory.",
        )

    if comparison == "duplicate":
        return ConsolidationResult(
            id=item.id,
            classification=item.classification,
            comparison=comparison,
            destination="existing_memory",
            action="skip",
            requires_validation=False,
            reason="The item was explicitly identified as already represented.",
        )

    if item.classification == "proposal":
        return ConsolidationResult(
            id=item.id,
            classification=item.classification,
            comparison=comparison,
            destination="review",
            action="propose",
            requires_validation=True,
            reason="External or internal proposals require evaluation before becoming project knowledge.",
        )

    if item.classification in {"decision", "architecture"}:
        return ConsolidationResult(
            id=item.id,
            classification=item.classification,
            comparison=comparison,
            destination="foundational_proposal",
            action="propose",
            requires_validation=True,
            reason="Decisions and architectural knowledge require explicit validation before Fundacional promotion.",
        )

    if item.classification == "state":
        destination = "evolutionary_memory"
    elif item.classification == "open_question":
        destination = "evolutionary_memory"
    else:
        destination = "evolutionary_memory"

    action = "record" if comparison in {"new", "update", "obsolete"} else "review"
    return ConsolidationResult(
        id=item.id,
        classification=item.classification,
        comparison=comparison,
        destination=destination,
        action=action,
        requires_validation=False,
        reason="Relevant knowledge is routed to evolutionary memory without automatic promotion to Fundacional.",
    )


def consolidate_item(item: KnowledgeItem) -> ConsolidationResult:
    comparison = compare_item(item)
    return route_item(item, comparison)
