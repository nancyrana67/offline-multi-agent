"""Conversation memory management."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from config import DATA_DIR
from core.message import Message

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Manages current conversation memory."""

    def __init__(self, max_turns: int = 100):
        self.max_turns = max_turns
        self.messages: List[Dict[str, Any]] = []
        self.memory_file = DATA_DIR / "conversation_memory.json"
        self.load()

    def add_message(self, message: Message):
        """Add message to conversation memory."""
        msg_dict = {
            "role": message.role.value,
            "content": message.content,
            "sender": message.sender,
            "timestamp": message.timestamp.isoformat(),
            "type": message.message_type.value,
        }
        self.messages.append(msg_dict)

        # Keep only recent messages
        if len(self.messages) > self.max_turns:
            self.messages = self.messages[-self.max_turns:]

        self.save()

    def get_recent(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent messages."""
        return self.messages[-count:]

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all messages."""
        return self.messages

    def clear(self):
        """Clear conversation memory."""
        self.messages = []
        self.save()

    def save(self):
        """Save to disk."""
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.messages, f)
        except Exception as e:
            logger.error(f"Error saving conversation memory: {str(e)}")

    def load(self):
        """Load from disk."""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, "r") as f:
                    self.messages = json.load(f)
        except Exception as e:
            logger.error(f"Error loading conversation memory: {str(e)}")
