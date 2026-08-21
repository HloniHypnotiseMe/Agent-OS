"""Standard usage hooks for commercial enrichment and outreach operations.

These hooks deliberately record usage even when provider cost is unknown. They
provide the missing instrumentation boundary without inventing provider prices.
Callers should invoke the hook immediately after a real provider operation.
"""

from __future__ import annotations

from commercial.provider_usage import ProviderUsageEvent, ProviderUsageSink


def record_enrichment(
    *,
    provider: str,
    external_event_id: str,
    source_ref: str,
    customer_id: str = "",
    package_id: str = "",
    units: float | None = None,
    cost_zar: float | None = None,
    notes: str = "",
    sink: ProviderUsageSink | None = None,
) -> ProviderUsageEvent:
    """Record one completed enrichment operation."""
    event = ProviderUsageEvent.now(
        provider=provider,
        capability="enrichment",
        external_event_id=external_event_id,
        source_ref=source_ref,
        customer_id=customer_id,
        package_id=package_id,
        units=units,
        cost_zar=cost_zar,
        notes=notes,
    )
    (sink or ProviderUsageSink()).append(event)
    return event


def record_outreach(
    *,
    provider: str,
    external_event_id: str,
    source_ref: str,
    customer_id: str = "",
    package_id: str = "",
    units: float | None = None,
    cost_zar: float | None = None,
    notes: str = "",
    sink: ProviderUsageSink | None = None,
) -> ProviderUsageEvent:
    """Record one completed outbound email/outreach operation."""
    event = ProviderUsageEvent.now(
        provider=provider,
        capability="email_outreach",
        external_event_id=external_event_id,
        source_ref=source_ref,
        customer_id=customer_id,
        package_id=package_id,
        units=units,
        cost_zar=cost_zar,
        notes=notes,
    )
    (sink or ProviderUsageSink()).append(event)
    return event
