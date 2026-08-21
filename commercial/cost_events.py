"""Provider/runtime cost-event normalization for the commercial cost ledger.

This module is intentionally provider-agnostic. Integration code can emit one
normalized event per billable delivery event without coupling providers to the
commercial ledger implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from commercial.cost_ledger import CostLedger, CostObservation


@dataclass(frozen=True)
class CostEvent:
    """One attributable delivery-cost event."""

    customer_id: str
    package_id: str
    event_date: date
    cost_field: str
    cost_zar: Optional[float]
    source_ref: str
    provider: str
    external_event_id: str = ""
    confidence: str = "OBSERVED"
    notes: str = ""


class CostEventRecorder:
    """Accumulate normalized cost events into complete package observations."""

    def __init__(self, ledger: CostLedger):
        self.ledger = ledger

    def validate_event(self, event: CostEvent) -> None:
        allowed = {
            "llm_cost_zar",
            "research_cost_zar",
            "enrichment_cost_zar",
            "email_cost_zar",
            "hosting_cost_zar",
            "payment_cost_zar",
            "human_delivery_cost_zar",
            "implementation_cost_zar",
            "third_party_cost_zar",
            "unknown_cost_zar",
        }
        if event.cost_field not in allowed:
            raise ValueError(f"Unsupported cost field: {event.cost_field}")
        if event.cost_zar is not None and event.cost_zar < 0:
            raise ValueError("cost_zar cannot be negative")
        if not event.source_ref:
            raise ValueError("source_ref is required for cost attribution")
        if not event.provider:
            raise ValueError("provider is required for cost attribution")

    def normalize(self, event: CostEvent) -> dict:
        self.validate_event(event)
        return {
            "customer_id": event.customer_id,
            "package_id": event.package_id,
            "event_date": event.event_date.isoformat(),
            "cost_field": event.cost_field,
            "cost_zar": event.cost_zar,
            "source_ref": event.source_ref,
            "provider": event.provider,
            "external_event_id": event.external_event_id,
            "confidence": event.confidence,
            "notes": event.notes,
        }

    @staticmethod
    def aggregate_events(
        events: list[CostEvent],
        *,
        observation_id: str,
        period_start: date,
        period_end: date,
        revenue_zar: float,
    ) -> CostObservation:
        if not events:
            raise ValueError("At least one cost event is required")

        customer_ids = {event.customer_id for event in events}
        package_ids = {event.package_id for event in events}
        if len(customer_ids) != 1 or len(package_ids) != 1:
            raise ValueError("Events must belong to exactly one customer and package")

        fields = {
            "llm_cost_zar": None,
            "research_cost_zar": None,
            "enrichment_cost_zar": None,
            "email_cost_zar": None,
            "hosting_cost_zar": None,
            "payment_cost_zar": None,
            "human_delivery_cost_zar": None,
            "implementation_cost_zar": None,
            "third_party_cost_zar": None,
            "unknown_cost_zar": None,
        }
        source_refs: list[str] = []

        for event in events:
            value = event.cost_zar
            if value is not None:
                fields[event.cost_field] = round(
                    (fields[event.cost_field] or 0) + value, 2
                )
            source_refs.append(event.source_ref)

        confidence = "OBSERVED" if all(event.confidence == "OBSERVED" for event in events) else "MIXED"
        return CostObservation(
            observation_id=observation_id,
            customer_id=next(iter(customer_ids)),
            package_id=next(iter(package_ids)),
            period_start=period_start,
            period_end=period_end,
            revenue_zar=revenue_zar,
            confidence=confidence,
            source_refs=tuple(dict.fromkeys(source_refs)),
            **fields,
        )

    def record_observation(self, observation: CostObservation) -> None:
        observation.require_complete_costs()
        self.ledger.append(observation)
