"""
Agent-OS Tools: Tool Registry and Interface

Central place to register, discover, and securely execute tools for agents.
"""

from typing import Dict, Callable, Any, List, Optional
import inspect

class Tool:
    def __init__(self, name: str, func: Callable, description: str, required_params: List[str] = None, 
                 dangerous: bool = False, category: str = "general"):
        self.name = name
        self.func = func
        self.description = description
        self.required_params = required_params or []
        self.dangerous = dangerous
        self.category = category

    def execute(self, **kwargs):
        # In real: add security checks, logging, sandboxing
        if self.dangerous:
            print(f"[Tools] WARNING: Executing dangerous tool {self.name}")
        return self.func(**kwargs)

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool
        print(f"[Tools] Registered: {tool.name} ({tool.category})")

    def get(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)

    def list_tools(self, category: str = None) -> List[Dict]:
        tools_list = []
        for name, tool in self.tools.items():
            if category is None or tool.category == category:
                tools_list.append({
                    "name": name,
                    "description": tool.description,
                    "category": tool.category,
                    "dangerous": tool.dangerous
                })
        return tools_list

    def execute(self, name: str, **kwargs) -> Any:
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        return tool.execute(**kwargs)

# Example built-in tools
def web_search(query: str, num_results: int = 5) -> List[Dict]:
    """Placeholder web search tool."""
    print(f"[Tool:web_search] Searching for: {query}")
    return [
        {"title": f"Result 1 for {query}", "url": "https://example.com/1", "snippet": "Relevant info about AI OS..."},
        {"title": f"Result 2 for {query}", "url": "https://example.com/2", "snippet": "Market analysis..."}
    ]

def code_executor(code: str, language: str = "python") -> Dict:
    """Safe code execution sandbox placeholder."""
    print(f"[Tool:code_executor] Executing {language} code...")
    return {"status": "success", "output": "Code executed successfully (simulated)", "language": language}

def file_writer(path: str, content: str) -> Dict:
    """Write files (dangerous - use with care)."""
    with open(path, 'w') as f:
        f.write(content)
    return {"status": "written", "path": path}

# Register defaults
def get_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    # Real web search (enhanced)
    try:
        from tools.web.web_search import web_search as real_web_search
        registry.register(Tool("web_search", real_web_search, "Real web search (DuckDuckGo via aiohttp+bs4)", ["query"], dangerous=False, category="research"))
    except:
        registry.register(Tool("web_search", web_search, "Search the web for information (fallback)", ["query"], dangerous=False, category="research"))
    
    registry.register(Tool("code_executor", code_executor, "Execute code in sandbox", ["code"], dangerous=True, category="development"))
    registry.register(Tool("file_writer", file_writer, "Write content to a file", ["path", "content"], dangerous=True, category="filesystem"))
    
    # MCP-style tools (inspired by googleapis/mcp-toolbox)
    try:
        from tools.mcp.mcp_database_tool import get_mcp_database_tool
        mcp_db = get_mcp_database_tool()
        registry.register(Tool("mcp_query_database", mcp_db.execute_query, "MCP-standardized database query (Finance/Legal/CRM)", ["query"], dangerous=True, category="data"))
        registry.register(Tool("mcp_list_tables", mcp_db.list_tables, "List available MCP database tables", [], dangerous=False, category="data"))
    except Exception as e:
        print(f"[ToolRegistry] MCP tools not fully loaded: {e}")
    
    # Ollama local LLM (inspired by real deployment in https://github.com/HloniHypnotiseMe/C6Group.AiOS)
    try:
        from core.models.ollama_integration import get_local_model_response
        registry.register(Tool("local_llm", get_local_model_response, "Query local Ollama model (tinyllama, phi, etc.) for offline AI", ["prompt", "model"], dangerous=False, category="ai"))
    except Exception as e:
        print(f"[ToolRegistry] Ollama integration not loaded: {e}")
    
    return registry

# Example
if __name__ == "__main__":
    reg = get_default_registry()
    print(reg.list_tools())
    result = reg.execute("web_search", query="Agent-OS architecture")
    print(result)