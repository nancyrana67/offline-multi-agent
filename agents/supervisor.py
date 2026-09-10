"""Supervisor Agent - Main orchestrator for task planning and delegation."""
import json
import logging
from typing import Any, Dict, List, Optional
import aiohttp

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType, ToolCall
from core.task import Task, SubTask, TaskStatus
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, TEMPERATURE

logger = logging.getLogger(__name__)


class SupervisorAgent(Agent):
    """Supervisor agent responsible for task planning and agent delegation."""

    def __init__(self):
        super().__init__(
            name="supervisor",
            description="Task planner and agent coordinator",
            model=DEFAULT_MODEL,
            tools=["plan_task", "delegate_task", "verify_result"],
        )
        self.subordinate_agents: List[str] = []

    def set_subordinate_agents(self, agents: List[str]):
        """Set the list of available agents for delegation."""
        self.subordinate_agents = agents

    async def handle_task(self, message: Message) -> Message:
        """Handle a task by creating a plan and delegating to agents."""
        user_request = message.content
        
        try:
            # Step 1: Create execution plan
            plan = await self._create_plan(user_request)
            self.status.progress = 0.3
            
            # Step 2: Analyze task and select agents
            task_analysis = await self._analyze_task(user_request, plan)
            selected_agents = task_analysis.get("agents", [])
            self.status.progress = 0.5
            
            # Step 3: Create subtasks
            subtasks = await self._create_subtasks(user_request, plan, selected_agents)
            self.status.progress = 0.6
            
            # Step 4: Create response with execution plan
            response_content = f"""Task Analysis Complete:

Execution Plan:
{plan}

Selected Agents: {', '.join(selected_agents)}

Subtasks Created: {len(subtasks)}

Ready to begin task execution."""
            
            response = Message(
                role=MessageRole.AGENT,
                content=response_content,
                message_type=MessageType.RESPONSE,
                sender=self.name,
                metadata={
                    "plan": plan,
                    "selected_agents": selected_agents,
                    "subtasks": len(subtasks),
                    "task_analysis": task_analysis,
                },
            )
            
            self.status.progress = 1.0
            return response
            
        except Exception as e:
            logger.error(f"Supervisor error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error processing task: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    async def _create_plan(self, task: str) -> str:
        """Create an execution plan for the task."""
        prompt = f"""You are a task planning expert. Create a detailed execution plan for this task:

Task: {task}

Provide a step-by-step plan that breaks down the task into logical steps."""
        
        return await self._call_ollama(prompt)

    async def _analyze_task(self, task: str, plan: str) -> Dict[str, Any]:
        """Analyze task and determine which agents to use."""
        available_agents_str = ", ".join(self.subordinate_agents)
        
        prompt = f"""You are a task analyzer. Analyze this task and recommend which agents should work on it.

Available Agents: {available_agents_str}

Task: {task}

Execution Plan: {plan}

Respond in JSON format:
{{
  "agents": ["agent1", "agent2"],
  "reasoning": "why these agents",
  "sequence": "execution order",
  "dependencies": {{}}
}}"""
        
        response = await self._call_ollama(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "agents": self.subordinate_agents[:3],
                "reasoning": response,
                "sequence": "parallel",
            }

    async def _create_subtasks(
        self, task: str, plan: str, agents: List[str]
    ) -> List[SubTask]:
        """Create subtasks from the plan."""
        prompt = f"""Break down this task into specific subtasks.

Task: {task}

Plan: {plan}

Available agents: {', '.join(agents)}

For each subtask, provide:
1. Subtask name
2. Description
3. Assigned agent
4. Dependencies (if any)

Format as JSON array."""
        
        response = await self._call_ollama(prompt)
        subtasks = []
        
        try:
            tasks_data = json.loads(response)
            for idx, task_data in enumerate(tasks_data):
                subtask = SubTask(
                    name=task_data.get("name", f"Subtask {idx+1}"),
                    description=task_data.get("description", ""),
                    assigned_agent=task_data.get("agent", agents[0] if agents else None),
                )
                subtasks.append(subtask)
        except:
            # Fallback: create simple subtasks
            for agent in agents[:3]:
                subtask = SubTask(
                    name=f"Task for {agent}",
                    description=f"Process task with {agent}",
                    assigned_agent=agent,
                )
                subtasks.append(subtask)
        
        return subtasks

    async def _call_ollama(self, prompt: str, model: str = None) -> str:
        """Call Ollama API to generate response."""
        model = model or self.model
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "temperature": TEMPERATURE,
                    "stream": False,
                }
                
                async with session.post(
                    f"{OLLAMA_BASE_URL}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "")
                    else:
                        logger.error(f"Ollama error: {resp.status}")
                        return ""
        except Exception as e:
            logger.error(f"Ollama connection error: {str(e)}")
            return ""
