from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from chatbot.config import config
from chatbot.services.clients import build_chat_model


def LLM(**kwargs: Any) -> BaseChatModel:
    """OpenAI-compatible chat model from ``llm_config`` (provider + deployment)."""
    llm_config = config.get_llm_config()
    model, connection = config.language_service_provider.resolve(
        llm_config, "llm_config"
    )
    return build_chat_model(model=model, connection=connection, **kwargs)
