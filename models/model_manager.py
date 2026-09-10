"""Model management for Ollama."""
import logging
import aiohttp
from typing import List, Dict, Any, Optional

from config import OLLAMA_BASE_URL

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages Ollama models."""

    def __init__(self):
        self.models: List[Dict[str, Any]] = []
        self.current_model: Optional[str] = None

    async def list_models(self) -> List[Dict[str, Any]]:
        """List all available models."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{OLLAMA_BASE_URL}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.models = data.get("models", [])
                        return self.models
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
        return []

    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{OLLAMA_BASE_URL}/api/pull",
                    json={"name": model_name},
                    timeout=aiohttp.ClientTimeout(total=3600),
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            logger.error(f"Error pulling model: {str(e)}")
        return False

    def set_current_model(self, model_name: str):
        """Set the current model."""
        self.current_model = model_name

    def get_current_model(self) -> Optional[str]:
        """Get current model."""
        return self.current_model
