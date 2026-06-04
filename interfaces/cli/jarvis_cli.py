#!/usr/bin/env python3
"""
Agent-OS CLI Interface

Command-line JARVIS for the owner. Full access to real agents.

Usage:
    python interfaces/cli/jarvis_cli.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from memory.long_term_memory import LongTermMemory
from tools.tool_registry import get_default_registry
from agents.protocol.arbitration import ArbitrationProtocol
from agents.protocol.voting import VotingProtocol
from agents.protocol.priority import PriorityQueueProtocol
from agents.jarvis.jarvis import JarvisAgent
# Import all agents
from agents.ceo.ceo import CEOAgent
from agents.researcher.researcher import ResearcherAgent
from agents.cto.cto import CTOAgent
from agents.coder.coder import CoderAgent
from agents.marketer.marketer import MarketerAgent
from agents.designer.designer import DesignerAgent
from agents.copywriter.copywriter import CopywriterAgent
from agents.sales.sales import SalesAgent
from agents.automation.automation import AutomationAgent
from agents.finance.finance import FinanceAgent
from agents.legal.legal import LegalAgent
from agents.support.support import SupportAgent

def init_full_os():
    memory = LongTermMemory(str(Path(__file__).parent.parent.parent / "memory_store.json"))
    tools = get_default_registry()
    
    protocol = type('Protocol', (object,), {
        'arbitration': ArbitrationProtocol({}),
        'voting': VotingProtocol(),
        'priority': PriorityQueueProtocol()
    })()
    
    agents = {
        "ceo": CEOAgent(memory, protocol, {}),
        "researcher": ResearcherAgent(memory, tools, {}),
        "cto": CTOAgent(memory, tools, {}),
        "coder": CoderAgent(memory, tools, {}),
        "marketer": MarketerAgent(memory, tools, {}),
        "designer": DesignerAgent(memory, tools, {}),
        "copywriter": CopywriterAgent(memory, tools, {}),
        "sales": SalesAgent(memory, tools, {}),
        "automation": AutomationAgent(memory, tools, {}),
        "finance": FinanceAgent(memory, tools, {}),
        "legal": LegalAgent(memory, tools, {}),
        "support": SupportAgent(memory, tools, {}),
    }
    
    def real_delegate(task):
        assigned = getattr(task, 'assigned_to', None) or 'ceo'
        return agents.get(assigned, agents['ceo'])
    
    protocol.delegate_task = real_delegate
    
    jarvis = JarvisAgent(memory, protocol, tools, agents)
    return jarvis, memory, agents

def run_cli():
    print("=" * 60)
    print("Agent-OS JARVIS CLI — Owner Command Center")
    print("Type 'exit' to quit. 'status' for system overview.")
    print("=" * 60)
    
    jarvis, memory, agents = init_full_os()
    print(jarvis.greet())
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit", "q"]:
                print("JARVIS: Until next time, Sir.")
                break
            if user_input.lower() == "status":
                print(f"Memory entries: {len(memory.get_all().get('entries', []))}")
                print(f"Active agents: {list(agents.keys())}")
                continue
            if not user_input:
                continue
            
            result = jarvis.chat(user_input)
            print(f"\nJARVIS: {result['response']}")
            
        except KeyboardInterrupt:
            print("\nJARVIS: Session ended.")
            break
        except Exception as e:
            print(f"JARVIS: Apologies, Sir. An error occurred: {e}")

if __name__ == "__main__":
    run_cli()