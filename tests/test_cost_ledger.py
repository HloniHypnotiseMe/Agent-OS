from datetime import date

import pytest

from commercial.cost_ledger import CostLedger, margin_gate, new_observation


COMPLETE = {
    "llm_cost_zar": 100.0,
    "research_cost_zar": 50.0,
    "enrichment_cost_zar": 25.0,
    "email_cost_zar": 10.0,
    "hosting_cost_zar": 40.0,
    "payment_cost_zar": 15.0,
    "human_delivery_cost_zar": 200.0,
    "implementation_cost_zar": 50.0,
    "third_party_cost_zar": 10.0,
    "unknown_cost_zar": 0.0,
}


def make_observation(**overrides):
    costs = {**COMPLETE, **overrides}
    return new_observation(
        "customer-001",
        "diamond",
        date(2026, 8, 1),
        date(2026, 8, 31),
        4995.0,
        **costs,
    )


def test_total_cost_and_margin_are_reproducible():
    observation = make_observation()
    assert observation.total_direct_cost_zar == 500.0
    assert observation.gross_margin_zar == 4495.0
    assert observation.gross_margin_pct == 89.99


def test_missing_cost_is_not_coerced_to_zero():
    observation = make_observation(research_cost_zar=None)
    assert "research_cost_zar" in observation.missing_cost_fields
    assert observation.total_direct_cost_zar is None
    assert observation.gross_margin_pct is None
    with pytest.raises(ValueError, match="research_cost_zar"):
        observation.require_complete_costs()


def test_ledger_persists_observations_and_calculates_percentiles(tmp_path):
    ledger = CostLedger(tmp_path / "cost_observations.jsonl")
    for cost in (100.0, 200.0, 300.0):
        ledger.append(make_observation(llm_cost_zar=cost))

    result = ledger.package_cost_percentiles("diamond")
    assert result["observations"] == 3
    assert result["p50_cost_zar"] == 600.0
    assert result["p90_cost_zar"] == 680.0


def test_margin_gate_is_deterministic():
    assert margin_gate(4995.0, 1000.0, 65.0) is True
    assert margin_gate(4995.0, 1800.0, 65.0) is False
