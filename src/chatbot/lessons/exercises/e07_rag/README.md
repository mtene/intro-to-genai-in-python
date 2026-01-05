# Exercise 7: Retrieval Augmented Generation

⏱️ **Estimated time**: 35 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Understand the RAG (Retrieval Augmented Generation) pattern and its benefits
* Explain how vector embeddings enable semantic search
* Build and populate a vector store
* Implement document chunking and embedding strategies
* Integrate retrieved context into LLM prompts

## Overview

In this exercise, you will extend the query sent to the [chatbot](chatbot.py) with relevant information from a vector store.

Run the [tests](tests.py) in the console to track progress and extend them with your own. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## Motivation

Large Language Models (LLMs) have been trained on publicly-available data. However vast this training data may be, it will still not be sufficient to accurately answer queries on highly-specialized domain-specific aspects. In order to bridge this gap, the query can be accompanied by relevant extracts from a curated corpus of knowledge stored in a database. This process is referred to as Retrieval Augmented Generation (RAG).

## Vector stores and embeddings

![RAG process](/images/rag.png)

The relevance of retrieved results is crucial for RAG success. Since queries are expressed in natural language, search should consider linguistic and contextual aspects rather than just keywords. This is why we use **vector stores** for semantic search instead of traditional SQL databases.

Semantic search works by transforming text into **embeddings** - vectors of floating-point numbers representing coordinates in high-dimensional space. This representation enables computing relevance through linear algebra operations like distances and angles.

**Embedding models** are trained specifically to generate embeddings. Like LLMs, they vary by parameter count, context length and hardware requirements. Models with publicly available weights can run locally using orchestrators like Ollama or vLLM. Proprietary models (such as those from OpenAI) are cloud-hosted and accessed via authenticated endpoints.

 **Embedding Model**                | **Active Params** | **Context Window** | **Embedding Dimension** | **Weights & Arch**       | **License**       | **Hardware Requirements** | **Ollama Catalog Name**
---                                 |---                |---                 |---                      |---                       |---                |---                        |---
 **Nomic Text Embeddings**          | 137M              | 8192               | 64 - 768                | Open / Open              | Apache 2.0        | CPU or GPU, ~0.3GB VRAM   | `nomic-embed-text`
 **Snowflake Arctic Embeddings**    | 137M              | 2000               | 64 - 768                | Open / Open              | Apache 2.0        | CPU or GPU, ~0.3GB VRAM   | `snowflake-arctic-embed:m-long`
 **Google Gemma Text Embeddings**   | 308M              | 2000               | 128 - 768               | Open / Open              | Apache 2.0-like   | CPU or GPU, ~0.6GB VRAM   | `embeddinggemma:300m`
 **OpenAI text-embedding-3-small**  | 350M              | 2048               | 512 - 1536              | Closed / Closed          | Proprietary       | Unknown                   | Cloud only
 **OpenAI text-embedding-3-large**  | 1000M             | 4096               | 256 - 3072              | Closed / Closed          | Proprietary       | Unknown                   | Cloud only
 **OpenAI text-embedding-ada-002**  | 1500M             | 4096               | 1536                    | Closed / Closed          | Proprietary       | Unknown                   | Cloud only

Notes:

* The context window size, given in tokens (1 token = ~4 characters), dictates how long the input text can be - this is why large texts have to be split into chunks, which are embedded individually.
* OpenAI's text-embedding-ada-002 is an older model, outperformed by all the others on benchmarks, including those with smaller size.
* Newer models support variable output dimension using Matryoshka Representation Learning (MRL).

Despite its small size, **Snowflake Arctic Embeddings** scores highly on RAG benchmarks. It is a great choice to run locally even on modest hardware.

A key operation when populating the database is splitting the content into chunks. The size of each chunk has to be small enough to fit in the context window of the embedding model, but also big enough to be useful when observed as stand-alone content. While the optimal chunking strategy varies by document and application, rules-of-thumb include splitting by paragraph, page or section.

## How do I do it?

Study the [`LocalVectorDB`](/src/chatbot/services/local_vectordb.py) class and notice that it is based on the Chroma database. Other options for local vector databases include Milvus and Meta's FAISS. Also notice the usage of the embeddings model, which will get called on each chunk ingested into the database, as well as on each user query before performing semantic search. The similarity metric is configurable - Euclidean and cosine distance being popular choices.

Your task is to read the target text document, split it into chunks using LangChain's [`RecursiveCharacterTextSplitter`](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter) and ingest them as a list of [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) into the vector store by calling `add_documents` with optional metadata that can e.g. identify the chunk number.

Then, perform semantic search based on the query, retrieving the most relevant text chunks, and include them as part of the conversation passed to the LLM. You have the choice between storing them in a system prompt or augmenting the user query itself. It is generally best to avoid including RAG context in the conversation history, as that will increase its size unnecessarily and bias the LLM during future queries.

## Further reading

[RAG 101: Chunking Strategies](https://towardsdatascience.com/rag-101-chunking-strategies-fdc6f6c2aaec/) explores various chunking approaches including fixed-size, recursive, semantic and agentic strategies for optimizing retrieval accuracy.

[Comparing Similarity Searches: Distance Metrics in Vector Stores](https://medium.com/@stepkurniawan/comparing-similarity-searches-distance-metrics-in-vector-stores-rag-model-f0b3f7532d6f) explains the differences between cosine similarity, Euclidean distance and dot product, with guidance on choosing the right metric for your embeddings.

[Best Practices for RAG](https://medium.com/@marcharaoui/chapter-5-best-practices-for-rag-7770fce8ac81) covers result filtering, re-ranking strategies and techniques for improving retrieval quality in production systems.

[8 RAG Architectures You Should Know](https://humanloop.com/blog/rag-architectures) provides a comprehensive overview of different RAG patterns including naive RAG, agentic RAG with tool-wrapped retrieval, corrective RAG and multi-query approaches, with their respective trade-offs.

[RAG Evaluation: Best Practices and Metrics](https://www.evidentlyai.com/llm-guide/rag-evaluation) demonstrates how to measure RAG system performance using metrics like context precision, context recall, faithfulness and answer relevance.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e06_mcp/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s07_rag/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md)
---|---|---|---
