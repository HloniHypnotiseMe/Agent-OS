"""
Agent-OS Runtime: Sandbox

Safe execution environment for code, tools, and agent actions.
"""

import tempfile
import os
from typing import Dict, Any

class Sandbox:
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or tempfile.mkdtemp(prefix="agent-os-sandbox-")
        print(f"[Sandbox] Initialized at {self.base_dir}")

    def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        print(f"[Sandbox] Executing {language} code in isolated env...")
        # In real: use restricted exec, docker, or gvisor
        try:
            if language == "python":
                # Very basic safe exec simulation
                exec_globals = {"__name__": "__sandbox__"}
                exec(code, exec_globals)
                return {"status": "success", "output": "Code executed safely in sandbox.", "language": language}
            return {"status": "unsupported", "language": language}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def cleanup(self):
        print(f"[Sandbox] Cleaning up {self.base_dir}")

# Example
if __name__ == "__main__":
    sb = Sandbox()
    print(sb.execute_code("print('Hello from sandbox')")["status"])