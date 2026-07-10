import logging

from langchain_openai import ChatOpenAI

from chatbot.config import config
from chatbot.services.authenticator import Authenticator

logger = logging.getLogger(__name__)


class RemoteLLM(ChatOpenAI):
    """Represents a cloud-hosted OpenAI LLM service
    Usage:
         llm_service = RemoteLLM()
         messages = [user_message(content="Hi")]
         answer = llm_service.invoke(messages)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_llm_config()

        super().__init__(
            model=service_config["model"],
            base_url=service_config["endpoint"],
            api_key=Authenticator(service_config["authentication"]).get_api_key,
            default_headers=service_config.get("extra_headers") or {},
            include_response_headers=True,
            max_retries=3,
            **kwargs,
        )
