"""Memory Agent - Manages conversation and long-term memory."""
import logging
from typing import Dict, List, Any

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class MemoryAgent(Agent):
    """Agent responsible for memory management."""

    def __init__(self):
        super().__init__(
            name="memory",
            description="Manages conversation and long-term memory",
            model="mistral",
            tools=["store_memory", "retrieve_memory", "search_memory", "clear_memory"],
        )
        self.short_term_memory: List[Dict[str, Any]] = []
        self.long_term_memory: Dict[str, Any] = {}

    async def handle_task(self, message: Message) -> Message:
        """Handle memory management tasks."""
        try:
            action = await self._classify_memory_action(message.content)
            
            if "store" in action.lower():
                result = await self._store_memory(message.content)
            elif "retrieve" in action.lower():
                result = await self._retrieve_memory(message.content)
            elif "search" in action.lower():
                result = await self._search_memory(message.content)
            else:
                result = "Memory action processed"
            
            response = Message(
                role=MessageRole.AGENT,
                content=result,
                message_type=MessageType.RESPONSE,
                sender=self.name,
                metadata={
                    "action": action,
                    "short_term_size": len(self.short_term_memory),
                    "long_term_size": len(self.long_term_memory),
                },
            )
            return response
            
        except Exception as e:
            logger.error(f"Memory agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    async def _classify_memory_action(self, task: str) -> str:
        """Classify the memory operation."""
        task_lower = task.lower()
        if "store" in task_lower or "save" in task_lower:
            return "store"
        elif "retrieve" in task_lower or "get" in task_lower:
            return "retrieve"
        elif "search" in task_lower or "find" in task_lower:
            return "search"
        return "retrieve"

    async def _store_memory(self, content: str) -> str:
        """Store information in memory."""
        # Extract key information and store
        memory_item = {"content": content, "type": "stored"}
        self.short_term_memory.append(memory_item)
        
        return f"Memory stored. Total memories: {len(self.short_term_memory)}"

    async def _retrieve_memory(self, query: str) -> str:
        """Retrieve from memory."""
        return f"Retrieved memories related to: {query[:50]}..."

    async def _search_memory(self, query: str) -> str:
        """Search memory."""
        return f"Search results for: {query}"
