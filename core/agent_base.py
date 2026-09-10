"""Base agent class for all AI agents."""
import asyncio
import json
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
import logging

from core.message import Message, MessageRole, MessageType, ToolCall, ToolResult, AgentStatus

logger = logging.getLogger(__name__)


class Agent(ABC):
    """Base class for all AI agents."""

    def __init__(
        self,
        name: str,
        description: str,
        model: str = None,
        tools: List[str] = None,
        max_retries: int = 3,
    ):
        self.name = name
        self.description = description
        self.model = model or "mistral"
        self.tools: Set[str] = set(tools or [])
        self.max_retries = max_retries
        self.status = AgentStatus(agent_name=name, status="idle")
        self.message_history: List[Message] = []
        self.start_time: Optional[float] = None

    async def process_message(self, message: Message) -> Message:
        """Process an incoming message and return a response."""
        try:
            self.status.status = "working"
            self.status.current_task = message.content[:50]
            self.start_time = time.time()

            # Store message
            self.message_history.append(message)

            # Process based on message type
            if message.message_type == MessageType.TASK:
                response = await self.handle_task(message)
            elif message.message_type == MessageType.TOOL_RESULT:
                response = await self.handle_tool_result(message)
            else:
                response = await self.handle_message(message)

            response.sender = self.name
            self.message_history.append(response)
            self.status.status = "complete"
            self.status.execution_time = time.time() - self.start_time

            return response

        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}")
            self.status.status = "error"
            self.status.error_message = str(e)
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    @abstractmethod
    async def handle_task(self, message: Message) -> Message:
        """Handle a task message. Implement in subclass."""
        pass

    async def handle_message(self, message: Message) -> Message:
        """Handle a regular message. Can be overridden in subclass."""
        return await self.handle_task(message)

    async def handle_tool_result(self, message: Message) -> Message:
        """Handle tool result. Can be overridden in subclass."""
        return Message(
            role=MessageRole.AGENT,
            content="Tool result received",
            message_type=MessageType.RESPONSE,
            sender=self.name,
        )

    def request_tool(
        self, tool_name: str, parameters: Dict[str, Any]
    ) -> ToolCall:
        """Create a tool call request."""
        return ToolCall(tool_name=tool_name, parameters=parameters)

    def get_status(self) -> AgentStatus:
        """Get current agent status."""
        return self.status

    def reset_status(self):
        """Reset agent status."""
        self.status = AgentStatus(agent_name=self.name, status="idle")

    def get_history(self) -> List[Message]:
        """Get message history."""
        return self.message_history

    def clear_history(self):
        """Clear message history."""
        self.message_history = []
