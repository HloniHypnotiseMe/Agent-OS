"""
Agent-OS Models: Model Abstraction Layer

Routes tasks to appropriate models (stub for real providers).
"""

from typing import Dict, Any

class ModelRouter:
    def __init__(self, config: Dict):
        self.config = config
        self.default = config.get("default_model", "claude-3-5-sonnet")

    def route(self, task_type: str, context: Dict = None) -> str:
        if "code" in task_type.lower():
            return "claude-3-5-sonnet"  # strong at coding
        if "research" in task_type.lower():
            return "claude-3-opus"  # deeper reasoning
        return self.default

    def get_available(self) -> list:
        return list(self.config.get("models", {}).keys()) or ["claude-3-5-sonnet", "gpt-4o", "local"]

# Example
router = ModelRouter({"default_model": "claude-3-5-sonnet"})