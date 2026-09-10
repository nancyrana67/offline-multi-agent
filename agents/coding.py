"""Coding Agent - Code generation, debugging, and explanation."""
import logging
import aiohttp
import json

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType, ToolCall
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, TEMPERATURE

logger = logging.getLogger(__name__)


class CodingAgent(Agent):
    """Agent specialized in code generation and debugging."""

    def __init__(self):
        super().__init__(
            name="coding",
            description="Code generation, debugging, and explanation",
            model="codellama",
            tools=["generate_code", "debug_code", "execute_code", "explain_code"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle coding tasks."""
        try:
            # Determine what kind of coding task
            task_type = await self._classify_task(message.content)
            
            if "generate" in task_type.lower():
                response_text = await self._generate_code(message.content)
            elif "debug" in task_type.lower():
                response_text = await self._debug_code(message.content)
            elif "explain" in task_type.lower():
                response_text = await self._explain_code(message.content)
            else:
                response_text = await self._generate_code(message.content)
            
            response = Message(
                role=MessageRole.AGENT,
                content=response_text,
                message_type=MessageType.RESPONSE,
                sender=self.name,
                metadata={"task_type": task_type},
            )
            return response
            
        except Exception as e:
            logger.error(f"Coding agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    async def _classify_task(self, task: str) -> str:
        """Classify the type of coding task."""
        keywords = {
            "generate": ["write", "create", "generate", "implement"],
            "debug": ["debug", "error", "fix", "problem"],
            "explain": ["explain", "understand", "how", "what"],
        }
        
        task_lower = task.lower()
        for task_type, keywords_list in keywords.items():
            if any(kw in task_lower for kw in keywords_list):
                return task_type
        return "generate"

    async def _generate_code(self, prompt: str) -> str:
        """Generate code using CodeLlama."""
        full_prompt = f"""You are an expert programmer. Generate clean, well-documented code.

Request: {prompt}

Provide the code with explanations."""
        
        return await self._call_ollama(full_prompt, model="codellama")

    async def _debug_code(self, prompt: str) -> str:
        """Debug code."""
        full_prompt = f"""You are an expert debugger. Analyze the following code/error and provide solutions.

Issue: {prompt}

Provide step-by-step debugging approach."""
        
        return await self._call_ollama(full_prompt)

    async def _explain_code(self, prompt: str) -> str:
        """Explain code."""
        full_prompt = f"""You are an expert code explainer. Explain the following in simple terms.

Code/Concept: {prompt}

Provide clear explanation with examples."""
        
        return await self._call_ollama(full_prompt)

    async def _call_ollama(self, prompt: str, model: str = None) -> str:
        """Call Ollama API."""
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
                        return f"Error: {resp.status}"
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            return f"Connection error: {str(e)}"
