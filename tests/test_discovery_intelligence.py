from discovery_intelligence.payment_handoff import RemotePayHandoff
from discovery_intelligence.pipeline import DiscoveryIntelligencePipeline


def fake_web_search(query, num_results=5):
    assert "example.co.za" in query
    return [
        {
            "title": "Example Restaurant",
            "url": "https://example.co.za/",
            "snippet": "Restaurant with online ordering and booking.",
            "source": "fixture",
        },
        {
            "title": "Example Business Profile",
            "url": "https://directory.example/test",
            "snippet": "Multiple locations and online ordering.",
            "source": "fixture",
        },
    ][:num_results]


def test_pipeline_separates_evidence_from_inference_and_builds_offer():
    pipeline = DiscoveryIntelligencePipeline(fake_web_search)
    record = pipeline.run("https://example.co.za")

    assert record.business_id.startswith("biz_")
    assert record.identity["website"] == "https://example.co.za"
    assert any(item.field == "website" for item in record.evidence)
    assert record.inferences[0].field == "business_identity"
    assert record.scores["commercial_opportunity"] >= 70
    assert record.recommended_offer is not None
    assert record.recommended_offer.currency == "ZAR"


def test_provenance_validation_passes_for_pipeline_output():
    record = DiscoveryIntelligencePipeline(fake_web_search).run(
        "https://example.co.za"
    )
    record.validate_provenance()


def test_remotepay_handoff_matches_payment_api_contract():
    offer = DiscoveryIntelligencePipeline(fake_web_search).run(
        "https://example.co.za"
    ).recommended_offer

    request = RemotePayHandoff.build_payment_request(
        offer,
        customer_id="cust_001",
        return_url="https://c6group.co.za/payment/success",
        cancel_url="https://c6group.co.za/payment/cancel",
    )

    assert request["amount"] == offer.price_minor
    assert request["currency"] == "ZAR"
    assert request["customer_id"] == "cust_001"
    assert request["item_name"] == offer.recommendation
    assert RemotePayHandoff.build_checkout_reference("txn_abc") == "remotepay:txn_abc"
