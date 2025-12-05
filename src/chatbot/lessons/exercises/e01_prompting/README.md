# Exercise 1: Text prompting

In this exercise, you will make the [chatbot logic](chatbot.py) use the LLM to answer user queries.

To achieve this, inspect the LLM classes in [`src/chatbot/services`](/src/chatbot/services) and the configuration file [`src/config.yaml`](/src/config.yaml). This configuration file allows you to choose which LLM is used and with what parameters.

## LLM selection

The language models used in the app need to be compatible with the [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create?api-mode=chat). Since this is the "industry standard", most model vendors will have implemented support.

For local LLMs, Ollama understands the OpenAI API and is able to translate requests back-and-forth for all models in their catalog.

## LLM authentication

Local LLMs require no authentication credentials. This explains the dummy value in the constructor of [`LocalLLM`](/src/chatbot/services/local_llm.py). It is there just because a non-empty string is expected by LangChain's `ChatOpenAI`, but the value is of no consequence.

For [`RemoteLLM`](/src/chatbot/services/remote_llm.py), authentication is done via a fixed secret key, to be configured via a user environment variable. Support for more advanced authentication mechanisms, such as token services, is out of scope as there is a wide range of possibilities, depending on corporate or application policies.

## Further reading

There are a few parameters which can be tuned to control the LLM's behavior during prompting:

* `temperature`, with a value between 0.0 and 2.0 (default: 1.0), controls the level of randomness in the output. Lower values (e.g., 0.2) make the model more focused and deterministic, while higher values (e.g., 0.9) make it more creative and diverse.
* `top_p`, with a value between 0.0 and 1.0 (default: 1.0), limits the model to sampling from the smallest set of tokens whose cumulative probability exceeds p. This helps balance diversity and relevance.
* `seed` is an integer value that controls the sequence of random choices made while generating the response

Setting `temperature` to `0.0` should ensure deterministic results. For positive values, a fixed `seed` value allows reproducing behavior as long as the same model and `api_version` are used, together with the same sequence of prompts.

Not all models expose the `seed` parameter. Others also provide a `top_k` parameter, which restricts sampling to the top k most likely tokens - this is not part of the [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create?api-mode=chat).

For more info see this [article](https://towardsai.net/p/machine-learning/understanding-llm-sampling-top-k-top-p-and-temperature). This [OpenAI post](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683) gives practical guidance on what values to use for different applications.

Also study the [`ChatOpenAI`](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html#langchain_openai.chat_models.base.ChatOpenAI) class in LangChain to understand the different ways LLMs can be configured and called.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e00_intro/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s01_prompting/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e02_system_prompt/README.md)
---|---|---|---
