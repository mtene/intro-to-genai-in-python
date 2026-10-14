"""Build LangChain chat and embedding clients from provider connection dicts."""

from typing import Any

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
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
