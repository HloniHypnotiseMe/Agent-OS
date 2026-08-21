import pytest

from discovery_intelligence.models import Offer
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


def test_pipeline_separates_evidence_from_inference_and_builds_unpriced_offer():
    record = DiscoveryIntelligencePipeline(fake_web_search).run("https://example.co.za")

    assert record.business_id.startswith("biz_")
    assert record.identity["website"] == "https://example.co.za"
    assert "name" not in record.identity
    assert any(item.field == "website" for item in record.evidence)
    assert record.inferences[0].field == "business_identity"
    assert record.scores["commercial_opportunity"] >= 70
    assert record.recommended_offer is not None
    assert record.recommended_offer.currency == "ZAR"
    assert record.recommended_offer.pricing_status == "unvalidated"
    assert record.recommended_offer.price_minor == 0


def test_provenance_validation_passes_for_pipeline_output():
    record = DiscoveryIntelligencePipeline(fake_web_search).run(
        "https://example.co.za"
    )
    record.validate_provenance()


def test_provenance_validation_rejects_unsourced_identity():
    record = DiscoveryIntelligencePipeline(fake_web_search).run(
        "https://example.co.za"
    )
    record.identity["industry"] = "restaurant"
    with pytest.raises(ValueError, match="Missing provenance"):
        record.validate_provenance()


def test_remotepay_handoff_rejects_unvalidated_offer():
    offer = DiscoveryIntelligencePipeline(fake_web_search).run(
        "https://example.co.za"
    ).recommended_offer

    with pytest.raises(ValueError, match="pricing must be validated"):
        RemotePayHandoff.build_payment_request(
            offer,
            customer_id="cust_001",
            return_url="https://c6group.co.za/payment/success",
            cancel_url="https://c6group.co.za/payment/cancel",
        )


def test_remotepay_handoff_matches_payment_api_contract_for_validated_offer():
    offer = Offer(
        offer_id="offer_test",
        business_id="biz_test",
        recommendation="C6 Business Intelligence Audit",
        deliverables=["Evidence-backed business profile"],
        price_minor=125000,
        currency="ZAR",
        pricing_status="validated",
    )

    request = RemotePayHandoff.build_payment_request(
        offer,
        customer_id="cust_001",
        return_url="https://c6group.co.za/payment/success",
        cancel_url="https://c6group.co.za/payment/cancel",
    )

    assert request["amount"] == 125000
    assert request["currency"] == "ZAR"
    assert request["customer_id"] == "cust_001"
    assert request["item_name"] == offer.recommendation
    assert RemotePayHandoff.build_checkout_reference("txn_abc") == "remotepay:txn_abc"
