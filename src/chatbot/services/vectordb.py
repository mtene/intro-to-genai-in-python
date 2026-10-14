from typing import Any

from langchain_core.vectorstores import VectorStore

from chatbot.services.clients import build_in_memory_vector_store
from chatbot.services.embeddings import Embeddings


def VectorDB(**kwargs: Any) -> VectorStore:
    """In-process vector store for RAG (uses ``embeddings_config`` via ``Embeddings()``)."""
    return build_in_memory_vector_store(embedding=Embeddings(), **kwargs)
