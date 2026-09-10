"""Embedding generation using Ollama."""
import logging
import aiohttp
from typing import List
import numpy as np

from config import OLLAMA_BASE_URL, EMBEDDING_MODEL

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generate embeddings using Ollama."""

    def __init__(self, model: str = None):
        self.model = model or EMBEDDING_MODEL
        self.cache = {}  # Simple cache for embeddings

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        # Check cache first
        if text in self.cache:
            return self.cache[text]

        try:
            async with aiohttp.ClientSession() as session:
                payload = {"model": self.model, "prompt": text}

                async with session.post(
                    f"{OLLAMA_BASE_URL}/api/embeddings",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        embedding = data.get("embedding", [])
                        self.cache[text] = embedding
                        return embedding
                    else:
                        logger.error(f"Embedding error: {resp.status}")
                        return []
        except Exception as e:
            logger.error(f"Embedding generation error: {str(e)}")
            return []

    async def generate_embeddings_batch(
        self, texts: List[str]
    ) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Similarity calculation error: {str(e)}")
            return 0.0
