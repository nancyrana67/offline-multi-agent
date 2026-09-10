"""Long-term memory management."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from config import DATA_DIR

logger = logging.getLogger(__name__)


class LongTermMemory:
    """Manages persistent long-term memory."""

    def __init__(self):
        self.memory_file = DATA_DIR / "long_term_memory.json"
        self.memories: Dict[str, Dict[str, Any]] = {}
        self.load()

    def store(self, key: str, value: Any, category: str = "general"):
        """Store information in long-term memory."""
        self.memories[key] = {
            "value": value,
            "category": category,
            "timestamp": datetime.now().isoformat(),
        }
        self.save()

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve information from memory."""
        if key in self.memories:
            return self.memories[key]["value"]
        return None

    def search(self, category: str) -> List[Dict[str, Any]]:
        """Search memories by category."""
        results = []
        for key, data in self.memories.items():
            if data["category"] == category:
                results.append({"key": key, **data})
        return results

    def delete(self, key: str) -> bool:
        """Delete a memory."""
        if key in self.memories:
            del self.memories[key]
            self.save()
            return True
        return False

    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """Get all memories."""
        return self.memories

    def save(self):
        """Save to disk."""
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.memories, f)
        except Exception as e:
            logger.error(f"Error saving long-term memory: {str(e)}")

    def load(self):
        """Load from disk."""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, "r") as f:
                    self.memories = json.load(f)
        except Exception as e:
            logger.error(f"Error loading long-term memory: {str(e)}")
