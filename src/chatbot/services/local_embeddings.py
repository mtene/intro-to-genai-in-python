from langchain_ollama import OllamaEmbeddings
from chatbot.config import config


class LocalEmbeddings(OllamaEmbeddings):
    """Represents a locally-hosted embeddings service orchestrated by Ollama
    Usage:
         embeddings_service = LocalEmbeddings()
         text = "Hi"
         embeddings = embeddings_service.embed_query(text)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_embeddings_config()

        # establish connection to service
        super().__init__(
            model=service_config["model"],
            base_url="http://127.0.0.1:11434",
            **kwargs,
        )
