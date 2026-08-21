"""C6 Discovery Intelligence v1.

A small, evidence-first commercial intelligence layer built on existing
Agent-OS research/web tooling and designed to consume C6Group.AiOS outputs.
"""

from .models import BusinessIntelligenceRecord, Evidence, Inference, Offer
from .pipeline import DiscoveryIntelligencePipeline

__all__ = [
    "BusinessIntelligenceRecord",
    "DiscoveryIntelligencePipeline",
    "Evidence",
    "Inference",
    "Offer",
]
