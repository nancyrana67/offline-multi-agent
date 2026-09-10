"""Math Agent - Mathematical reasoning and calculations."""
import logging
import math

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class MathAgent(Agent):
    """Agent specialized in mathematical reasoning."""

    def __init__(self):
        super().__init__(
            name="math",
            description="Mathematical reasoning and calculations",
            model="mistral",
            tools=["calculate", "solve_equation", "statistics"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle math problems."""
        try:
            response = Message(
                role=MessageRole.AGENT,
                content=f"""Math Problem: {message.content}

Math Capabilities:
1. Arithmetic operations
2. Algebra and equations
3. Statistics and probability
4. Calculus concepts
5. Geometry

Processing mathematical problem...""",
                message_type=MessageType.RESPONSE,
                sender=self.name,
            )
            return response
            
        except Exception as e:
            logger.error(f"Math agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )
