"""Core message system for agent communication."""
from enum import Enum
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime


class MessageRole(str, Enum):
    """Message roles in agent communication."""
    USER = "user"
    AGENT = "agent"
    SUPERVISOR = "supervisor"
    SYSTEM = "system"
    TOOL = "tool"


class MessageType(str, Enum):
    """Types of messages."""
    TASK = "task"
    RESPONSE = "response"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    STATUS = "status"


@dataclass
class ToolCall:
    """Represents a tool call request."""
    tool_name: str
    parameters: Dict[str, Any]
    tool_id: Optional[str] = None


@dataclass
class ToolResult:
    """Represents a tool execution result."""
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: Optional[float] = None


@dataclass
class Message:
    """Core message structure for agent communication."""
    role: MessageRole
    content: str
    message_type: MessageType = MessageType.RESPONSE
    sender: Optional[str] = None
    recipient: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[ToolResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_message_id: Optional[str] = None
    conversation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "role": self.role.value,
            "content": self.content,
            "message_type": self.message_type.value,
            "sender": self.sender,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class AgentStatus:
    """Status of an agent."""
    agent_name: str
    status: str  # "idle", "working", "complete", "error", "waiting"
    current_task: Optional[str] = None
    progress: float = 0.0  # 0-1
    error_message: Optional[str] = None
    tokens_used: int = 0
    execution_time: float = 0.0
