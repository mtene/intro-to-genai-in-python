import yaml
from pathlib import Path
from enum import StrEnum
from typing import Any

from chatbot.services.provider import LanguageServiceProvider


class AuthenticationType(StrEnum):
    ENV_VAR_SECRET = "env_var_secret"


class ServiceType(StrEnum):
    LOCAL = "local"
    REMOTE = "remote"


class Config:
    def __init__(self) -> None:
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path, encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f)
        self._data = raw
        self.language_service_provider = LanguageServiceProvider.from_config_data(raw)
        self._vectordb_config: dict[str, Any] = raw["vectordb_config"]
        self._observability_config: dict[str, Any] = raw["observability_config"]
        self._log_level: str = raw["log_level"]

    def get_llm_config(self) -> dict[str, Any]:
        return self._data["llm_config"].copy()

    def get_embeddings_config(self) -> dict[str, Any]:
        return self._data["embeddings_config"].copy()

    def get_vectordb_type(self) -> ServiceType:
        return ServiceType(self._vectordb_config["type"])

    def get_vectordb_config(self) -> dict[str, Any]:
        return self._vectordb_config.copy()

    def get_observability_config(self) -> dict[str, Any]:
        return self._observability_config.copy()

    def get_log_level(self) -> str:
        return self._log_level


config = Config()
