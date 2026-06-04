"""
Agent-OS Core: Task Router

Routes incoming tasks/instructions to the appropriate agent or layer.
Simple keyword + rule-based for now (can be upgraded with LLM).
"""

from typing import Dict, Any, Optional

class TaskRouter:
    def __init__(self, agents_registry: Dict[str, str]):
        """
        agents_registry: mapping of keywords/skills to agent names
        e.g. {"research": "researcher", "code": "coder", "strategy": "ceo"}
        """
        self.agents = agents_registry or {
            "research": "researcher",
            "market": "researcher",
            "analysis": "researcher",
            "code": "coder",
            "develop": "coder",
            "build": "coder",
            "strategy": "ceo",
            "plan": "ceo",
            "launch": "ceo",
            "business": "ceo",
            "design": "designer",
            "marketing": "marketer",
            "sales": "sales",
            "finance": "finance",
            "legal": "legal",
            "automation": "automation",
        }

    def route(self, task_description: str, context: Dict = None) -> str:
        """Return the best agent name for the task."""
        task_lower = task_description.lower()

        # Priority rules
        if any(kw in task_lower for kw in ["research", "investigate", "find", "market size", "competitor"]):
            return self.agents.get("research", "researcher")
        if any(kw in task_lower for kw in ["code", "implement", "develop", "script", "program"]):
            return self.agents.get("code", "coder")
        if any(kw in task_lower for kw in ["strategy", "plan", "roadmap", "launch", "business"]):
            return self.agents.get("strategy", "ceo")
        if any(kw in task_lower for kw in ["design", "ui", "visual", "logo"]):
            return self.agents.get("design", "designer")
        if any(kw in task_lower for kw in ["market", "campaign", "promote"]):
            return self.agents.get("marketing", "marketer")

        # Fallback to CEO for high-level or unknown
        return self.agents.get("strategy", "ceo")

    def get_available_agents(self) -> list:
        return list(set(self.agents.values()))

# Simple default instance creator
def get_default_router(agents: Dict = None) -> TaskRouter:
    return TaskRouter(agents)