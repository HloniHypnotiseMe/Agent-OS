"""Canonical data contracts for Discovery Intelligence v1."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

EvidenceType = Literal["source", "observation", "inference_support"]
VerificationStatus = Literal["unverified", "corroborated", "verified"]


@dataclass(frozen=True)
class Evidence:
    field: str
    value: Any
    source_url: str
    source_title: str = ""
    observed_at: str = ""
    confidence: float = 0.0
    evidence_type: EvidenceType = "source"
    verification_status: VerificationStatus = "unverified"

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.source_url:
            raise ValueError("source_url is required for evidence")


@dataclass(frozen=True)
class Inference:
    field: str
    conclusion: Any
    supporting_evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class Offer:
    offer_id: str
    business_id: str
    recommendation: str
    deliverables: List[str]
    price_minor: int
    currency: str = "ZAR"
    billing_period: str = "once"
    payment_provider: str = "RemotePay"
    checkout_reference: Optional[str] = None


@dataclass
class BusinessIntelligenceRecord:
    business_id: str
    identity: Dict[str, Any]
    evidence: List[Evidence] = field(default_factory=list)
    inferences: List[Inference] = field(default_factory=list)
    opportunities: List[Dict[str, Any]] = field(default_factory=list)
    scores: Dict[str, int] = field(default_factory=dict)
    recommendations: List[Dict[str, Any]] = field(default_factory=list)
    recommended_offer: Optional[Offer] = None
    research_run_id: str = ""

    def validate_provenance(self) -> None:
        """Reject factual-looking fields that have no source evidence.

        Inferences are intentionally stored separately from source-backed facts.
        """
        factual_fields = {
            "name", "website", "industry", "location", "description"
        }
        covered = {item.field for item in self.evidence}
        missing = factual_fields.intersection(self.identity) - covered
        if missing:
            raise ValueError(
                "Missing provenance for factual fields: " + ", ".join(sorted(missing))
            )
