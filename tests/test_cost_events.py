from datetime import date

import pytest

from commercial.cost_events import CostEvent, CostEventRecorder
from commercial.cost_ledger import CostLedger


def event(field: str, value: float | None, source: str = "provider://event/1") -> CostEvent:
    return CostEvent(
        customer_id="cust-1",
        package_id="pkg-1",
        event_date=date(2026, 8, 21),
        cost_field=field,
        cost_zar=value,
        source_ref=source,
        provider="test-provider",
    )


def test_normalize_requires_provider_and_source():
    recorder = CostEventRecorder(CostLedger("/tmp/c6-cost-events.jsonl"))
    assert recorder.normalize(event("llm_cost_zar", 10))["cost_zar"] == 10


def test_unknown_cost_remains_unknown():
    observation = CostEventRecorder.aggregate_events(
        [event("llm_cost_zar", 10)],
        observation_id="obs-1",
        period_start=date(2026, 8, 21),
        period_end=date(2026, 8, 21),
        revenue_zar=1000,
    )
    assert observation.total_direct_cost_zar is None
    assert "research_cost_zar" in observation.missing_cost_fields


def test_events_accumulate_same_cost_category():
    observation = CostEventRecorder.aggregate_events(
        [event("llm_cost_zar", 10, "provider://1"), event("llm_cost_zar", 15, "provider://2")],
        observation_id="obs-2",
        period_start=date(2026, 8, 21),
        period_end=date(2026, 8, 21),
        revenue_zar=1000,
    )
    assert observation.llm_cost_zar == 25
    assert observation.source_refs == ("provider://1", "provider://2")


def test_cross_customer_events_are_rejected():
    first = event("llm_cost_zar", 10)
    second = CostEvent(
        customer_id="cust-2",
        package_id="pkg-1",
        event_date=first.event_date,
        cost_field="research_cost_zar",
        cost_zar=5,
        source_ref="provider://2",
        provider="test-provider",
    )
    with pytest.raises(ValueError, match="exactly one customer"):
        CostEventRecorder.aggregate_events(
            [first, second],
            observation_id="obs-3",
            period_start=date(2026, 8, 21),
            period_end=date(2026, 8, 21),
            revenue_zar=1000,
        )
