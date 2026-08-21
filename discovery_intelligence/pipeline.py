"""Evidence-first business discovery and commercial recommendation pipeline."""

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Callable, Dict, List
from urllib.parse import urlparse

from .models import BusinessIntelligenceRecord, Evidence, Inference, Offer


class DiscoveryIntelligencePipeline:
    """Compose existing Agent-OS web research with C6 commercial logic.

    The web-search callable is injected so the pipeline can use the existing
    Agent-OS tool in production and deterministic fixtures in tests.
    """

    def __init__(self, web_search: Callable[..., List[Dict[str, Any]]]):
        self.web_search = web_search

    @staticmethod
    def _business_id(url: str) -> str:
        host = urlparse(url).netloc.lower().removeprefix("www.")
        return "biz_" + sha256(host.encode("utf-8")).hexdigest()[:12]

    @staticmethod
    def _run_id(url: str) -> str:
        seed = f"{url}|{datetime.now(timezone.utc).date().isoformat()}"
        return "research_" + sha256(seed.encode("utf-8")).hexdigest()[:12]

    @staticmethod
    def _validate_depth(depth: str) -> None:
        if depth not in {"standard", "deep"}:
            raise ValueError("depth must be 'standard' or 'deep'")

    def research(self, url: str, depth: str = "standard") -> BusinessIntelligenceRecord:
        if not url.startswith(("http://", "https://")):
            raise ValueError("business URL must use http:// or https://")
        self._validate_depth(depth)

        business_id = self._business_id(url)
        run_id = self._run_id(url)
        host = urlparse(url).netloc.lower().removeprefix("www.")
        num_results = 12 if depth == "deep" else 8
        results = self.web_search(f'"{host}" business', num_results=num_results)
        if not results:
            raise ValueError("research returned no evidence")

        now = datetime.now(timezone.utc).isoformat()
        evidence: List[Evidence] = [
            Evidence(
                field="website",
                value=url,
                source_url=url,
                source_title=host,
                observed_at=now,
                confidence=0.99,
                verification_status="verified",
            )
        ]

        inferred_name = ""
        inference_sources: List[str] = []
        for result in results:
            source_url = result.get("url", "")
            if not source_url:
                continue
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            evidence.append(
                Evidence(
                    field="research_signal",
                    value={"title": title, "snippet": snippet},
                    source_url=source_url,
                    source_title=title,
                    observed_at=now,
                    confidence=0.70,
                    verification_status="corroborated",
                )
            )
            if not inferred_name and title:
                inferred_name = title
            inference_sources.append(source_url)

        identity = {"website": url, "domain": host}
        inferences = []
        if inferred_name:
            inferences.append(
                Inference(
                    field="business_identity",
                    conclusion=inferred_name,
                    supporting_evidence=inference_sources[:5],
                    confidence=0.60,
                )
            )

        return BusinessIntelligenceRecord(
            business_id=business_id,
            identity=identity,
            evidence=evidence,
            inferences=inferences,
            research_run_id=run_id,
        )

    @staticmethod
    def score(record: BusinessIntelligenceRecord) -> BusinessIntelligenceRecord:
        signals = " ".join(str(item.value).lower() for item in record.evidence)
        score = 50
        for keyword, weight in {
            "restaurant": 10,
            "ecommerce": 10,
            "online": 6,
            "booking": 6,
            "order": 5,
            "multiple": 4,
            "automation": 8,
        }.items():
            if keyword in signals:
                score += weight
        record.scores["commercial_opportunity"] = min(score, 100)
        return record

    @staticmethod
    def recommend(record: BusinessIntelligenceRecord) -> BusinessIntelligenceRecord:
        score = record.scores.get("commercial_opportunity", 0)
        recommendation = "C6 Business Intelligence Audit"
        deliverables = [
            "Evidence-backed business profile",
            "Opportunity assessment",
            "Prioritized C6 action plan",
        ]
        if score >= 70:
            recommendation = "C6 Growth + Automation"
            deliverables.extend([
                "Automation opportunity map",
                "Commercial conversion recommendations",
            ])

        record.opportunities.append({
            "type": "commercial",
            "score": score,
            "priority": "high" if score >= 70 else "medium",
        })
        record.recommendations.append({
            "product": recommendation,
            "reason": "Derived from observed research signals",
        })
        record.recommended_offer = Offer(
            offer_id="offer_" + record.business_id,
            business_id=record.business_id,
            recommendation=recommendation,
            deliverables=deliverables,
            price_minor=0,
            pricing_status="unvalidated",
        )
        return record

    def run(self, url: str, depth: str = "standard") -> BusinessIntelligenceRecord:
        record = self.research(url, depth=depth)
        self.score(record)
        self.recommend(record)
        return record
