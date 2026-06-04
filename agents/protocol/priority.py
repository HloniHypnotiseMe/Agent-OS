"""
Agent-OS Protocol: Task Priority Queue

Manages task prioritization, queuing, and scheduling for agents.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import heapq
import time

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

@dataclass(order=True)
class PrioritizedTask:
    priority: int
    timestamp: float = field(compare=False)
    task_id: str = field(compare=False)
    description: str = field(compare=False)
    agent: Optional[str] = field(compare=False, default=None)
    deadline: Optional[float] = field(compare=False, default=None)
    metadata: Dict[str, Any] = field(compare=False, default_factory=dict)

class PriorityQueueProtocol:
    def __init__(self):
        self._queue: List[PrioritizedTask] = []
        self._task_map: Dict[str, PrioritizedTask] = {}

    def add_task(self, task_id: str, description: str, priority: Priority, 
                 agent: Optional[str] = None, deadline: Optional[float] = None, 
                 metadata: Dict = None):
        """Add a task to the priority queue."""
        pt = PrioritizedTask(
            priority=priority.value,
            timestamp=time.time(),
            task_id=task_id,
            description=description,
            agent=agent,
            deadline=deadline,
            metadata=metadata or {}
        )
        heapq.heappush(self._queue, pt)
        self._task_map[task_id] = pt
        print(f"[Priority] Added task {task_id} with priority {priority.name}: {description[:60]}...")

    def get_next_task(self, for_agent: Optional[str] = None) -> Optional[PrioritizedTask]:
        """Get the highest priority task, optionally filtered by agent."""
        while self._queue:
            pt = heapq.heappop(self._queue)
            if for_agent is None or pt.agent == for_agent or pt.agent is None:
                if pt.task_id in self._task_map:
                    del self._task_map[pt.task_id]
                    print(f"[Priority] Dispatched task {pt.task_id} to {for_agent or 'any'}")
                    return pt
            else:
                # Re-add if not for this agent (simple approach; better impl would use better data struct)
                heapq.heappush(self._queue, pt)
                break  # avoid infinite if all don't match
        return None

    def peek(self) -> Optional[PrioritizedTask]:
        """View the next task without removing."""
        if self._queue:
            return self._queue[0]
        return None

    def remove_task(self, task_id: str) -> bool:
        """Remove a specific task."""
        if task_id in self._task_map:
            pt = self._task_map[task_id]
            self._queue = [t for t in self._queue if t.task_id != task_id]
            heapq.heapify(self._queue)
            del self._task_map[task_id]
            return True
        return False

    def list_tasks(self) -> List[Dict]:
        return [pt.__dict__ for pt in self._queue]

# Example
if __name__ == "__main__":
    pq = PriorityQueueProtocol()
    pq.add_task("t1", "Research competitors", Priority.HIGH, "researcher")
    pq.add_task("t2", "Fix critical bug", Priority.CRITICAL, "coder")
    next_task = pq.get_next_task()
    print(f"Next task: {next_task.description if next_task else 'None'}")