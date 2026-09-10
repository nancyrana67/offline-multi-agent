"""Main application entry point for Offline Multi-Agent AI Workspace."""
import asyncio
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from core.orchestrator import AgentOrchestrator
from core.task import Task, TaskStatus
from core.message import Message, MessageRole, MessageType
from agents import (
    SupervisorAgent,
    ChatAgent,
    CodingAgent,
    DataAgent,
    WritingAgent,
    MemoryAgent,
    RAGAgent,
    CriticAgent,
)
from memory import ConversationMemory, LongTermMemory
from rag import RAGRetriever
from models import ModelManager, PromptManager
from tools import ToolManager, Calculator
from ui.pages import start_app
from config import (
    OLLAMA_BASE_URL,
    DEFAULT_MODEL,
    EMBEDDING_MODEL,
    DEBUG,
    DATA_DIR,
    UPLOADS_DIR,
    OUTPUTS_DIR,
)


class OfflineAIWorkspace:
    """Main application class."""

    def __init__(self):
        logger.info("Initializing Offline AI Workspace...")
        
        # Initialize core components
        self.orchestrator = AgentOrchestrator()
        self.memory = ConversationMemory()
        self.long_term_memory = LongTermMemory()
        self.rag = RAGRetriever()
        self.model_manager = ModelManager()
        self.prompt_manager = PromptManager()
        self.tool_manager = ToolManager()
        
        # Register tools
        self._register_tools()
        
        # Initialize agents
        self._init_agents()
        
        logger.info("Workspace initialized successfully")

    def _register_tools(self):
        """Register all available tools."""
        self.tool_manager.register_tool(
            name="calculator",
            description="Perform mathematical calculations",
            execute_fn=Calculator.evaluate,
            parameters={"expression": "string"},
        )
        logger.info("Tools registered")

    def _init_agents(self):
        """Initialize and register all agents."""
        agents = [
            SupervisorAgent(),
            ChatAgent(),
            CodingAgent(),
            DataAgent(),
            WritingAgent(),
            MemoryAgent(),
            RAGAgent(),
            CriticAgent(),
        ]
        
        for agent in agents:
            self.orchestrator.register_agent(agent)
            logger.info(f"Agent registered: {agent.name}")
        
        # Configure supervisor
        supervisor = self.orchestrator.get_agent("supervisor")
        if supervisor:
            supervisor.set_subordinate_agents([
                "chat", "coding", "data", "writing", "memory", "rag", "critic"
            ])

    async def process_user_request(self, request: str) -> str:
        """Process a user request through the multi-agent system."""
        logger.info(f"Processing request: {request[:50]}...")
        
        try:
            # Create task
            task = Task(
                title="User Request",
                description=request,
                user_request=request,
            )
            
            # Execute task
            result_task = await self.orchestrator.execute_task(task)
            
            # Store in memory
            if result_task.result:
                self.memory.add_message(Message(
                    role=MessageRole.USER,
                    content=request,
                    message_type=MessageType.TASK,
                ))
                self.memory.add_message(Message(
                    role=MessageRole.AGENT,
                    content=result_task.result,
                    message_type=MessageType.RESPONSE,
                ))
            
            return result_task.result or "Task completed"
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return f"Error: {str(e)}"

    def get_status(self) -> dict:
        """Get current system status."""
        return {
            "agents": self.orchestrator.get_agents(),
            "agent_statuses": {
                name: {
                    "status": status.status,
                    "progress": status.progress,
                }
                for name, status in self.orchestrator.get_agent_statuses().items()
            },
            "rag_stats": self.rag.get_stats(),
            "memory_stats": {
                "conversation_messages": len(self.memory.get_all()),
                "long_term_memories": len(self.long_term_memory.get_all()),
            },
        }


def main():
    """Main entry point."""
    logger.info("Starting Offline AI Workspace")
    logger.info(f"Ollama URL: {OLLAMA_BASE_URL}")
    logger.info(f"Default Model: {DEFAULT_MODEL}")
    logger.info(f"Embedding Model: {EMBEDDING_MODEL}")
    
    # Start the NiceGUI application
    start_app()


if __name__ == "__main__":
    main()
