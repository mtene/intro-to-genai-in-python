# Exercise 7: Retrieval Augmented Generation

In this exercise, you will extend the query sent to the [chatbot](chatbot.py) with relevant information from a vector store.

## Motivation

Large Language Models (LLMs) have been trained on publicly-available data. However vast, this will still not be sufficient to accurately answer queries on highly-specialized domain-specific aspects. In order to bridge this gap, the query can be accompanied by relevant extracts from a curated corpus of knowledge stored in a database. This process is referred to Retrieval Augmented Generation (RAG).

## Vector stores and embeddings

![RAG process](/images/rag.png)

The relevance of the retrieved results is crucial to success. Since queries are expressed in natural language, the search should take linguistic and contextual aspects into account, rather than focus on specific keywords. Therefore, instead of traditional SQL databases, we will use vector stores which are able to perform semantic search. In order to do this, text needs to be transformed into a vector of floating-point numbers, corresponding to coordinates in a high-dimensional space, called embeddings. This representation allows computing relevance via linear algebra operations, such as distances or angles.

Embeddings are computed by models trained specifically for this purpose. Like LLMs, these models are distinguished by their number of parameters, context lengths and (CPU or GPU) hardware requirements. If their weights are made publicly available, orchestrators like Ollama or vLLM can be used to run them on local hardware. Proprietary models, such as those provided by OpenAI, are hosted in the cloud and accessed through endpoints after providing authentication credentials.

 **Embedding Model**                | **Active Params** | **Context Window** | **Embedding Dimension** | **Weights & Arch**       | **License**       | **Hardware Requirements** | **Ollama Catalog Name** |
---                                 |---                |---                 |---                      |---                       |---                |---                        |---                      |
 **Nomic Text Embedddings**         | 137M              | 8192               | 64 - 768                | Open / Open              | Apache 2.0        | CPU or GPU, ~0.3GB VRAM   | `nomic-embed-text`      |
 **Google Gemma Text Embeddings**   | 308M              | 2000               | 128 - 768               | Open / Open              | Apache 2.0-like   | CPU or GPU, ~0.6GB VRAM   | `embeddinggemma:300m`   |
 **OpenAI text-embedding-3-small**  | 350M              | 2048               | 512 - 1536              | Closed / Closed          | Proprietary       | Unknown                   | Cloud only              |
 **OpenAI text-embedding-3-large**  | 1000M             | 4096               | 256 - 3072              | Closed / Closed          | Proprietary       | Unknown                   | Cloud only              |
 **OpenAI text-embedding-ada-002**  | 1500M             | 4096               | 1536                    | Closed / Closed          | Proprietary       | Unknown                   | Cloud only              |

Notes:

* The context window size, given in tokens (1 token = ~4 characters), dictates how long the input text can be - this is why large texts have to be split into chunks, which are embedded individually.
* OpenAI's text-embedding-ada-002 is an older model, outperformed by all the others on benchmarks, including those with smaller size.
* Newer models support variable output dimension using Matryoshka Representation Learning (MRL).

Despite its small size, **Nomic Text Embedddings** scores highly on benchmarks, even outperforming **OpenAI text-embedding-3-small**. It is a great choice to run locally even on modest hardware.

A key operation when populating the database is splitting the content into chunks. The size of each chunk has to be small enough to fit in the context window of the embedding model, but also big enough to be useful when observed as stand-alone content. While the optimal chunking strategy varies by document and application, rules-of-thumb include splitting by paragraph, page or section.

## How do I do it?

Study the [`LocalVectorDB`](/src/chatbot/services/local_vectordb.py) class and notice that it is based on Meta's FAISS. Other options for local vector databases include ChromaDB and Milvus. Also notice the usage of the embeddings model, which will get called on each chunk ingested into the database, as well as on each user query before performing semantic search. The similarity metric is configurable - Euclidean and cosine distance being popular choices.

Your task is to read the target text document, split it into chunks using LangChain's [`RecursiveCharacterTextSplitter`](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter) and ingest them as a list of [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) into the vector store by calling `add_documents` with optional metadata that can e.g. identify the chunk number.

Semantic search is performed before inference, where the top 10 results, by relevance, are presented to the LLM via the system prompt:

```python
relevant_chunks = self._vectordb.similarity_search(question, k=10)
system_prompt = system_message(
    f"Respond to the user ONLY based on the following content:\n{'\n'.join(doc.page_content for doc in relevant_chunks)}"
)
```

## Further reading

Chunking, the distance metric used and result filtering are all essential for an effective RAG strategy. Each of these aspects have many subtleties that need to be refined for the dataset and application at hand.

By their nature, RAG systems always perform semantic search on the user query and send the results to the LLM. This might not be desirable when the user has a short follow-up remark such as "Try again with value 10" or "Thanks!", as the retrieved content will not be relevant and may bias the model towards hallucination. An alternative approach is to wrap the vector store into a tool. This can lead to the other extreme, where the model does not exercise the tool when it should have, which can be mitigated, in part, by adding explicit instructions to the system prompt.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e06_mcp/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s07_rag/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md)
---|---|---|---
