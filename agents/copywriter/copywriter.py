"""
Agent-OS: Copywriter Agent

Specialized in writing high-quality copy: emails, landing pages, social posts, ads, scripts.
"""

from typing import Dict, Any
import time

class CopywriterAgent:
    def __init__(self, memory, tools, model_config):
        self.memory = memory
        self.tools = tools
        self.model = model_config
        self.name = "copywriter"

    def write_copy(self, type: str, topic: str, tone: str = "professional", length: str = "medium") -> Dict[str, Any]:
        print(f"[{self.name}] Writing {type} copy on '{topic}' in {tone} tone")
        
        samples = {
            "email": f"Subject: Unlock the Power of Agent-OS\n\nDear {topic},\n\nIn a world of fragmented AI tools, Agent-OS stands out...",
            "landing": f"# {topic}\n\nThe only operating system built for teams of autonomous AI agents.\n\n[CTA: Start Free Trial]",
            "social": f"🚀 Just launched Agent-OS — your personal JARVIS that delegates to a full team of AI agents. No more prompt engineering hell. {topic}",
            "ad": f"Stop juggling 10 AI tools. Agent-OS gives you one JARVIS that runs your entire digital workforce. {topic}."
        }
        
        copy = samples.get(type.lower(), f"High-quality {tone} copy about {topic} for {type}.")
        
        result = {
            "type": type,
            "topic": topic,
            "tone": tone,
            "copy": copy,
            "word_count": len(copy.split()),
            "timestamp": time.time()
        }
        self.memory.store(f"copy_{int(time.time())}", f"{type} for {topic}", result)
        return result

# Example
if __name__ == "__main__":
    cw = CopywriterAgent(memory=type('m', (object,), {'store': lambda *a: None})(), tools={}, model_config={})
    print(cw.write_copy("email", "AI founders", "exciting")["copy"][:100])