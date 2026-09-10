"""Agent orchestration and task management."""
import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from core.message import Message, MessageRole, MessageType, AgentStatus
from core.task import Task, TaskStatus, SubTask

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Orchestrates agent communication and task execution."""

    def __init__(self):
        self.agents: Dict[str, Any] = {}  # agent_name -> Agent instance
        self.active_tasks: Dict[str, Task] = {}  # task_id -> Task
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.agent_statuses: Dict[str, AgentStatus] = {}

    def register_agent(self, agent: Any):
        """Register an agent with the orchestrator."""
        self.agents[agent.name] = agent
        self.agent_statuses[agent.name] = agent.get_status()
        logger.info(f"Registered agent: {agent.name}")

    def unregister_agent(self, agent_name: str):
        """Unregister an agent."""
        if agent_name in self.agents:
            del self.agents[agent_name]
            del self.agent_statuses[agent_name]
            logger.info(f"Unregistered agent: {agent_name}")

    def get_agents(self) -> List[str]:
        """Get list of registered agent names."""
        return list(self.agents.keys())

    def get_agent(self, name: str) -> Optional[Any]:
        """Get an agent by name."""
        return self.agents.get(name)

    async def send_message(
        self,
        message: Message,
        recipient: str,
        timeout: int = 300,
    ) -> Optional[Message]:
        """Send a message to an agent and wait for response."""
        if recipient not in self.agents:
            logger.error(f"Agent not found: {recipient}")
            return None

        try:
            agent = self.agents[recipient]
            message.recipient = recipient
            response = await asyncio.wait_for(
                agent.process_message(message), timeout=timeout
            )
            return response
        except asyncio.TimeoutError:
            logger.error(f"Timeout waiting for response from {recipient}")
            return None
        except Exception as e:
            logger.error(f"Error sending message to {recipient}: {str(e)}")
            return None

    async def execute_task(
        self,
        task: Task,
        supervisor_name: str = "supervisor",
    ) -> Task:
        """Execute a task using the supervisor agent."""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        self.active_tasks[task.id] = task

        try:
            # Send task to supervisor
            task_message = Message(
                role=MessageRole.USER,
                content=task.user_request,
                message_type=MessageType.TASK,
                metadata={
                    "task_id": task.id,
                    "task_title": task.title,
                    "task_description": task.description,
                },
            )

            response = await self.send_message(
                task_message,
                supervisor_name,
                timeout=task.metadata.get("timeout", 300),
            )

            if response:
                task.mark_complete(result=response.content)
            else:
                task.mark_failed("No response from supervisor")

        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            task.mark_failed(str(e))
        finally:
            # Clean up
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]

        return task

    def get_agent_statuses(self) -> Dict[str, AgentStatus]:
        """Get status of all agents."""
        return {
            name: self.agents[name].get_status()
            for name in self.agents
        }

    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get status of a specific task."""
        return self.active_tasks.get(task_id)

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task."""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.status = TaskStatus.CANCELLED
            del self.active_tasks[task_id]
            return True
        return False

    def get_active_tasks(self) -> List[Task]:
        """Get all active tasks."""
        return list(self.active_tasks.values())
