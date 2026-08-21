import json

from agents.researcher.researcher import ResearcherAgent
from agents.sales.sales import SalesAgent
from commercial.provider_usage import ProviderUsageSink


class Memory:
    def retrieve(self, query, k=3):
        return []

    def store(self, *args):
        return None


class ResearchTools:
    def use_tool(self, name, **kwargs):
        assert name == "web_search"
        return [{"source": "https://example.com/business", "content": "business research"}]


class OutreachTools:
    def use_tool(self, name, **kwargs):
        assert name == "send_email"
        return {"provider": "test-mail", "message_id": "msg-123"}


def read_events(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_research_records_enrichment_usage(tmp_path):
    sink = ProviderUsageSink(tmp_path / "usage.jsonl")
    agent = ResearcherAgent(Memory(), ResearchTools(), {}, usage_sink=sink)

    result = agent.perform_research("test business")

    assert result["query"] == "test business"
    events = read_events(tmp_path / "usage.jsonl")
    assert len(events) == 1
    assert events[0]["capability"] == "enrichment"
    assert events[0]["provider"] == "web_search"
    assert events[0]["source_ref"] == "https://example.com/business"
    assert events[0]["cost_zar"] is None
    assert events[0]["units"] == 1


def test_successful_outreach_records_usage(tmp_path):
    sink = ProviderUsageSink(tmp_path / "usage.jsonl")
    agent = SalesAgent(Memory(), OutreachTools(), {}, usage_sink=sink)

    result = agent.send_outreach("owner@example.com", "C6", "Hello")

    assert result["message_id"] == "msg-123"
    events = read_events(tmp_path / "usage.jsonl")
    assert len(events) == 1
    assert events[0]["capability"] == "email_outreach"
    assert events[0]["provider"] == "test-mail"
    assert events[0]["external_event_id"] == "msg-123"
    assert events[0]["cost_zar"] is None
    assert events[0]["units"] == 1
