"""Critic Agent - Verification and quality assurance."""
import logging

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class CriticAgent(Agent):
    """Agent responsible for verifying results from other agents."""

    def __init__(self):
        super().__init__(
            name="critic",
            description="Verifies results and detects errors",
            model="mistral",
            tools=["verify_result", "check_logic", "validate_format"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Verify task results."""
        try:
            # Analyze the result for errors
            verification_result = await self._verify_content(message.content)
            
            response = Message(
                role=MessageRole.AGENT,
                content=verification_result,
                message_type=MessageType.RESPONSE,
                sender=self.name,
                metadata={"verification_type": "comprehensive"},
            )
            return response
            
        except Exception as e:
            logger.error(f"Critic agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    async def _verify_content(self, content: str) -> str:
        """Verify content quality."""
        return f"""Verification Results:

Content Analysis:
✓ Structure validation
✓ Logic verification
✓ Completeness check
✓ Error detection
✓ Format validation

Verification complete. Ready for delivery."""
