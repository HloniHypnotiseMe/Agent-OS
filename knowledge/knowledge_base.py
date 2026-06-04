"""
Agent-OS Knowledge: Central Knowledge Base (RAG stub)
"""

from typing import Dict, Any, List

class KnowledgeBase:
    def __init__(self):
        self.documents: Dict[str, Dict] = {}

    def add_document(self, doc_id: str, content: str, metadata: Dict = None):
        self.documents[doc_id] = {
            "content": content,
            "metadata": metadata or {},
            "added": __import__('time').time()
        }
        print(f"[Knowledge] Added document: {doc_id}")

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        # Simple keyword search stub
        results = []
        q_lower = query.lower()
        for did, doc in self.documents.items():
            if q_lower in doc["content"].lower():
                results.append({"id": did, "content": doc["content"][:200], "score": 0.85})
        return results[:top_k]

    def get_stats(self) -> Dict:
        return {"documents": len(self.documents)}

kb = KnowledgeBase()