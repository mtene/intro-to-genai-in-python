import logging
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from pydantic import SecretStr
from chatbot.config import config
from chatbot.services.authenticator import Authenticator

logger = logging.getLogger(__name__)


class RemoteEmbeddings(AzureOpenAIEmbeddings):
    """Represents a cloud-hosted OpenAI embeddings service
    Usage:
         embeddings_service = RemoteEmbeddings()
         text = "Hi"
         embeddings = embeddings_service.embed_query(text)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_embeddings_config()

        # establish connection to service
        super().__init__(
            api_key=SecretStr("dummy"),
            api_version=service_config["api_version"],
            model=service_config["model"],
            azure_deployment=service_config["model"],
            azure_endpoint=service_config["endpoint"],
            default_headers=service_config["extra_headers"],
            azure_ad_token_provider=Authenticator(
                service_config["authentication"]
            ).get_api_key,
            **kwargs,
        )
