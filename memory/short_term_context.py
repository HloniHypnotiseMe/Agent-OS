"""
Agent-OS Memory: Short-term Context Manager

Handles session-level context, conversation state, and temporary working memory.
"""

from typing import Dict, Any, List, Optional
import time

class ShortTermContext:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.context: Dict[str, Any] = {
            "current_session": str(int(time.time())),
            "conversation_turns": [],
            "active_tasks": [],
            "user_preferences": {},
            "last_actions": []
        }

    def add_turn(self, speaker: str, message: str, metadata: Dict = None):
        turn = {
            "speaker": speaker,
            "message": message,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self.context["conversation_turns"].append(turn)
        if len(self.context["conversation_turns"]) > self.max_turns:
            self.context["conversation_turns"].pop(0)
        print(f"[ShortTerm] Added turn from {speaker}")

    def get_recent_context(self, n: int = 5) -> List[Dict]:
        return self.context["conversation_turns"][-n:]

    def set_active_task(self, task_id: str, description: str):
        self.context["active_tasks"].append({"id": task_id, "description": description, "started": time.time()})

    def get_full_context(self) -> Dict:
        return self.context

    def clear_session(self):
        self.context["conversation_turns"] = []
        self.context["active_tasks"] = []
        print("[ShortTerm] Session cleared")

# Example
if __name__ == "__main__":
    ctx = ShortTermContext()
    ctx.add_turn("owner", "Research the market")
    print(len(ctx.get_recent_context()))