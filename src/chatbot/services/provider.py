"""Provider catalog and resolution of ``llm_config`` / ``embeddings_config``."""

from typing import Any


class LanguageServiceProvider:
    """Endpoints, auth, and deployments under ``providers`` in config."""

    def __init__(self, providers: dict[str, Any]) -> None:
        self._providers = providers

    @classmethod
    def from_config_data(cls, data: dict[str, Any]) -> "LanguageServiceProvider":
        block = data.get("providers")
        if not isinstance(block, dict):
            raise ValueError("config must include a providers mapping")
        return cls(block)

    def resolve(
        self, service_config: dict[str, Any], config_key: str
    ) -> tuple[str, dict[str, Any]]:
        """Model name and connection for a service config (provider + deployment)."""
        provider_id = service_config.get("provider")
        deployment_id = service_config.get("deployment")
        if not isinstance(provider_id, str) or not provider_id.strip():
            raise ValueError(f"{config_key} must include non-empty provider")
        if not isinstance(deployment_id, str) or not deployment_id.strip():
            raise ValueError(f"{config_key} must include non-empty deployment")
        provider_id = provider_id.strip()
        deployment_id = deployment_id.strip()
        model = self.deployment_model_name(provider_id, deployment_id)
        connection = self.connection(provider_id)
        return model, connection

    def connection(self, provider_id: str) -> dict[str, Any]:
        provider = self._providers.get(provider_id)
        if not isinstance(provider, dict):
            raise ValueError(f"unknown provider {provider_id!r}")
        endpoint = provider.get("endpoint")
        if not isinstance(endpoint, str) or not endpoint.strip():
            raise ValueError(f"providers.{provider_id} must include endpoint")
        connection: dict[str, Any] = {"endpoint": endpoint.strip()}
        if "extra_headers" in provider:
            connection["extra_headers"] = provider["extra_headers"]
        if "authentication" in provider:
            connection["authentication"] = provider["authentication"]
        return connection

    def deployment_model_name(self, provider_id: str, deployment_id: str) -> str:
        provider = self._providers.get(provider_id)
        if not isinstance(provider, dict):
            raise ValueError(f"unknown provider {provider_id!r}")
        deployments = provider.get("deployments")
        if not isinstance(deployments, dict):
            raise ValueError(f"providers.{provider_id} has no deployments")
        entry = deployments.get(deployment_id)
        if not isinstance(entry, dict):
            raise ValueError(
                f"providers.{provider_id}.deployments.{deployment_id} not defined"
            )
        name = entry.get("name", deployment_id)
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                f"providers.{provider_id}.deployments.{deployment_id}.name must be set"
            )
        return name.strip()
