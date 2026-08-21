"""Provider usage telemetry for commercial cost attribution.

Usage is recorded even when the monetary cost is unknown. Monetary cost is never
invented: callers may provide an observed cost in ZAR when the provider exposes it.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class ProviderUsageEvent:
    provider: str
    capability: str
    external_event_id: str
    source_ref: str
    occurred_at: str
    customer_id: str = ""
    package_id: str = ""
    cost_zar: Optional[float] = None
    units: Optional[float] = None
    notes: str = ""

    @classmethod
    def now(
        cls,
        *,
        provider: str,
        capability: str,
        external_event_id: str,
        source_ref: str,
        customer_id: str = "",
        package_id: str = "",
        cost_zar: Optional[float] = None,
        units: Optional[float] = None,
        notes: str = "",
    ) -> "ProviderUsageEvent":
        if cost_zar is not None and cost_zar < 0:
            raise ValueError("cost_zar cannot be negative")
        if not provider or not capability or not source_ref:
            raise ValueError("provider, capability and source_ref are required")
        return cls(
            provider=provider,
            capability=capability,
            external_event_id=external_event_id,
            source_ref=source_ref,
            occurred_at=datetime.now(timezone.utc).isoformat(),
            customer_id=customer_id,
            package_id=package_id,
            cost_zar=cost_zar,
            units=units,
            notes=notes,
        )


class ProviderUsageSink:
    """Append-only JSONL telemetry sink."""

    def __init__(self, path: str | Path = "data/commercial/provider_usage.jsonl"):
        self.path = Path(path)

    def append(self, event: ProviderUsageEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event), sort_keys=True) + "\n")
