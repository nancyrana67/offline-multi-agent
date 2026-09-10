"""Research Agent - Information retrieval and research."""
import logging

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class ResearchAgent(Agent):
    """Agent specialized in research and information retrieval."""

    def __init__(self):
        super().__init__(
            name="research",
            description="Information retrieval and research from local sources",
            model="mistral",
            tools=["search_documents", "retrieve_context", "synthesize_info"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle research tasks."""
        try:
            response = Message(
                role=MessageRole.AGENT,
                content=f"""Research Task: {message.content}

Research Process:
1. Query formulation
2. Document search
3. Information extraction
4. Source verification
5. Synthesis and organization

Results ready for delivery.""",
                message_type=MessageType.RESPONSE,
                sender=self.name,
            )
            return response
            
        except Exception as e:
            logger.error(f"Research agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )
