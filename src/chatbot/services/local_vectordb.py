import chromadb.config
from langchain_chroma import Chroma
from .embeddings import Embeddings
from chatbot.config import config, VectorDBSimilarityType


class LocalVectorDB(Chroma):
    """Represents a locally-hosted vector store which supports semantic search
    Usage:
         vectordb_service = LocalVectorDB()
         text = "Hi"
         results = vectordb_service.invoke(text)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_vectordb_config()

        # create embeddings service
        embeddings_service = Embeddings()

        # define index and distance
        match service_config["similarity"]:
            case VectorDBSimilarityType.EUCLIDEAN_DISTANCE:
                collection_metadata = {"hnsw:space": "l2"}
            case VectorDBSimilarityType.COSINE:
                collection_metadata = {"hnsw:space": "cosine"}
            case _:
                raise NotImplementedError

        # establish connection to service
        super().__init__(
            embedding_function=embeddings_service,
            collection_metadata=collection_metadata,
            client_settings=chromadb.config.Settings(anonymized_telemetry=False),
            **kwargs,
        )
