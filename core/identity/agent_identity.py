"""
Agent-OS Core: Agent Identity

Manages persistent identity, roles, and permissions for agents.
"""

from typing import Dict, Any

class AgentIdentity:
    def __init__(self, name: str, role: str, capabilities: list):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.created = __import__('time').time()
        self.version = "1.0"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "capabilities": self.capabilities,
            "version": self.version
        }

# Pre-defined identities (expand as agents are added)
IDENTITIES = {
    "jarvis": AgentIdentity("jarvis", "Owner Personal Assistant", ["conversation", "delegation", "reporting"]),
    "ceo": AgentIdentity("ceo", "Strategic Leader", ["strategy", "delegation", "decision"]),
    "researcher": AgentIdentity("researcher", "Research Specialist", ["research", "analysis", "synthesis"]),
}