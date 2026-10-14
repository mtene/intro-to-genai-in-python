from typing import Any

from langchain_core.embeddings import Embeddings as EmbeddingsModel

from chatbot.config import config
from chatbot.services.clients import build_embeddings_model


def Embeddings(**kwargs: Any) -> EmbeddingsModel:
    """OpenAI-compatible embeddings from ``embeddings_config`` (provider + deployment)."""
    embeddings_config = config.get_embeddings_config()
    model, connection = config.language_service_provider.resolve(
        embeddings_config, "embeddings_config"
    )
    return build_embeddings_model(model=model, connection=connection, **kwargs)
