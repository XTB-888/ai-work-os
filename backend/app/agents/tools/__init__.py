"""
Agent Tools - Tool Registry
Central registry for all agent tools.
"""
from typing import Dict, Any, Callable
from app.agents.tools.code_executor import code_executor
from app.agents.tools.web_search import web_search_tool
from app.agents.tools.file_manager import file_manager


class ToolRegistry:
    """
    Central registry for agent tools.
    Provides a unified interface for agents to access tools.
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools."""
        # Code Executor
        self.register_tool(
            name="code_executor",
            description="Execute Python code in a safe environment",
            function=code_executor.execute,
            parameters={
                "code": "Python code to execute",
                "context": "Optional context variables (dict)"
            }
        )

        # Web Search
        self.register_tool(
            name="web_search",
            description="Search the web for information",
            function=web_search_tool.search,
            parameters={
                "query": "Search query",
                "max_results": "Maximum number of results (default: 5)"
            }
        )

        # File Manager - Write
        self.register_tool(
            name="write_file",
            description="Write content to a file",
            function=file_manager.write_file,
            parameters={
                "file_path": "Relative file path",
                "content": "File content"
            }
        )

        # File Manager - Read
        self.register_tool(
            name="read_file",
            description="Read content from a file",
            function=file_manager.read_file,
            parameters={
                "file_path": "Relative file path"
            }
        )

        # File Manager - List
        self.register_tool(
            name="list_files",
            description="List files in a directory",
            function=file_manager.list_files,
            parameters={
                "directory": "Directory path (default: current)"
            }
        )

    def register_tool(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Dict[str, str]
    ):
        """
        Register a new tool.
        
        Args:
            name: Tool name
            description: Tool description
            function: Tool function
            parameters: Parameter descriptions
        """
        self.tools[name] = {
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters
        }

    def get_tool(self, name: str) -> Dict[str, Any]:
        """Get a tool by name."""
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """List all available tools."""
        return {
            name: {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for name, tool in self.tools.items()
        }

    async def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name.
        
        Args:
            name: Tool name
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        tool = self.get_tool(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }

        try:
            function = tool["function"]
            # Check if function is async
            if hasattr(function, '__call__'):
                import inspect
                if inspect.iscoroutinefunction(function):
                    result = await function(**kwargs)
                else:
                    result = function(**kwargs)
            else:
                result = function(**kwargs)
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution error: {str(e)}"
            }


# Global instance
tool_registry = ToolRegistry()
