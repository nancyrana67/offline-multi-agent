"""Document Agent - Document analysis and processing."""
import logging

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class DocumentAgent(Agent):
    """Agent specialized in document processing and analysis."""

    def __init__(self):
        super().__init__(
            name="document",
            description="PDF, DOCX, and text document analysis",
            model="mistral",
            tools=["extract_text", "summarize", "extract_info", "compare_docs"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle document processing tasks."""
        try:
            response = Message(
                role=MessageRole.AGENT,
                content=f"""Document Processing: {message.content}

Supported Formats:
- PDF (.pdf)
- Word (.docx)
- Text (.txt)
- Markdown (.md)

Capabilities:
1. Text extraction
2. Summarization
3. Information extraction
4. Document comparison

Ready to process documents.""",
                message_type=MessageType.RESPONSE,
                sender=self.name,
            )
            return response
            
        except Exception as e:
            logger.error(f"Document agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )
