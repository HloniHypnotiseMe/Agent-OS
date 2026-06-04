"""
Agent-OS Memory: Long-term Memory System

Persistent storage for knowledge, past tasks, agent experiences, and learnings.
Supports retrieval, storage, and self-improvement via reflection.
"""

from typing import Dict, List, Any, Optional
import json
import time
from pathlib import Path

class LongTermMemory:
    def __init__(self, storage_path: str = "./memory_store.json"):
        self.storage_path = Path(storage_path)
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    self._data = json.load(f)
            except:
                self._data = {}
        else:
            self._data = {"entries": [], "reflections": []}

    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self._data, f, indent=2)

    def store(self, key: str, query_or_task: str, content: Any, metadata: Dict = None):
        """Store a new memory entry."""
        entry = {
            "id": f"mem_{int(time.time()*1000)}",
            "key": key,
            "query": query_or_task,
            "content": content,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self._data.setdefault("entries", []).append(entry)
        self._save()
        print(f"[Memory] Stored: {key}")

    def retrieve(self, query: str, k: int = 5, filters: Dict = None) -> List[Dict]:
        """Retrieve relevant memories (simple keyword match for now)."""
        query_lower = query.lower()
        matches = []
        for entry in self._data.get("entries", []):
            if query_lower in str(entry.get("query", "")).lower() or query_lower in str(entry.get("content", "")).lower():
                matches.append(entry)
        
        # Sort by recency
        matches.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return matches[:k]

    def retrieve_relevant(self, query: str, limit: int = 5) -> List[Dict]:
        """Alias for retrieve with semantic hint (expand with embeddings later)."""
        return self.retrieve(query, k=limit)

    def reflect(self, period: str = "daily"):
        """Self-reflection to improve the system (core of self-improving workflows)."""
        recent = self.retrieve("recent", k=20)
        reflection = {
            "period": period,
            "timestamp": time.time(),
            "insights": f"Processed {len(recent)} recent entries. Identified patterns in agent delegation success.",
            "improvements": ["Enhance protocol arbitration", "Add more tool integrations"]
        }
        self._data.setdefault("reflections", []).append(reflection)
        self._save()
        print(f"[Memory] Reflection completed for {period}")
        return reflection

    def get_all(self) -> Dict:
        return self._data

# Example
if __name__ == "__main__":
    mem = LongTermMemory("/tmp/test_memory.json")
    mem.store("research", "AI OS market", {"size": "large", "growth": "40%"})
    results = mem.retrieve("AI OS")
    print(f"Retrieved {len(results)} items")
    mem.reflect()
