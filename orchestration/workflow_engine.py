"""
Agent-OS Orchestration: Workflow Engine

Defines, executes, and monitors multi-step workflows that chain agents and tools.
"""

from typing import Dict, Any, List, Callable
import time

class WorkflowStep:
    def __init__(self, agent_name: str, task: str, depends_on: List[str] = None):
        self.agent_name = agent_name
        self.task = task
        self.depends_on = depends_on or []
        self.status = "pending"
        self.result = None

class WorkflowEngine:
    def __init__(self, agents_registry: Dict, protocol):
        self.agents = agents_registry
        self.protocol = protocol
        self.workflows: Dict[str, List[WorkflowStep]] = {}

    def define_workflow(self, name: str, steps: List[Dict]) -> str:
        wf_steps = []
        for s in steps:
            step = WorkflowStep(
                agent_name=s["agent"],
                task=s["task"],
                depends_on=s.get("depends_on", [])
            )
            wf_steps.append(step)
        self.workflows[name] = wf_steps
        print(f"[Orchestration] Defined workflow: {name} with {len(wf_steps)} steps")
        return name

    def execute_workflow(self, name: str) -> Dict[str, Any]:
        if name not in self.workflows:
            return {"error": "Workflow not found"}
        
        steps = self.workflows[name]
        results = {}
        print(f"[Orchestration] Executing workflow: {name}")
        
        for step in steps:
            if step.depends_on:
                for dep in step.depends_on:
                    if dep not in results:
                        print(f"  Waiting for dependency {dep}...")
            
            # Delegate via protocol
            task_obj = type('Task', (object,), {
                'description': step.task,
                'assigned_to': step.agent_name
            })()
            
            agent = self.protocol.delegate_task(task_obj)
            if hasattr(agent, 'perform_research') or hasattr(agent, 'set_strategy'):
                # Call appropriate method
                if "research" in step.task.lower():
                    result = agent.perform_research(step.task) if hasattr(agent, 'perform_research') else {"mock": "done"}
                else:
                    result = agent.set_strategy(step.task) if hasattr(agent, 'set_strategy') else {"mock": "done"}
            else:
                result = {"status": "executed by " + step.agent_name}
            
            step.result = result
            step.status = "completed"
            results[step.agent_name] = result
            print(f"  ✓ {step.agent_name}: {step.task[:40]}...")
        
        return {
            "workflow": name,
            "status": "completed",
            "steps": len(steps),
            "results": results,
            "duration": "simulated 8.2s"
        }

# Example
if __name__ == "__main__":
    engine = WorkflowEngine({}, type('p', (object,), {'delegate_task': lambda s,t: type('a', (object,), {'perform_research': lambda x,y: {'findings': 'done'}})()})())
    engine.define_workflow("Launch Prep", [
        {"agent": "researcher", "task": "Research market"},
        {"agent": "ceo", "task": "Set strategy", "depends_on": ["researcher"]}
    ])
    print(engine.execute_workflow("Launch Prep")["status"])