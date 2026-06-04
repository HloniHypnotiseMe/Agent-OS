"""
Agent-OS: Ollama Local LLM Integration

Support for running local models via Ollama (tinyllama, phi, etc.).
Inspired by real-world C6Group.AiOS deployment (https://github.com/HloniHypnotiseMe/C6Group.AiOS).

Usage:
- Install Ollama: https://ollama.com
- Pull a model: ollama pull tinyllama
- Then use in agents via this module.

This keeps Agent-OS runnable offline with local AI.
"""

import requests
from typing import Dict, Any, Optional

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def is_available(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return resp.status_code == 200
        except:
            return False

    def list_models(self) -> list:
        try:
            resp = requests.get(f"{self.base_url}/api/tags")
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
        except:
            return []

    def generate(self, model: str, prompt: str, system: Optional[str] = None) -> str:
        """Simple generate call."""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system

        try:
            resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
            data = resp.json()
            return data.get("response", "[Ollama error: no response]")
        except Exception as e:
            return f"[Ollama error: {str(e)}]"

# Global client
ollama = OllamaClient()

def get_local_model_response(prompt: str, model: str = "tinyllama", system: Optional[str] = None) -> str:
    """Convenience function for agents."""
    if not ollama.is_available():
        return "[Local AI not available - falling back to simulation. Start Ollama and pull a model.]"
    return ollama.generate(model, prompt, system)