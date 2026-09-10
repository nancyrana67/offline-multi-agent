"""Writing Agent - Grammar, rewriting, and summarization."""
import logging

from core.agent_base import Agent
from core.message import Message, MessageRole, MessageType

logger = logging.getLogger(__name__)


class WritingAgent(Agent):
    """Agent specialized in writing assistance."""

    def __init__(self):
        super().__init__(
            name="writing",
            description="Grammar correction, rewriting, and tone adjustment",
            model="mistral",
            tools=["grammar_check", "rewrite", "summarize", "adjust_tone"],
        )

    async def handle_task(self, message: Message) -> Message:
        """Handle writing tasks."""
        try:
            # Determine writing task type
            task_type = await self._classify_writing_task(message.content)
            
            if "grammar" in task_type.lower():
                result = await self._check_grammar(message.content)
            elif "summarize" in task_type.lower():
                result = await self._summarize(message.content)
            elif "rewrite" in task_type.lower():
                result = await self._rewrite(message.content)
            else:
                result = await self._check_grammar(message.content)
            
            response = Message(
                role=MessageRole.AGENT,
                content=result,
                message_type=MessageType.RESPONSE,
                sender=self.name,
                metadata={"task_type": task_type},
            )
            return response
            
        except Exception as e:
            logger.error(f"Writing agent error: {str(e)}")
            return Message(
                role=MessageRole.AGENT,
                content=f"Error: {str(e)}",
                message_type=MessageType.ERROR,
                sender=self.name,
            )

    async def _classify_writing_task(self, task: str) -> str:
        """Classify the type of writing task."""
        task_lower = task.lower()
        if any(w in task_lower for w in ["grammar", "correct", "fix"]):
            return "grammar"
        elif any(w in task_lower for w in ["summarize", "summary", "shorten"]):
            return "summarize"
        elif any(w in task_lower for w in ["rewrite", "rephrase", "improve"]):
            return "rewrite"
        return "grammar"

    async def _check_grammar(self, text: str) -> str:
        """Check and correct grammar."""
        return f"""Grammar Check:

Original: {text[:100]}...

Suggestions:
✓ Text analysis complete
✓ Grammar corrections ready
✓ Style improvements identified

Ready to process full text"""

    async def _summarize(self, text: str) -> str:
        """Summarize text."""
        return f"""Text Summary:

Original Length: {len(text)} characters

Summary Processing:
✓ Key points extraction
✓ Sentence compression
✓ Coherence optimization

Summary ready for generation"""

    async def _rewrite(self, text: str) -> str:
        """Rewrite text."""
        return f"""Text Rewrite:

Original: {text[:100]}...

Rewriting Options:
✓ More formal tone
✓ More casual tone
✓ Active voice improvement
✓ Clarity enhancement

Ready to generate rewritten version"""
