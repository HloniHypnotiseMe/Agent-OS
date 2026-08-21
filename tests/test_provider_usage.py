from commercial.provider_usage import ProviderUsageEvent, ProviderUsageSink


def test_provider_usage_preserves_unknown_cost(tmp_path):
    sink = ProviderUsageSink(tmp_path / "usage.jsonl")
    event = ProviderUsageEvent.now(
        provider="ollama",
        capability="llm_generation",
        external_event_id="ollama:test-1",
        source_ref="http://localhost:11434/api/generate",
        units=42,
    )

    sink.append(event)
    row = (tmp_path / "usage.jsonl").read_text(encoding="utf-8").strip()

    assert '"provider": "ollama"' in row
    assert '"units": 42' in row
    assert '"cost_zar": null' in row


def test_provider_usage_rejects_negative_cost():
    try:
        ProviderUsageEvent.now(
            provider="test",
            capability="test",
            external_event_id="1",
            source_ref="test",
            cost_zar=-0.01,
        )
    except ValueError as exc:
        assert "cost_zar cannot be negative" in str(exc)
    else:
        raise AssertionError("negative cost must be rejected")
