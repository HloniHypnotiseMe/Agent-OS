"""
Agent-OS Protocol: Task Delegation

This module handles delegating tasks between specialized agents.
"""

from typing import Dict, Any, List, Optional
import uuid

class Task:
    def __init__(self, description: str, priority: int = 5, required_skills: List[str] = None, 
                 assigned_to: Optional[str] = None, context: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())
        self.description = description
        self.priority = priority
        self.required_skills = required_skills or []
        self.assigned_to = assigned_to
        self.context = context or {}
        self.status = "pending"

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "required_skills": self.required_skills,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "context": self.context
        }

class DelegationProtocol:
    def __init__(self, agents_registry: Dict[str, Any]):
        self.agents = agents_registry  # e.g. {"ceo": ceo_agent_instance, ...}

    def delegate_task(self, task: Task) -> Optional[str]:
        """
        Delegate a task to the most suitable agent based on skills and availability.
        """
        if not task.required_skills:
            # Default to CEO or general router
            best_agent = "ceo"
        else:
            # Simple matching logic (expand with real matching later)
            best_agent = None
            for skill in task.required_skills:
                if skill in ["research", "analysis"]:
                    best_agent = "researcher"
                elif skill in ["code", "programming", "development"]:
                    best_agent = "coder"
                elif skill in ["marketing", "promotion"]:
                    best_agent = "marketer"
                elif skill in ["design", "visual"]:
                    best_agent = "designer"
                # Add more mappings...
                if best_agent:
                    break
            
            if not best_agent:
                best_agent = "ceo"  # fallback

        task.assigned_to = best_agent
        task.status = "delegated"

        print(f"[Delegation] Task {task.id} delegated to {best_agent}: {task.description[:50]}...")
        return best_agent

    def get_agent(self, agent_name: str):
        return self.agents.get(agent_name)

# Example usage
if __name__ == "__main__":
    # Placeholder registry
    agents = {"ceo": "CEOAgent()", "researcher": "ResearcherAgent()"}
    protocol = DelegationProtocol(agents)
    task = Task("Research market for AI OS", priority=8, required_skills=["research"])
    agent = protocol.delegate_task(task)
    print(f"Assigned to: {agent}")