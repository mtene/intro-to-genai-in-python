import logging
import os
from typing import Dict
from chatbot.config import AuthenticationType

logger = logging.getLogger(__name__)


class Authenticator:
    """
    Provides API keys for language services.
    The value is static as retrieved from envirnoment variables.
    Could be extended to use a token service instead.
    """

    def __init__(self, auth_config: Dict[str, str]):
        self._auth_config = auth_config

    def get_api_key(self) -> str:
        match self._auth_config["type"]:
            case AuthenticationType.API_KEY:
                api_key = os.getenv(self._auth_config["api_key_env_var"]) or ""
                return api_key
            case _:
                raise NotImplementedError
