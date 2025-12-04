import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.docstore.in_memory import InMemoryDocstore
from .embeddings import Embeddings
from chatbot.config import config, VectorDBSimilarityType


class LocalVectorDB(FAISS):
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
        embeddings_size = len(embeddings_service.embed_query("dummy"))
        match service_config["similarity"]:
            case VectorDBSimilarityType.EUCLIDEAN_DISTANCE:
                index = faiss.IndexFlatL2(embeddings_size)
                distance_strategy = DistanceStrategy.EUCLIDEAN_DISTANCE
            case VectorDBSimilarityType.COSINE:
                index = faiss.IndexFlatIP(embeddings_size)
                distance_strategy = DistanceStrategy.COSINE
            case _:
                raise NotImplementedError

        # establish connection to service
        super().__init__(
            embedding_function=embeddings_service,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
            distance_strategy=distance_strategy,
            **kwargs,
        )
