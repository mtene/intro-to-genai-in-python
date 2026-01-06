import logging
import os
from typing import Dict
from chatbot.config import AuthenticationType

logger = logging.getLogger(__name__)


def _read_env_var(name: str, purpose: str) -> str:
    value = os.getenv(name) or ""
    if len(value) > 0:
        logger.debug(f"Successfully retrieved {purpose} from env var {name}")
    else:
        logger.error(f"Failed to retrieve {purpose} from env var {name}")
    return value


class Authenticator:
    """
    Provides API keys for language services.
    The value is static as retrieved from environment variables.
    Could be extended to use a token service instead.
    """

    def __init__(self, auth_config: Dict[str, str]):
        self._auth_config = auth_config

    def get_api_key(self) -> str:
        match self._auth_config["type"]:
            case AuthenticationType.ENV_VAR_SECRET:
                return _read_env_var(self._auth_config["env_var_name"], "API key")
            case _:
                raise NotImplementedError
