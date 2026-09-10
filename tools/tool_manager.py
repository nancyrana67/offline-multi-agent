"""Tool management system."""
import logging
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """Tool definition."""
    name: str
    description: str
    execute: Callable
    parameters: Dict[str, Any]


class ToolManager:
    """Manages available tools for agents."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        execute_fn: Callable,
        parameters: Dict[str, Any] = None,
    ):
        """Register a new tool."""
        tool = Tool(
            name=name,
            description=description,
            execute=execute_fn,
            parameters=parameters or {},
        )
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, str]:
        """List all available tools."""
        return {name: tool.description for name, tool in self.tools.items()}

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool."""
        tool = self.get_tool(tool_name)
        if not tool:
            logger.error(f"Tool not found: {tool_name}")
            return None

        try:
            if hasattr(tool.execute, '__await__'):
                return await tool.execute(**kwargs)
            else:
                return tool.execute(**kwargs)
        except Exception as e:
            logger.error(f"Tool execution error: {str(e)}")
            return None
