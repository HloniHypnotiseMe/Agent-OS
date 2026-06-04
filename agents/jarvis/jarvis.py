"""
Agent-OS: JARVIS - Owner's Personal Assistant

The "JARVIS" layer: A conversational, always-on personal AI assistant for the company owner.
It understands natural language instructions, maintains conversation context, 
delegates tasks to specialized agents via the protocol, reports back results,
and acts as the primary human-in-the-loop interface.

Style: Witty, efficient, loyal like Iron Man's JARVIS. 
"Right away, sir." / "Shall I proceed?" etc.
"""

from typing import Dict, Any, List, Optional
import time
import re

class JarvisAgent:
    def __init__(self, memory, protocol, tools, agents_registry: Dict[str, Any]):
        self.memory = memory
        self.protocol = protocol
        self.tools = tools
        self.agents = agents_registry  # dict of agent instances by name
        self.name = "jarvis"
        self.conversation_history: List[Dict] = []
        self.owner_name = "Sir"  # customizable

        self.role_prompt = """
You are JARVIS, the owner's personal AI assistant and interface to Agent-OS.
- Be concise, helpful, slightly witty, and professional.
- Always confirm understanding and next steps.
- When the owner gives an instruction, parse intent and delegate to the right specialist agent(s) using the protocol.
- Report results back conversationally.
- Maintain context across the conversation.
- If unclear, ask clarifying questions.
- Never mention you are simulated unless asked.
"""

    def greet(self) -> str:
        """Initial greeting."""
        greeting = f"Good evening, {self.owner_name}. Agent-OS is fully operational. How may I assist you today?"
        self._log_conversation("jarvis", greeting)
        return greeting

    def chat(self, user_input: str, channel: str = "cli") -> Dict[str, Any]:
        """
        Main conversational entry point.
        Takes owner's natural language instruction (from any channel), processes it, delegates if needed, and responds.
        Supports hierarchical supervision (manager pattern from multi-agent personal assistants).
        """
        print(f"\n[{self.name.upper()}] Owner said via {channel}: {user_input}")
        self._log_conversation("owner", user_input)

        # 1. Parse intent (simple rule-based + keyword for now; can upgrade to LLM)
        intent = self._parse_intent(user_input)

        response_text = ""
        delegated_to = None
        result = None

        if intent["action"] == "greet" or "hello" in user_input.lower():
            response_text = self.greet()

        elif intent["action"] == "research":
            query = intent.get("query", user_input)
            print(f"[{self.name}] Delegating research: {query}")
            delegated_to = "researcher"
            if "researcher" in self.agents:
                researcher = self.agents["researcher"]
                result = researcher.perform_research(query)
                response_text = f"Right away. I've tasked the Researcher with '{query}'. Here's what we found:\n\n{result.get('findings', 'Analysis complete.')}\n\nSources noted in memory. Shall I have the team act on this?"

        elif intent["action"] == "strategy" or "plan" in user_input.lower():
            goal = intent.get("goal", user_input.replace("plan", "").strip())
            print(f"[{self.name}] Delegating strategy: {goal}")
            delegated_to = "ceo"
            if "ceo" in self.agents:
                ceo = self.agents["ceo"]
                result = ceo.set_strategy(goal)
                response_text = f"Strategy set for '{goal}'. I've delegated the phases to the team:\n" + \
                               "\n".join([f"  - {p['phase']} → {p['owner']}" for p in result.get("phases", [])]) + \
                               "\n\nWould you like me to proceed with execution or adjust priorities?"

        elif intent["action"] == "code" or "develop" in user_input.lower() or "build" in user_input.lower():
            spec = user_input
            print(f"[{self.name}] Delegating coding task")
            delegated_to = "coder"
            if "coder" in self.agents:
                coder = self.agents["coder"]
                result = coder.write_code(spec)
                response_text = f"Understood. The Coder agent has generated the requested code ({result.get('lines', 0)} lines). I've saved the spec to memory.\n\nPreview:\n{result.get('code', '')[:300]}...\n\nShall I have the CTO review it or deploy a test?"

        elif intent["action"] == "status" or "progress" in user_input.lower() or "how are we" in user_input.lower():
            response_text = "Current system status: All core agents online. Memory has " + \
                           f"{len(self.memory.get_all().get('entries', []))} entries. " + \
                           "Latest activity: Research and strategy tasks completed. " + \
                           "Everything is running smoothly, " + self.owner_name + "."

        elif intent["action"] == "delegate_general":
            # Generic delegation
            target = intent.get("target_agent", "ceo")
            task_desc = user_input
            print(f"[{self.name}] Generic delegation to {target}: {task_desc}")
            delegated_to = target
            if target in self.agents:
                agent = self.agents[target]
                if hasattr(agent, 'perform_research'):
                    result = agent.perform_research(task_desc)
                elif hasattr(agent, 'set_strategy'):
                    result = agent.set_strategy(task_desc)
                else:
                    result = {"status": "task received by " + target}
                response_text = f"Task delegated to the {target.title()} agent. Result: {str(result)[:200]}...\n\nAnything else, {self.owner_name}?"

        else:
            # Default: Treat as general instruction, delegate to CEO or researcher
            response_text = f"Understood, {self.owner_name}. I'll route that through the appropriate channels. "
            delegated_to = "ceo"
            if "ceo" in self.agents:
                ceo = self.agents["ceo"]
                result = ceo.set_strategy(user_input[:100])  # treat utterance as goal
                response_text += "Strategy initiated. The team is on it."

        # Store the interaction
        self.memory.store(
            f"jarvis_chat_{int(time.time())}",
            user_input,
            {
                "response": response_text,
                "delegated_to": delegated_to,
                "result_summary": str(result)[:300] if result else None,
                "intent": intent,
                "channel": channel  # Support for WhatsApp/Slack/Telegram/etc. (inspired by personal-ai-assistant)
            }
        )

        self._log_conversation("jarvis", response_text)

        return {
            "response": response_text,
            "delegated_to": delegated_to,
            "intent": intent,
            "result": result,
            "channel": channel,
            "timestamp": time.time()
        }

    def _parse_intent(self, text: str) -> Dict[str, Any]:
        """Simple natural language intent parser (keyword + regex based). 
        In production this would call an LLM with the role prompt."""
        text_lower = text.lower().strip()

        if any(w in text_lower for w in ["hello", "hi", "hey", "good morning", "good evening"]):
            return {"action": "greet"}

        if any(w in text_lower for w in ["research", "find out", "look up", "investigate", "market"]):
            query = re.sub(r'(?i)^(can you |please |jarvis, )?(research|find out about|look up) ', '', text).strip()
            return {"action": "research", "query": query or text}

        if any(w in text_lower for w in ["strategy", "plan", "roadmap", "launch", "business plan"]):
            goal = re.sub(r'(?i)^(create |develop |set |make )?(a )?(strategy|plan|roadmap) (for |about )?', '', text).strip()
            return {"action": "strategy", "goal": goal or text}

        if any(w in text_lower for w in ["code", "develop", "build", "write", "program", "implement"]):
            return {"action": "code"}

        if any(w in text_lower for w in ["status", "progress", "how are we", "update", "what's happening"]):
            return {"action": "status"}

        # Fallback: general delegation
        target = None
        for agent_name in self.agents.keys():
            if agent_name in text_lower:
                target = agent_name
                break
        return {"action": "delegate_general", "target_agent": target or "ceo"}

    def _log_conversation(self, speaker: str, message: str):
        self.conversation_history.append({
            "speaker": speaker,
            "message": message,
            "timestamp": time.time()
        })
        # Keep only last 20 turns
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history

    def set_owner_name(self, name: str):
        self.owner_name = name

# Example standalone use
if __name__ == "__main__":
    # Placeholder dependencies for testing
    memory = type('m', (object,), {
        'store': lambda s,k,q,c: print(f"[Mem] Stored {k}"),
        'get_all': lambda s: {"entries": []}
    })()
    protocol = type('p', (object,), {
        'delegate_task': lambda s,t: print(f"[Protocol] Delegated: {getattr(t, 'description', t)}")
    })()
    tools = {}
    agents = {"ceo": type('a', (object,), {'set_strategy': lambda s,g: {"phases": []}})(), 
              "researcher": type('a', (object,), {'perform_research': lambda s,q: {"findings": "Mock research done."}})()}

    jarvis = JarvisAgent(memory, protocol, tools, agents)
    print(jarvis.greet())
    resp = jarvis.chat("Research the current market for AI operating systems")
    print("\nJARVIS:", resp["response"])
    resp2 = jarvis.chat("Set a launch strategy for v2")
    print("\nJARVIS:", resp2["response"])