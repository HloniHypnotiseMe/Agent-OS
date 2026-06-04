"""
Agent-OS: Sales Agent

Handles lead qualification, demos, closing, CRM, and revenue operations.
"""

from typing import Dict, Any
import time

class SalesAgent:
    def __init__(self, memory, tools, model_config):
        self.memory = memory
        self.tools = tools
        self.model = model_config
        self.name = "sales"

    def qualify_lead(self, lead_info: Dict) -> Dict[str, Any]:
        print(f"[{self.name}] Qualifying lead: {lead_info.get('name', 'Unknown')}")
        
        score = 75
        if "founder" in str(lead_info).lower() or "ai" in str(lead_info).lower():
            score = 90
        
        result = {
            "lead": lead_info,
            "score": score,
            "status": "hot" if score > 80 else "warm",
            "next_step": "Schedule demo with JARVIS" if score > 70 else "Nurture with content",
            "timestamp": time.time()
        }
        self.memory.store(f"lead_{int(time.time())}", str(lead_info), result)
        return result

    def run_demo_script(self, prospect: str) -> str:
        return f"Demo script for {prospect}: 'Watch how JARVIS delegates your research task to the Researcher agent in seconds...'"

# Example
if __name__ == "__main__":
    sales = SalesAgent(memory=type('m', (object,), {'store': lambda *a: None})(), tools={}, model_config={})
    print(sales.qualify_lead({"name": "AI Founder", "company": "Startup"})["status"])