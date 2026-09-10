"""Chat Agent - General conversation and explanations."""
import logging
import aiohttp

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, TEMPERATURE

logger = logging.getLogger(__name__)


class ChatAgent(Agent):
    """Chat agent for general conversation."""

    def __init__(self):
        super().__init__(
            name="chat",
            description="General conversation and explanations",
            model=DEFAULT_MODEL,
            tools=["search_memory", "retrieve_context"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle chat messages."""
        try:
            # Call Ollama for response
            response_text = await self._generate_response(message.content)
            
            response = Message(
                role=MessageRole.AGENT,
                content=response_text,
                message_type=MessageType.RESPONSE,
                sender=self.name,
            )
            return response
            
        except Exception as e:
            logger.error(f"Chat agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    async def _generate_response(self, prompt: str) -> str:
        """Generate response using Ollama."""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
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
                        return data.get("response", "No response generated")
                    else:
                        return f"API Error: {resp.status}"
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            return f"Connection error: {str(e)}"
