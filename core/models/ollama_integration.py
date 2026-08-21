"""
Agent-OS: Ollama Local LLM Integration

Support for running local models via Ollama (tinyllama, phi, etc.).
Inspired by real-world C6Group.AiOS deployment.

Usage telemetry is emitted for every completed request. Local Ollama has no
per-request provider charge in this integration, so cost_zar remains unknown;
hosting/runtime cost must be supplied separately from actual infrastructure data.
"""

import requests
from typing import Dict, Any, Optional
import time

from commercial.provider_usage import ProviderUsageEvent, ProviderUsageSink


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", usage_sink: Optional[ProviderUsageSink] = None):
        self.base_url = base_url
        self.usage_sink = usage_sink or ProviderUsageSink()

    def is_available(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return resp.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list:
        try:
            resp = requests.get(f"{self.base_url}/api/tags")
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        *,
        customer_id: str = "",
        package_id: str = "",
    ) -> str:
        """Generate text and emit provider usage telemetry."""
        payload = {"model": model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system

        started = time.monotonic()
        event_id = f"ollama:{model}:{time.time_ns()}"
        try:
            resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
            data = resp.json()
            response = data.get("response", "[Ollama error: no response]")
            self.usage_sink.append(
                ProviderUsageEvent.now(
                    provider="ollama",
                    capability="llm_generation",
                    external_event_id=event_id,
                    source_ref=f"{self.base_url}/api/generate",
                    customer_id=customer_id,
                    package_id=package_id,
                    units=data.get("eval_count"),
                    notes=f"model={model};elapsed_seconds={time.monotonic() - started:.3f};cost_zar=UNKNOWN",
                )
            )
            return response
        except Exception as e:
            self.usage_sink.append(
                ProviderUsageEvent.now(
                    provider="ollama",
                    capability="llm_generation",
                    external_event_id=event_id,
                    source_ref=f"{self.base_url}/api/generate",
                    customer_id=customer_id,
                    package_id=package_id,
                    notes=f"model={model};failed;error={type(e).__name__}",
                )
            )
            return f"[Ollama error: {str(e)}]"


ollama = OllamaClient()


def get_local_model_response(
    prompt: str,
    model: str = "tinyllama",
    system: Optional[str] = None,
    customer_id: str = "",
    package_id: str = "",
) -> str:
    """Convenience function for agents."""
    if not ollama.is_available():
        return "[Local AI not available - falling back to simulation. Start Ollama and pull a model.]"
    return ollama.generate(
        model,
        prompt,
        system,
        customer_id=customer_id,
        package_id=package_id,
    )
