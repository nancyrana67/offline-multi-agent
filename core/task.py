"""Task management system."""
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class TaskStatus(str, Enum):
    """Task status states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class SubTask:
    """A subtask within a main task."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)  # IDs of subtasks this depends on

    def is_ready(self, completed_subtasks: Set[str]) -> bool:
        """Check if all dependencies are completed."""
        return all(dep in completed_subtasks for dep in self.dependencies)


@dataclass
class Task:
    """Main task structure."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    user_request: str = ""
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Subtasks and execution
    subtasks: List[SubTask] = field(default_factory=list)
    execution_plan: str = ""  # String representation of the plan
    
    # Results and errors
    result: Optional[Any] = None
    error: Optional[str] = None
    
    # Agents involved
    agents_involved: Set[str] = field(default_factory=set)
    
    # Performance metrics
    total_tokens_used: int = 0
    total_execution_time: float = 0.0
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Retry information
    retry_count: int = 0
    max_retries: int = 3

    def add_subtask(self, subtask: SubTask):
        """Add a subtask."""
        self.subtasks.append(subtask)

    def get_subtask(self, task_id: str) -> Optional[SubTask]:
        """Get a subtask by ID."""
        return next((t for t in self.subtasks if t.id == task_id), None)

    def get_pending_subtasks(self) -> List[SubTask]:
        """Get all pending subtasks."""
        return [t for t in self.subtasks if t.status == TaskStatus.PENDING]

    def get_completed_subtasks(self) -> Set[str]:
        """Get IDs of all completed subtasks."""
        return {t.id for t in self.subtasks if t.status == TaskStatus.COMPLETE}

    def all_subtasks_complete(self) -> bool:
        """Check if all subtasks are complete."""
        return all(t.status == TaskStatus.COMPLETE for t in self.subtasks)

    def mark_complete(self, result: Any = None):
        """Mark task as complete."""
        self.status = TaskStatus.COMPLETE
        self.completed_at = datetime.now()
        self.result = result
        if self.started_at:
            self.total_execution_time = (
                self.completed_at - self.started_at
            ).total_seconds()

    def mark_failed(self, error: str):
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.error = error
        self.completed_at = datetime.now()

    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.retry_count < self.max_retries
