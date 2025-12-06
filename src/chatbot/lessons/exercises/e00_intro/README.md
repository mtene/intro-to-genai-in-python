# Exercise 0: Introduction

⏱️ **Estimated time**: 10 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Navigate the project structure and understand the chatbot framework
* Run the Streamlit UI and command-line interfaces
* Understand the chatbot interface and how exercises are organized
* Use the `/test` command to validate chatbot implementations
* Choose an appropriate local LLM based on hardware requirements
* Distinguish between semi-open and fully-open models

## Overview

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

### Constructor

If the chatbot is supposed to hold any state that needs to be initialized, define a constructor. The constructor takes no arguments because any necessary configuration is retrieved from [`chatbot.config`](/src/chatbot/config.py).

```python
def __init__(self):
    pass
```

Store reusable services (like the LLM) as fields to avoid unnecessary repeated setup.

## Testing

Each exercise and solution includes an automated test suite that validates your implementation. To run tests, launch the console interface and use the `/test` command:

```powershell
uv run exercise-1

>>> /test
```

The test suite will evaluate your chatbot against predefined test cases, checking for expected keywords, response length, and other criteria. This provides immediate feedback on whether your implementation meets the requirements.

For comprehensive documentation on writing custom tests, understanding evaluation metrics, and best practices, see the [Testing Guide](/src/chatbot/testing/README.md).

## Choice of language model

This decision depends on the level of complexity in your application. Some guidelines are provided below.

### Remote LLMs

Remote LLMs are the most powerful models, typically hosted on cloud infrastructure. They require authentication (API keys, tokens, etc.) and come with billing and legal implications related to data IP.

To use remote LLMs:

1. Follow due process to obtain credentials
1. Update [`config.yaml`](/src/config.yaml) with the necessary details
1. Store secret values in user environment variables before starting the app

### Local LLMs

Local LLMs are smaller models ideal for experimentation. All models listed here have **open-sourced weights** (semi-open at minimum), enabling them to run entirely on your local machine without internet access.

Many models also have **open-sourced architecture** (fully-open), providing complete transparency into the model design. Both semi-open and fully-open models can typically be fine-tuned, either through standard tools (e.g. Unsloth) or vendor-provided SDKs.

Running local LLMs requires an orchestration framework, such as:

* Ollama: Easiest to get started with, supports many models via CLI and API.
* vLLM: Best for high-performance, multi-user, or server-based deployments.

Choose a model based on your application's required capabilities and available hardware (CPU or discrete GPU):

* **< 5B parameters**: designed for edge devices with limited resources (IoT, phones). Very responsive but often struggle with reasoning, have difficulty following instructions and produce more hallucinations.
* **5-8B parameters**: run reasonably well on consumer-grade laptops with discrete graphics cards.
* **8-15B parameters**: require more powerful workstation GPUs.
* **> 15B parameters**: require cluster-grade GPUs.

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

**Notes**:

* **MoE (Mixture-of-Experts)**: multiple specialized models in the bundle (explaining the large total parameter count), but only one is selected based on the query (active parameters).
* **Context window**: measured in tokens (1 token ≈ 4 characters). Dictates the maximum combined length of query, conversation history, system prompts and relevant background information.
* **Input modality**: refers to the type of input data the model accepts. All listed local models produce text-only output. Image generation is a separate topic beyond this tutorial's scope.
* **Emulated support**: the model lacks built-in machinery for structured outputs or tool calling but may comply with clear prompting instructions. This approach often requires custom response parsing since libraries like LangGraph or LlamaIndex typically don't offer support. No strong guarantees of compliance.
* **Native support**: the model has innate ability to understand JSON schema constraints (or similar mechanisms), with strong compliance guarantees.
* **Capabilities marked with `*`**: advertised by the vendor but unreliable in practice, likely due to training / fine-tuning approaches or small parameter counts.

To complete all tutorials, native support for both structured outputs and tool calling is needed. **IBM Granite 4 7B MoE** meets these criteria and is able to run at decently low latency on a consumer-grade laptop with a discrete GPU. Opt for **GPT-OSS 20B MoE** if your machine has better-than-average hardware.

🏠 [Overview](/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e01_prompting/README.md)
---|---
