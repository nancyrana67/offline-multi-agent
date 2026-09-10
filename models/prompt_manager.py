"""Prompt templates and management."""
import logging
from pathlib import Path
from typing import Dict

from config import PROMPTS_DIR

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages prompt templates."""

    def __init__(self):
        self.prompts: Dict[str, str] = {}
        self.load_prompts()

    def load_prompts(self):
        """Load all prompt files."""
        for prompt_file in PROMPTS_DIR.glob("*.txt"):
            name = prompt_file.stem
            try:
                with open(prompt_file, "r") as f:
                    self.prompts[name] = f.read()
            except Exception as e:
                logger.error(f"Error loading prompt {name}: {str(e)}")

    def get_prompt(self, name: str) -> str:
        """Get a prompt by name."""
        return self.prompts.get(name, "")

    def format_prompt(self, name: str, **kwargs) -> str:
        """Get and format a prompt."""
        prompt = self.get_prompt(name)
        if not prompt:
            return ""
        try:
            return prompt.format(**kwargs)
        except Exception as e:
            logger.error(f"Error formatting prompt: {str(e)}")
            return prompt

    def list_prompts(self) -> list:
        """List all prompts."""
        return list(self.prompts.keys())
