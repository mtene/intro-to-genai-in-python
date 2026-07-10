import logging

from langchain_openai.embeddings import OpenAIEmbeddings

from chatbot.config import config
from chatbot.services.authenticator import Authenticator

logger = logging.getLogger(__name__)


class RemoteEmbeddings(OpenAIEmbeddings):
    """Represents a cloud-hosted OpenAI embeddings service
    Usage:
         embeddings_service = RemoteEmbeddings()
         text = "Hi"
         embeddings = embeddings_service.embed_query(text)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_embeddings_config()

        super().__init__(
            model=service_config["model"],
            base_url=service_config["endpoint"],
            api_key=Authenticator(service_config["authentication"]).get_api_key,
            default_headers=service_config.get("extra_headers") or {},
            max_retries=3,
            **kwargs,
        )
