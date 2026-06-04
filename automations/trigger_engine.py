"""
Agent-OS Automations: Trigger Engine

Event-driven and scheduled automations.
"""

from typing import Dict, Any, Callable
import time

class TriggerEngine:
    def __init__(self):
        self.triggers: Dict[str, Dict] = {}
        self.running = False

    def register_trigger(self, name: str, trigger_type: str, condition: str, action: Callable):
        self.triggers[name] = {
            "type": trigger_type,
            "condition": condition,
            "action": action,
            "last_fired": None
        }
        print(f"[Automations] Registered trigger: {name}")

    def fire_trigger(self, name: str, context: Dict = None):
        if name in self.triggers:
            trig = self.triggers[name]
            trig["last_fired"] = time.time()
            print(f"[Automations] Firing {name}")
            return trig["action"](context or {})
        return None

# Example global
engine = TriggerEngine()