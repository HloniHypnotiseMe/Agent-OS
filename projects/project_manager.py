"""
Agent-OS Projects: Project & Task Management
"""

from typing import Dict, Any, List
import time

class ProjectManager:
    def __init__(self):
        self.projects: Dict[str, Dict] = {}

    def create_project(self, name: str, owner: str = "owner", description: str = "") -> Dict:
        pid = f"proj_{int(time.time())}"
        proj = {
            "id": pid,
            "name": name,
            "owner": owner,
            "description": description,
            "status": "active",
            "tasks": [],
            "created": time.time()
        }
        self.projects[pid] = proj
        print(f"[Projects] Created project: {name}")
        return proj

    def add_task(self, project_id: str, task_desc: str, assigned_to: str) -> Dict:
        if project_id not in self.projects:
            return {"error": "Project not found"}
        task = {"id": f"task_{int(time.time())}", "desc": task_desc, "assigned": assigned_to, "status": "open"}
        self.projects[project_id]["tasks"].append(task)
        return task

# Global
pm = ProjectManager()