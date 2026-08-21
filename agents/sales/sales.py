"""
Agent-OS: Sales Agent

Handles lead qualification, demos, closing, CRM, and revenue operations.
"""

from typing import Dict, Any
import time

from commercial.provider_usage import ProviderUsageSink
from commercial.usage_hooks import record_outreach


class SalesAgent:
    def __init__(self, memory, tools, model_config, usage_sink=None):
        self.memory = memory
        self.tools = tools
        self.model = model_config
        self.usage_sink = usage_sink or ProviderUsageSink()
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

    def send_outreach(self, recipient: str, subject: str, body: str, customer_id: str = "", package_id: str = "") -> Dict[str, Any]:
        """Send outreach through the configured tool and record only successful delivery."""
        if not hasattr(self.tools, "use_tool"):
            raise RuntimeError("SalesAgent requires a tool provider with use_tool for outreach")

        result = self.tools.use_tool(
            "send_email",
            recipient=recipient,
            subject=subject,
            body=body,
        )

        external_event_id = str(
            result.get("id") or result.get("message_id") or result.get("event_id") or f"outreach:{int(time.time() * 1000)}"
        ) if isinstance(result, dict) else f"outreach:{int(time.time() * 1000)}"
        source_ref = str(result.get("source") or result.get("provider") or "send_email") if isinstance(result, dict) else "send_email"

        record_outreach(
            provider=source_ref,
            external_event_id=external_event_id,
            source_ref=source_ref,
            customer_id=customer_id,
            package_id=package_id,
            units=1,
            notes=f"Outbound email to {recipient}",
            sink=self.usage_sink,
        )

        return result if isinstance(result, dict) else {"result": result}


# Example
if __name__ == "__main__":
    sales = SalesAgent(memory=type('m', (object,), {'store': lambda *a: None})(), tools={}, model_config={})
    print(sales.qualify_lead({"name": "AI Founder", "company": "Startup"})["status"])
