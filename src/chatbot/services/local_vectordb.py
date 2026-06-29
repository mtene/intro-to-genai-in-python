from typing import Any

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from typing_extensions import override

from .embeddings import Embeddings


class LocalVectorDB(InMemoryVectorStore):
    """In-memory vector store for semantic search (cosine similarity via numpy)."""

    def __init__(self, **kwargs: Any):
        super().__init__(embedding=Embeddings(), **kwargs)
        # Reentrant call guard
        self._retrieving = False

    @override
    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> list[Document]:
        # Reentrant call guard
        if self._retrieving:
            return super().similarity_search(query, k=k, **kwargs)
        self._retrieving = True
        try:
            # Emits telemetry spans under LangchainInstrumentor
            return self.as_retriever(search_kwargs={"k": k, **kwargs}).invoke(query)
        finally:
            self._retrieving = False
