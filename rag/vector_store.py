"""Vector store for RAG."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from config import DATA_DIR
from rag.embeddings import EmbeddingGenerator

logger = logging.getLogger(__name__)


class VectorStore:
    """Store and retrieve embeddings."""

    def __init__(self, store_name: str = "default"):
        self.store_name = store_name
        self.embeddings: Dict[str, Any] = {}  # text_id -> {text, embedding, metadata}
        self.store_path = DATA_DIR / f"store_{store_name}.json"
        self.embedding_generator = EmbeddingGenerator()
        self.load_store()

    def load_store(self):
        """Load vector store from disk."""
        try:
            if self.store_path.exists():
                with open(self.store_path, "r") as f:
                    self.embeddings = json.load(f)
                logger.info(f"Loaded {len(self.embeddings)} embeddings")
        except Exception as e:
            logger.error(f"Error loading store: {str(e)}")
            self.embeddings = {}

    def save_store(self):
        """Save vector store to disk."""
        try:
            with open(self.store_path, "w") as f:
                json.dump(self.embeddings, f)
            logger.info(f"Saved {len(self.embeddings)} embeddings")
        except Exception as e:
            logger.error(f"Error saving store: {str(e)}")

    async def add_embedding(
        self,
        text_id: str,
        text: str,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """Add text and its embedding to store."""
        try:
            embedding = await self.embedding_generator.generate_embedding(text)
            if not embedding:
                return False

            self.embeddings[text_id] = {
                "text": text,
                "embedding": embedding,
                "metadata": metadata or {},
                "added_at": datetime.now().isoformat(),
            }
            self.save_store()
            return True
        except Exception as e:
            logger.error(f"Error adding embedding: {str(e)}")
            return False

    async def add_embeddings_batch(
        self,
        texts: List[Tuple[str, str, Dict]],  # (text_id, text, metadata)
    ) -> int:
        """Add multiple embeddings."""
        count = 0
        for text_id, text, metadata in texts:
            if await self.add_embedding(text_id, text, metadata):
                count += 1
        return count

    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Tuple[str, float, Dict]]:
        """Search for similar embeddings."""
        try:
            query_embedding = await self.embedding_generator.generate_embedding(
                query
            )
            if not query_embedding:
                return []

            # Calculate similarities
            similarities = []
            for text_id, item in self.embeddings.items():
                similarity = EmbeddingGenerator.cosine_similarity(
                    query_embedding, item["embedding"]
                )
                similarities.append((text_id, similarity, item["metadata"]))

            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all embeddings."""
        return list(self.embeddings.values())

    def clear(self):
        """Clear the store."""
        self.embeddings = {}
        self.save_store()

    def delete(self, text_id: str) -> bool:
        """Delete an embedding."""
        if text_id in self.embeddings:
            del self.embeddings[text_id]
            self.save_store()
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        return {
            "total_embeddings": len(self.embeddings),
            "store_name": self.store_name,
            "store_path": str(self.store_path),
        }
