"""
Agent-OS Protocol: Voting System

Implements democratic or weighted voting for agent decisions.
"""

from typing import List, Dict, Any
from collections import Counter

class Vote:
    def __init__(self, agent_id: str, choice: str, weight: float = 1.0, rationale: str = ""):
        self.agent_id = agent_id
        self.choice = choice
        self.weight = weight
        self.rationale = rationale

class VotingProtocol:
    def __init__(self):
        self.votes: List[Vote] = []

    def cast_vote(self, agent_id: str, choice: str, weight: float = 1.0, rationale: str = ""):
        """Cast a vote from an agent."""
        vote = Vote(agent_id, choice, weight, rationale)
        self.votes.append(vote)
        print(f"[Voting] {agent_id} voted for '{choice}' (weight: {weight})")

    def tally_votes(self) -> Dict[str, Any]:
        """Tally the votes and determine winner."""
        if not self.votes:
            return {"winner": None, "breakdown": {}, "total_weight": 0}

        choice_weights = Counter()
        for vote in self.votes:
            choice_weights[vote.choice] += vote.weight

        total_weight = sum(choice_weights.values())
        winner = choice_weights.most_common(1)[0][0] if choice_weights else None

        breakdown = {
            choice: {"weight": w, "percentage": round(w / total_weight * 100, 1)} 
            for choice, w in choice_weights.items()
        }

        result = {
            "winner": winner,
            "breakdown": breakdown,
            "total_weight": total_weight,
            "num_voters": len(self.votes)
        }

        print(f"[Voting] Winner: {winner} with {breakdown.get(winner, {}).get('percentage', 0)}%")
        return result

    def reset(self):
        self.votes = []

# Example usage
if __name__ == "__main__":
    vp = VotingProtocol()
    vp.cast_vote("ceo", "proceed_with_mvp", weight=2.0, rationale="Business priority")
    vp.cast_vote("cto", "proceed_with_mvp", weight=1.5)
    vp.cast_vote("researcher", "full_architecture_first", weight=1.0)
    result = vp.tally_votes()
    print(result)