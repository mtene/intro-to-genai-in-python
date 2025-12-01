import logging
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr
from chatbot.config import config
from chatbot.services.authenticator import Authenticator

logger = logging.getLogger(__name__)


class RemoteLLM(AzureChatOpenAI):
    """Represents a cloud-hosted OpenAI LLM service
    Usage:
         llm_service = RemoteLLM()
         messages = [user_message(content="Hi")]
         answer = llm_service.invoke(messages)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_llm_config()

        # establish connection to service
        super().__init__(
            api_key=SecretStr("dummy"),
            api_version=service_config["api_version"],
            azure_deployment=service_config["model"],
            azure_endpoint=service_config["endpoint"],
            default_headers=service_config["extra_headers"],
            include_response_headers=True,
            azure_ad_token_provider=Authenticator(
                service_config["authentication"]
            ).get_api_key,
            **kwargs,
        )
