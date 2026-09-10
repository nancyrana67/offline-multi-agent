"""RAG Retriever combining document processing and vector search."""
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid

from config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RETRIEVAL, UPLOADS_DIR
from rag.document_processor import DocumentProcessor
from rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Retrieval-Augmented Generation retriever."""

    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore("documents")
        self.document_index = {}  # Document ID -> {name, path, chunks_count}

    async def index_document(
        self, file_path: str, doc_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Index a document for RAG."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return {"success": False, "error": "File not found"}

            if file_path.suffix.lower() not in self.document_processor.SUPPORTED_FORMATS:
                return {
                    "success": False,
                    "error": f"Unsupported format: {file_path.suffix}",
                }

            # Extract text
            text = self.document_processor.extract_text(str(file_path))
            if not text:
                return {"success": False, "error": "Could not extract text"}

            # Clean text
            text = self.document_processor.clean_text(text)

            # Chunk text
            chunks = self.document_processor.chunk_text(
                text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP
            )

            # Create document ID
            doc_id = str(uuid.uuid4())
            doc_name = doc_name or file_path.name

            # Add embeddings
            texts_to_embed = [
                (f"{doc_id}_chunk_{i}", chunk, {"doc_id": doc_id, "doc_name": doc_name, "chunk_index": i})
                for i, chunk in enumerate(chunks)
            ]

            count = await self.vector_store.add_embeddings_batch(texts_to_embed)

            # Store document info
            self.document_index[doc_id] = {
                "name": doc_name,
                "path": str(file_path),
                "chunks_count": len(chunks),
                "text_length": len(text),
                "format": file_path.suffix.lower(),
            }

            logger.info(f"Indexed {doc_name}: {count} chunks")
            return {
                "success": True,
                "doc_id": doc_id,
                "doc_name": doc_name,
                "chunks_count": count,
            }

        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}")
            return {"success": False, "error": str(e)}

    async def retrieve(
        self, query: str, top_k: int = TOP_K_RETRIEVAL
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks for a query."""
        try:
            results = await self.vector_store.search(query, top_k=top_k)
            retrieved = []

            for text_id, score, metadata in results:
                chunk_text = self.vector_store.embeddings.get(text_id, {}).get(
                    "text", ""
                )
                retrieved.append(
                    {
                        "text_id": text_id,
                        "content": chunk_text,
                        "score": score,
                        "document": metadata.get("doc_name"),
                        "chunk_index": metadata.get("chunk_index"),
                    }
                )

            return retrieved
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            return []

    def get_documents(self) -> List[Dict[str, Any]]:
        """Get all indexed documents."""
        return list(self.document_index.values())

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document and its embeddings."""
        try:
            if doc_id in self.document_index:
                # Delete all chunks for this document
                for text_id in list(self.vector_store.embeddings.keys()):
                    if text_id.startswith(f"{doc_id}_"):
                        self.vector_store.delete(text_id)

                del self.document_index[doc_id]
                self.vector_store.save_store()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics."""
        return {
            "documents_indexed": len(self.document_index),
            "vector_store": self.vector_store.get_stats(),
            "documents": self.document_index,
        }
