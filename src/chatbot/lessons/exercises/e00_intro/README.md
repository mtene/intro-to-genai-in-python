# Exercise 0: Introduction

⏱️ **Estimated time:** 10 minutes

This is a basic setup to confirm that the UI and framework code are working as expected and get you familiar with the overall structure of the code.

The [chatbot logic](chatbot.py) for this exercise is just a dummy implementation that repeats the question back to the user after some waiting. The sleep delays may seem unnecessary, but they serve to demonstrate the status update notification feature.

## User interface

The graphical user interface is defined using [`streamlit`](https://docs.streamlit.io/get-started) in [`src/user_interface/app.py`](/src/user_interface/app.py). It consists of a basic conversation pane and a selector for choosing which chatbot implementation to use.

![Chat UI](/images/ui.png)

The chatbot defined in each exercise or solution can also be tested at the command-line, by issuing the following launch commands:

```powershell
uv run exercise-5
```

or

```powershell
uv run solution-5
```

This allows you to attach a debugger and step through the code or capture exceptions.

## Chatbot

All chatbot implementations inherit from the common interface [`BaseChatBot`](/src/chatbot/chatbot_base.py), with their specific behavior defined in `src/chatbot/lessons/*/chatbot.py`. The core `get_answer` method receives the user question as a string and returns the assistant's answer as a string.

```python
@override
def get_answer(self, question: str, ctx: ChatContext) -> str:
    pass
```

The `ctx` argument does not affect the chatbot's behavior. It is used solely for displaying progress updates to the UI.

If the chatbot holds any state that needs to be initialized, then a constructor should be defined. It is assumed to take no arguments, since any necessary configuration is retrieved from [`chatbot.config`](/src/chatbot/config.py).

```python
def __init__(self):
    pass
```

Storing reusable services, like the LLM, as fields is a good idea to avoid unnecessary repeated setup.

## Choice of language model

This decision depends on the level of complexity in your application. Some guidelines are provided below.

### Remote LLMs

These are the most powerful models, typically hosted on cloud infrastructure. Authentication is needed to access them (API key, tokens, etc.) and there are associated billing and legal / data IP implications.

If you decide to use them, first follow due process to obtain credentials, then update [`config.yaml`](/src/config.yaml) with the necessary details and store any secret values in user environment variables before starting the app.

### Local LLMs

Local LLMs are smaller and ideal for experimentation. These models have open-sourced weights (semi-open) and sometimes open-sourced architecture (fully-open), allowing them to run entirely on your local machine without accessing the internet.
To run them, you need an orchestration framework, for example:

* Ollama: Easiest to get started with, supports many models via CLI and API.
* vLLM: Best for high-performance, multi-user, or server-based deployments.

Choose the model based on the required capabilities of your application and available hardware (CPU or discrete GPU). As a rule of thumb, models with less than 5B parameters are meant for edge devices with limited resources (IoT, phones). They are very responsive but often struggle with reasoning, having difficulty following instructions and a higher probability of producing hallucinated answers. Models between 5-8B will run reasonably well on consumer-grade laptops with discrete graphics cards. Models between 8-15B need more powerful workstation GPUs, while sizes above 15B require cluster-grade GPUs.

Some options are given below, in ascending order of hardware requirements. You can use them by pasting the Ollama catalog name in the `local_llm` settings from [`config.yaml`](/src/config.yaml).

Model                           | Active Params | Context Window | Input modality  | Structured Output   | Tool Calling  | Weights & Arch     | License           | Hardware Requirements  | Ollama Catalog Name
---                             |---            |---             |---              |---                  |---            |---                 |---                |---                     |---
**Google Gemma 3 0.27B**        | 0.27B         | 32K            | Text-only       | Emulated            | Emulated      | Open / Open        | Apache 2.0-like   | CPU or GPU, 0.5GB VRAM | `gemma3:270m`
**IBM Granite 4 0.35B**         | 0.35B         | 1000K          | Text-only       | Native              | Native        | Open / Open        | Apache 2.0        | CPU or GPU, 0.8GB VRAM | `granite4:350m-h`
**Google Gemma 3 1B**           | 1B            | 32K            | Text-only       | Emulated            | Emulated      | Open / Open        | Apache 2.0-like   | CPU or GPU, 1GB VRAM   | `gemma3:1b`
**IBM Granite 4 1B**            | 1B            | 1000K          | Text-only       | Native              | Native        | Open / Open        | Apache 2.0        | CPU or GPU, 1.8GB VRAM | `granite4:1b-h`
**Microsoft Phi-4 Mini 3.8B**   | 3.84B         | 128K           | Text-only       | Native\*            | Native\*      | Open / Open        | MIT               | CPU or GPU, 2.5GB VRAM | `phi4-mini:3.8b`
**IBM Granite 4 3B**            | 3B            | 1000K          | Text-only       | Native              | Native        | Open / Open        | Apache 2.0        | CPU or GPU, 3.8GB VRAM | `granite4:3b-h`
**IBM Granite 4 7B MoE**        | 1B            | 1000K          | Text-only       | Native              | Native        | Open / Open        | Apache 2.0        | GPU, 4.2GB VRAM        | `granite4:7b-a1b-h`
**Mistral 0.3 7B**              | 7B            | 32K            | Text-only       | Native              | Native        | Open / Open        | Apache 2.0        | GPU, 4.5GB VRAM        | `mistral:7b`
**Meta LLaMA 3.1 8B**           | 8B            | 128K           | Text-only       | Native              | Native        | Open / Open        | Community license | GPU, 5GB VRAM          | `llama3.1:8b`
**OpenAI GPT-OSS 20B MoE**      | 3.6B          | 128K           | Text-only       | Native              | Native        | Open / Closed      | Apache 2.0        | GPU, 14GB VRAM         | `gpt-oss:20b`
**Mistral Small 3.2 24B**       | 24B           | 128K           | Text, Images    | Native              | Native        | Open / Open        | Apache 2.0        | GPU, 15GB VRAM         | `mistral-small3.2:24b`
**IBM Granite 4 32B MoE**       | 9B            | 1000K          | Text-only       | Native              | Native        | Open / Open        | Apache 2.0        | GPU, 19GB VRAM         | `granite4:32b-a9b-h`
**OpenAI GPT-OSS 120B MoE**     | 5.1B          | 128K           | Text-only       | Native              | Native        | Open / Closed      | Apache 2.0        | GPU, 65GB VRAM         | `gpt-oss:120b`

Notes:

* `MoE` stands for mixture-of-experts, meaning that there are multiple specialized models in the bundle (hence the large number of total parameters), but only one of them is selected based on the query (active parameters).
* The context window size, given in tokens (1 token = ~4 characters), dictates how long the query plus any associated info, such as conversation history, system prompts or relevant background, can be supplied to the model.
* Technically, modality is specified separately for the LLM input and output. Here, we explicitly refer to the type of input data, since all the listed local models are text-only on the output. Generating images is a whole different topic, out of scope here.
* Emulated support for a capability (structured outputs or tool calling) means that the model does not have built-in machinery for the feature, but may comply if clear instructions are included while prompting. However, this approach often requires custom code to parse the response, since libraries like LangGraph or LlamaIndex do not usually offer support, plus there are no strong guarantees that the model will comply.
* Native support means that the model has innate ability to understand the constraints described in the prescribed JSON schema (or similar mechanism), with a strong guarantee to comply.
* Model capabilities marked with `*` match what was advertised by the vendor, but practical testing shows they are unreliable, probably due to the way the model was trained / fine-tuned or the small number of parameters.

To complete all tutorials, native support for both structured outputs and tool calling is needed. **IBM Granite 4 7B MoE** meets these criteria and is able to run at decently low latency on a consumer-grade laptop with a discrete GPU. Opt for **GPT-OSS 20B MoE** if your machine has better-than-average hardware.

🏠 [Overview](/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e01_prompting/README.md)
---|---
