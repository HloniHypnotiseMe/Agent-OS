from commercial.provider_usage import ProviderUsageSink
from commercial.usage_hooks import record_enrichment, record_outreach


def test_enrichment_hook_records_capability_and_unknown_cost(tmp_path):
    sink = ProviderUsageSink(tmp_path / "usage.jsonl")
    event = record_enrichment(
        provider="example-enrichment",
        external_event_id="enr-1",
        source_ref="test:enrichment",
        package_id="business_audit",
        units=12,
        sink=sink,
    )

    assert event.capability == "enrichment"
    assert event.cost_zar is None
    assert event.units == 12
    assert (tmp_path / "usage.jsonl").read_text(encoding="utf-8").count("enr-1") == 1


def test_outreach_hook_records_capability_and_known_cost(tmp_path):
    sink = ProviderUsageSink(tmp_path / "usage.jsonl")
    event = record_outreach(
        provider="example-mail",
        external_event_id="mail-1",
        source_ref="test:outreach",
        package_id="lead_generation",
        units=1,
        cost_zar=0.42,
        sink=sink,
    )

    assert event.capability == "email_outreach"
    assert event.cost_zar == 0.42
    assert event.units == 1
    assert (tmp_path / "usage.jsonl").read_text(encoding="utf-8").count("mail-1") == 1
