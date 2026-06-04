#!/usr/bin/env python3
"""
Agent-OS Simple Web Server + JARVIS API

Serves the beautiful self-contained JARVIS UI (works in any browser).
Also exposes a /api/chat endpoint that uses the REAL Python Agent-OS agents.

Usage:
    cd /home/user/agent-os
    python interfaces/web/server.py

Then open http://localhost:8000 in any browser.
"""

import sys
import os
import json
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Make sure we can import the Agent-OS modules
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from memory.long_term_memory import LongTermMemory
    from tools.tool_registry import get_default_registry
    from agents.protocol.arbitration import ArbitrationProtocol
    from agents.protocol.voting import VotingProtocol
    from agents.protocol.priority import PriorityQueueProtocol
    from core.execution.execution_engine import ExecutionEngine
    from agents.ceo.ceo import CEOAgent
    from agents.researcher.researcher import ResearcherAgent
    from agents.cto.cto import CTOAgent
    from agents.coder.coder import CoderAgent
    from agents.marketer.marketer import MarketerAgent
    from agents.designer.designer import DesignerAgent
    from agents.copywriter.copywriter import CopywriterAgent
    from agents.sales.sales import SalesAgent
    from agents.automation.automation import AutomationAgent
    from agents.finance.finance import FinanceAgent
    from agents.legal.legal import LegalAgent
    from agents.support.support import SupportAgent
    from agents.jarvis.jarvis import JarvisAgent
except ImportError as e:
    print("ERROR: Could not import Agent-OS modules. Make sure you're running from the project root.")
    print(e)
    sys.exit(1)

# Global OS components (initialized once)
OS_COMPONENTS = None

def initialize_real_os():
    """Initialize the full real Agent-OS (same as main.py but extended)."""
    global OS_COMPONENTS
    if OS_COMPONENTS:
        return OS_COMPONENTS
    
    print("[Server] Initializing real Agent-OS for browser JARVIS...")
    
    memory = LongTermMemory(str(PROJECT_ROOT / "memory_store.json"))
    tools = get_default_registry()
    
    protocol = type('Protocol', (object,), {
        'arbitration': ArbitrationProtocol({}),
        'voting': VotingProtocol(),
        'priority': PriorityQueueProtocol()
    })()
    
    execution = ExecutionEngine(
        core_config={"version": "1.0"},
        policies={"safety": True},
        routing=type('Router', (object,), {'route': lambda s, task: 'ceo'})(),
        memory=memory
    )
    
    agents = {
        "ceo": CEOAgent(memory, protocol, {}),
        "researcher": ResearcherAgent(memory, tools, {}),
        "cto": CTOAgent(memory, tools, {}),
        "coder": CoderAgent(memory, tools, {}),
        "marketer": MarketerAgent(memory, tools, {}),
        "designer": DesignerAgent(memory, tools, {}),
        "copywriter": CopywriterAgent(memory, tools, {}),
        "sales": SalesAgent(memory, tools, {}),
        "automation": AutomationAgent(memory, tools, {}),
        "finance": FinanceAgent(memory, tools, {}),
        "legal": LegalAgent(memory, tools, {}),
        "support": SupportAgent(memory, tools, {}),
    }
    
    def real_delegate(task):
        assigned = getattr(task, 'assigned_to', None) or 'ceo'
        return agents.get(assigned, agents['ceo'])
    
    protocol.delegate_task = real_delegate
    
    # Create the real JARVIS
    jarvis = JarvisAgent(memory, protocol, tools, agents)
    
    OS_COMPONENTS = {
        "memory": memory,
        "tools": tools,
        "protocol": protocol,
        "execution": execution,
        "agents": agents,
        "jarvis": jarvis
    }
    
    print("[Server] Real Agent-OS ready. JARVIS is online.")
    return OS_COMPONENTS

class AgentOSHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "/jarvis":
            # Serve the beautiful JARVIS UI
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ui_path = PROJECT_ROOT / "interfaces" / "web" / "jarvis_ui.html"
            with open(ui_path, "rb") as f:
                self.wfile.write(f.read())
            return
        
        if parsed.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            components = initialize_real_os()
            status = {
                "status": "online",
                "agents": list(components["agents"].keys()),
                "memory_entries": len(components["memory"].get_all().get("entries", [])),
                "jarvis_ready": True,
                "workflows_available": ["research_to_report", "launch_prep"]
            }
            self.wfile.write(json.dumps(status).encode())
            return
        
        if parsed.path == "/api/agents":
            components = initialize_real_os()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            agents_info = {name: {"role": type(agent).__doc__.split('\n')[0] if agent.__doc__ else "Specialist"} for name, agent in components["agents"].items()}
            self.wfile.write(json.dumps(agents_info).encode())
            return
        
        if parsed.path == "/api/memory":
            components = initialize_real_os()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            mem = components["memory"].get_all()
            self.wfile.write(json.dumps({"entries": len(mem.get("entries", [])), "recent": mem.get("entries", [])[-3:] if mem.get("entries") else []}).encode())
            return
        
        # Fallback to serving static files (if any)
        super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/api/chat":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                user_input = data.get("message", "").strip()
                
                if not user_input:
                    self._send_error(400, "No message provided")
                    return
                
                components = initialize_real_os()
                jarvis = components["jarvis"]
                
                # Use the REAL JARVIS
                result = jarvis.chat(user_input)
                
                response = {
                    "response": result["response"],
                    "delegated_to": result.get("delegated_to"),
                    "intent": result.get("intent"),
                    "timestamp": result["timestamp"],
                    "real_backend": True
                }
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"[Server] Chat error: {e}")
                self._send_error(500, str(e))
            return
        
        self._send_error(404, "Endpoint not found")
    
    def _send_error(self, code, message):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())
    
    def log_message(self, format, *args):
        # Cleaner logging
        print(f"[Server] {args[0]}")

def run_server(port=8000):
    os.chdir(PROJECT_ROOT)  # Serve from project root so relative paths work if needed
    
    # Pre-initialize so first request is fast
    initialize_real_os()
    
    # Bind to 0.0.0.0 so it is accessible from other devices on the LAN
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, AgentOSHandler)
    
    print("=" * 60)
    print("🚀 Agent-OS Web Server + JARVIS UI (Multi-Device Ready)")
    print("=" * 60)
    print(f"Local access (this machine):  http://localhost:{port}")
    print(f"LAN / other devices on same WiFi:  http://YOUR_LOCAL_IP:{port}")
    print("   (Find your IP with: ipconfig on Windows, or ifconfig/ip addr on Linux/Mac)")
    print(f"Or directly the static HTML (simulation only):  file://{PROJECT_ROOT}/interfaces/web/jarvis_ui.html")
    print("\nThe UI works 100% offline in any browser (pure JS simulation mode when opened directly).")
    print("When connected to this server, chat uses the REAL Python agents + all upgrades.")
    print("\nLocal AI (Ollama): If Ollama is running with a model (tinyllama/phi), agents can use it offline.")
    print("   (See core/models/ollama_integration.py - inspired by real C6Group.AiOS deployment)")
    print("\nFor internet access from anywhere:")
    print("  - Use ngrok: ngrok http {port}")
    print("  - Or deploy the server to a VPS / always-on machine.")
    print("  - Docker support: see deployments/ (or use Runtipi for easy self-hosting).")
    print("\nPress Ctrl+C to stop.")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down...")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)