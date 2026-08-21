"""Cost observation instrumentation for C6 commercial delivery economics.

The ledger deliberately separates *unknown* from zero. A missing cost component is
represented by ``None`` and prevents a margin calculation until resolved. This
keeps package economics auditable and prevents silent under-reporting of delivery
cost.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
import json
from pathlib import Path
from statistics import quantiles
from typing import Iterable, Optional
from uuid import uuid4


COST_FIELDS = (
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
)


@dataclass(frozen=True)
class CostObservation:
    observation_id: str
    customer_id: str
    package_id: str
    period_start: date
    period_end: date
    revenue_zar: float
    llm_cost_zar: Optional[float] = None
    research_cost_zar: Optional[float] = None
    enrichment_cost_zar: Optional[float] = None
    email_cost_zar: Optional[float] = None
    hosting_cost_zar: Optional[float] = None
    payment_cost_zar: Optional[float] = None
    human_delivery_cost_zar: Optional[float] = None
    implementation_cost_zar: Optional[float] = None
    third_party_cost_zar: Optional[float] = None
    unknown_cost_zar: Optional[float] = None
    confidence: str = "UNKNOWN"
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.customer_id or not self.package_id:
            raise ValueError("customer_id and package_id are required")
        if self.period_end < self.period_start:
            raise ValueError("period_end cannot precede period_start")
        if self.revenue_zar < 0:
            raise ValueError("revenue_zar cannot be negative")
        for field_name in COST_FIELDS:
            value = getattr(self, field_name)
            if value is not None and value < 0:
                raise ValueError(f"{field_name} cannot be negative")

    @property
    def missing_cost_fields(self) -> tuple[str, ...]:
        return tuple(name for name in COST_FIELDS if getattr(self, name) is None)

    @property
    def total_direct_cost_zar(self) -> Optional[float]:
        if self.missing_cost_fields:
            return None
        return round(sum(getattr(self, name) for name in COST_FIELDS), 2)

    @property
    def gross_margin_zar(self) -> Optional[float]:
        total = self.total_direct_cost_zar
        return None if total is None else round(self.revenue_zar - total, 2)

    @property
    def gross_margin_pct(self) -> Optional[float]:
        if self.revenue_zar == 0 or self.gross_margin_zar is None:
            return None
        return round((self.gross_margin_zar / self.revenue_zar) * 100, 2)

    def to_record(self) -> dict:
        record = asdict(self)
        record["period_start"] = self.period_start.isoformat()
        record["period_end"] = self.period_end.isoformat()
        record["source_refs"] = list(self.source_refs)
        record["total_direct_cost_zar"] = self.total_direct_cost_zar
        record["gross_margin_zar"] = self.gross_margin_zar
        record["gross_margin_pct"] = self.gross_margin_pct
        record["missing_cost_fields"] = list(self.missing_cost_fields)
        return record

    def require_complete_costs(self) -> None:
        missing = self.missing_cost_fields
        if missing:
            raise ValueError(
                "Cannot calculate validated economics; missing cost fields: "
                + ", ".join(missing)
            )


class CostLedger:
    """Append-only JSONL store for customer/pilot cost observations."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, observation: CostObservation) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(observation.to_record(), sort_keys=True) + "\n")

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def observations(self, package_id: Optional[str] = None) -> list[dict]:
        rows = self.read()
        if package_id is None:
            return rows
        return [row for row in rows if row["package_id"] == package_id]

    def package_cost_percentiles(self, package_id: str) -> dict[str, Optional[float]]:
        costs = [
            row["total_direct_cost_zar"]
            for row in self.observations(package_id)
            if row.get("total_direct_cost_zar") is not None
        ]
        if not costs:
            return {"p50_cost_zar": None, "p90_cost_zar": None, "observations": 0}
        if len(costs) == 1:
            return {
                "p50_cost_zar": round(costs[0], 2),
                "p90_cost_zar": round(costs[0], 2),
                "observations": 1,
            }
        points = quantiles(costs, n=100, method="inclusive")
        return {
            "p50_cost_zar": round(points[49], 2),
            "p90_cost_zar": round(points[89], 2),
            "observations": len(costs),
        }


def new_observation(customer_id: str, package_id: str, period_start: date, period_end: date, revenue_zar: float, **costs) -> CostObservation:
    """Create a uniquely identified observation while preserving unknown costs."""
    unknown = {key: value for key, value in costs.items() if key not in COST_FIELDS}
    if unknown:
        raise ValueError(f"Unknown cost fields: {', '.join(sorted(unknown))}")
    return CostObservation(
        observation_id=str(uuid4()),
        customer_id=customer_id,
        package_id=package_id,
        period_start=period_start,
        period_end=period_end,
        revenue_zar=revenue_zar,
        **costs,
    )


def margin_gate(revenue_zar: float, total_direct_cost_zar: float, minimum_margin_pct: float) -> bool:
    if revenue_zar <= 0:
        raise ValueError("revenue_zar must be greater than zero")
    margin_pct = ((revenue_zar - total_direct_cost_zar) / revenue_zar) * 100
    return margin_pct >= minimum_margin_pct
