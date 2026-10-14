# Exercise: Text prompting

⏱️ **Estimated time**: 15 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Configure local and remote LLMs
* Prompt the LLM
* Understand how `temperature`, `top_p` and `seed` parameters affect outputs
* Explain the difference between deterministic and non-deterministic generation
* Apply appropriate parameter settings for different use cases

## Overview

In this exercise, you will make the [chatbot logic](chatbot.py) use the LLM to answer user queries.

To achieve this, inspect the LLM classes in [`src/chatbot/services`](/src/chatbot/services) and the configuration file [`src/config.yaml`](/src/config.yaml). This configuration file allows you to choose which LLM is used and with what parameters.


## LLM selection

The language models used in this app must be compatible with the [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create?api-mode=chat). Since this is the industry standard, most model vendors have implemented support.

For local LLMs, Ollama exposes an OpenAI-compatible API; the shipped `local_ollama` provider in [`config.yaml`](/src/config.yaml) points at it.

## LLM configuration

Local and remote models use the same layout in [`config.yaml`](/src/config.yaml):

* **`providers`** — each entry has an OpenAI-compatible `endpoint`, optional `extra_headers`, and optional `authentication` (API keys via [`Authenticator`](/src/chatbot/services/authenticator.py)).
* **`deployments`** — under each provider, a `name` is the model id sent to that endpoint.
* **`llm_config`** — `provider` and `deployment` select which entry to use.

The default local path uses `local_ollama` with no `authentication`. [`build_chat_model`](/src/chatbot/services/clients.py) supplies a placeholder API key anyway because LangChain's `ChatOpenAI` expects a non-empty string.

For a hosted model, add a provider (or copy the `remote_openai` pattern), add a deployment, and point `llm_config` at them.

## LLM behavior tuning

You can use the following parameters to control the LLM's behavior during prompting:

* **`temperature`** (0.0 - 2.0, default: 1.0): controls the shape of the probability distribution over tokens. Lower values sharpen the distribution, making high-probability tokens more dominant (focused, deterministic outputs). Higher values flatten the distribution, making all tokens more equally likely (creative, diverse outputs). At temperature 0, only the most likely token is selected. Theoretically, temperature can be any positive value - approaching infinity yields a uniform distribution - but OpenAI caps it at 2.0 for practical reasons.

![temperature effect](/images/temperature_effect.png)

* **`top_p`** (0.0 - 1.0, default: 1.0): filters the set of candidate tokens by cumulative probability. Only tokens whose cumulative probability mass sums to p or less are considered for sampling. This prunes low-probability tokens while preserving context-dependent flexibility: when the model is confident, fewer tokens are sampled; when uncertain, more options remain available.

![top_p effect](/images/top_p_effect.png)

* **`seed`** (positive integer): controls the sequence of random choices during response generation.

**Reproducibility**: setting `temperature` to `0.0` ensures deterministic results. With positive temperature values, a fixed `seed` enables reproducible behavior when using the same model, endpoint and prompt sequence.

**Note**: not all models expose the `seed` parameter. Some models provide a `top_k` parameter (restricting sampling to the top k most likely tokens), which is not part of the [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create?api-mode=chat) standard.

## Further reading

[Understanding LLM Sampling: Top-k, Top-p and Temperature](https://towardsai.net/p/machine-learning/understanding-llm-sampling-top-k-top-p-and-temperature) provides detailed explanations of how sampling parameters affect LLM output quality and randomness.

[Cheat Sheet: Mastering Temperature and Top-p in ChatGPT API](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683) offers practical guidance on choosing parameter values for different application types.

[ChatOpenAI API Reference](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html#langchain_openai.chat_models.base.ChatOpenAI) documents the LangChain class for configuring and calling OpenAI-compatible LLMs with various parameters.

---

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e00_intro/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s01_prompting/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e02_evals/README.md)
---|---|---|---
