"""
Agent-OS Observability: Logger & Metrics

Central logging, tracing, and basic metrics.
"""

import time
from typing import Dict, Any, List

class Logger:
    def __init__(self):
        self.logs: List[Dict] = []
        self.metrics: Dict[str, int] = {"delegations": 0, "errors": 0, "tasks_completed": 0}

    def log(self, level: str, component: str, message: str, metadata: Dict = None):
        entry = {
            "timestamp": time.time(),
            "level": level,
            "component": component,
            "message": message,
            "metadata": metadata or {}
        }
        self.logs.append(entry)
        print(f"[{level}] {component}: {message}")
        if level == "ERROR":
            self.metrics["errors"] += 1

    def record_delegation(self, from_agent: str, to_agent: str):
        self.metrics["delegations"] += 1
        self.log("INFO", "protocol", f"Delegated from {from_agent} to {to_agent}")

    def get_metrics(self) -> Dict:
        return self.metrics.copy()

    def get_recent_logs(self, n: int = 20) -> List[Dict]:
        return self.logs[-n:]

# Global instance
system_logger = Logger()