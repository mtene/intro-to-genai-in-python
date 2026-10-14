"""Build LangChain chat, embedding, and vector-store clients."""

from typing import Any, override

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from pydantic import SecretStr

from chatbot.services.authenticator import Authenticator


def _base_url(connection: dict[str, Any]) -> str:
    endpoint = connection.get("endpoint")
    if not isinstance(endpoint, str) or not endpoint.strip():
        raise ValueError("provider connection must include endpoint")
    return endpoint.strip().rstrip("/")


def _api_key(connection: dict[str, Any]) -> Any:
    auth = connection.get("authentication")
    if auth is None:
        return SecretStr("ollama")
    return Authenticator(auth).get_api_key


def build_chat_model(
    *,
    model: str,
    connection: dict[str, Any],
    **kwargs: Any,
) -> BaseChatModel:
    return ChatOpenAI(
        model=model,
        base_url=_base_url(connection),
        api_key=_api_key(connection),
        default_headers=dict(connection.get("extra_headers") or {}),
        include_response_headers=connection.get("authentication") is not None,
        max_retries=3,
        **kwargs,
    )


def build_embeddings_model(
    *,
    model: str,
    connection: dict[str, Any],
    **kwargs: Any,
) -> Embeddings:
    return OpenAIEmbeddings(
        model=model,
        base_url=_base_url(connection),
        api_key=_api_key(connection),
        default_headers=dict(connection.get("extra_headers") or {}),
        max_retries=3,
        **kwargs,
    )


class InMemoryVectorDB(InMemoryVectorStore):
    """In-memory store; routes search through a retriever for LangChain telemetry spans."""

    def __init__(self, *, embedding: Embeddings, **kwargs: Any) -> None:
        super().__init__(embedding=embedding, **kwargs)
        self._retrieving = False

    @override
    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> list[Document]:
        if self._retrieving:
            return super().similarity_search(query, k=k, **kwargs)
        self._retrieving = True
        try:
            return self.as_retriever(search_kwargs={"k": k, **kwargs}).invoke(query)
        finally:
            self._retrieving = False


def build_in_memory_vector_store(
    *,
    embedding: Embeddings,
    **kwargs: Any,
) -> VectorStore:
    return InMemoryVectorDB(embedding=embedding, **kwargs)
