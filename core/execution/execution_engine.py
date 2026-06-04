"""
Agent-OS Core: Execution Engine

The central execution flow controller. Routes tasks, manages context, enforces policies.
"""

from typing import Dict, Any, Optional, List
import time

class ExecutionEngine:
    def __init__(self, core_config: Dict, policies: Dict, routing: Any, memory: Any):
        self.config = core_config
        self.policies = policies
        self.routing = routing
        self.memory = memory
        self.running_tasks = {}

    def execute_task(self, task_description: str, agent_name: Optional[str] = None, 
                     context: Dict = None) -> Dict[str, Any]:
        """
        Main entry point for executing any task in the OS.
        """
        start_time = time.time()
        task_id = f"task_{int(start_time)}"

        print(f"[Execution] Starting task: {task_description}")

        # 1. Check policies
        if not self._check_policies(task_description):
            return {"status": "denied", "reason": "Policy violation", "task_id": task_id}

        # 2. Route to appropriate agent or handle
        target = agent_name or self.routing.route(task_description)

        # 3. Retrieve relevant context/memory
        relevant_context = self.memory.retrieve_relevant(task_description, limit=5)

        # 4. Execute (placeholder - in real: call agent)
        result = self._simulate_agent_execution(target, task_description, relevant_context)

        # 5. Store outcome in memory
        self.memory.store(task_id, task_description, result, target)

        duration = time.time() - start_time
        print(f"[Execution] Completed in {duration:.2f}s. Status: {result.get('status')}")

        return {
            "task_id": task_id,
            "target_agent": target,
            "result": result,
            "duration": duration,
            "context_used": len(relevant_context)
        }

    def _check_policies(self, task: str) -> bool:
        """Enforce core policies."""
        forbidden = ["harm", "illegal", "deceptive"]
        task_lower = task.lower()
        for word in forbidden:
            if word in task_lower:
                print(f"[Execution] Policy violation detected: {word}")
                return False
        return True

    def _simulate_agent_execution(self, agent: str, task: str, context: List) -> Dict:
        """Placeholder for actual agent invocation."""
        # In production: send to agents/{agent}/ with prompt + tools + memory
        return {
            "status": "success",
            "output": f"[{agent}] Completed: {task}. Used {len(context)} memory items.",
            "confidence": 0.92,
            "actions_taken": ["analyzed", "planned", "executed"]
        }

# Example
if __name__ == "__main__":
    # Placeholders
    engine = ExecutionEngine({}, {}, type('obj', (object,), {'route': lambda s,d: 'ceo'})(), 
                             type('obj', (object,), {'retrieve_relevant': lambda s,d,l: [], 'store': lambda *a: None})())
    result = engine.execute_task("Develop a marketing plan for Agent-OS launch")
    print(result)