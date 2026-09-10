"""RAG Agent - Retrieval-Augmented Generation for document queries."""
import logging

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class RAGAgent(Agent):
    """Agent for RAG operations and document retrieval."""

    def __init__(self):
        super().__init__(
            name="rag",
            description="Document retrieval and augmented generation",
            model="mistral",
            tools=["search_documents", "retrieve_chunks", "generate_from_context"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle RAG queries."""
        try:
            # Search documents for relevant information
            retrieved_docs = await self._search_documents(message.content)
            
            response = Message(
                role=MessageRole.AGENT,
                content=f"""RAG Query Results:

Query: {message.content}

Documents Retrieved: {len(retrieved_docs)}

Relevant context extracted and ready for generation.""",
                message_type=MessageType.RESPONSE,
                sender=self.name,
                metadata={"documents_found": len(retrieved_docs)},
            )
            return response
            
        except Exception as e:
            logger.error(f"RAG agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    async def _search_documents(self, query: str) -> list:
        """Search indexed documents."""
        # This will be integrated with the vector store
        return []
