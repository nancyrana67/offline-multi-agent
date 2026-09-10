"""Presentation Agent - PPTX generation and presentation creation."""
import logging

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class PresentationAgent(Agent):
    """Agent specialized in presentation generation."""

    def __init__(self):
        super().__init__(
            name="presentation",
            description="Generate presentations and create PPTX files",
            model="mistral",
            tools=["create_presentation", "add_slide", "generate_content"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle presentation generation tasks."""
        try:
            response = Message(
                role=MessageRole.AGENT,
                content=f"""Presentation Generation: {message.content}

Presentation Pipeline:
1. Topic analysis
2. Outline creation
3. Slide generation
4. Content writing
5. Speaker notes
6. PPTX export

Generating presentation...""",
                message_type=MessageType.RESPONSE,
                sender=self.name,
            )
            return response
            
        except Exception as e:
            logger.error(f"Presentation agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )
