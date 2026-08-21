"""Commercial handoff contract for the existing RemotePay payment API."""

from dataclasses import asdict
from typing import Any, Dict

from .models import Offer


class RemotePayHandoff:
    """Translate a validated C6 offer into RemotePay's PaymentCreate shape.

    This deliberately does not call the payment service. RemotePay currently
    exposes POST /payments and owns the transaction/PayFast execution path.
    Keeping this boundary pure makes the intelligence layer testable and keeps
    payment credentials and provider state out of discovery.
    """

    endpoint = "/payments"

    @classmethod
    def build_payment_request(
        cls,
        offer: Offer,
        customer_id: str,
        return_url: str,
        cancel_url: str,
    ) -> Dict[str, Any]:
        if not customer_id:
            raise ValueError("customer_id is required")
        if not return_url or not cancel_url:
            raise ValueError("return_url and cancel_url are required")
        if offer.price_minor <= 0:
            raise ValueError("offer price must be positive")

        return {
            "amount": offer.price_minor,
            "currency": offer.currency,
            "customer_id": customer_id,
            "return_url": return_url,
            "cancel_url": cancel_url,
            "item_name": offer.recommendation,
            "item_description": "; ".join(offer.deliverables),
        }

    @classmethod
    def build_checkout_reference(cls, transaction_id: str) -> str:
        if not transaction_id:
            raise ValueError("transaction_id is required")
        return f"remotepay:{transaction_id}"
