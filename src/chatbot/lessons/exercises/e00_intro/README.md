# Exercise: Introduction

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

Start it from the project root with:

```powershell
uv run genai-chat
```

![Chat UI](/images/ui.png)

The chatbot defined in each exercise or solution can also be tested at the command-line:

```powershell
uv run exercise-1
```

or

```powershell
uv run solution-1
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

Finally, override the `reset` method to clear any state for repeatable testing purposes.

```python
@override
def reset(self):
    pass
```

## Testing

Lessons with a `tests.py` file define example inputs and criteria for assessing chatbot responses. Run `/test` in the console to execute that lesson's tests and review the results:

```powershell
uv run exercise-2

>>> /test
```

## Choice of language model

This decision depends on the level of complexity in your application. Some guidelines are provided below.

### Remote LLMs

Remote LLMs are the most powerful models, typically hosted on cloud infrastructure. They require authentication (API keys, tokens, etc.) and come with billing and legal implications related to data IP. Remote services are accessed through an OpenAI-compatible API endpoint configured in [`config.yaml`](/src/config.yaml).

To use remote LLMs:

1. Follow due process to obtain credentials
1. Update [`config.yaml`](/src/config.yaml) with the necessary details
1. Store credentials in user environment variables before starting the app

### Local LLMs

Local LLMs are smaller models ideal for experimentation. All models listed here have **open-sourced weights** (semi-open at minimum), enabling them to run entirely on your local machine without internet access.

Many models also have **open-sourced architecture** (fully-open), providing complete transparency into the model design. Both semi-open and fully-open models can typically be fine-tuned, either through standard tools (e.g. Unsloth) or vendor-provided SDKs.

Running local LLMs requires an orchestration framework, such as:

* Ollama: Easiest to get started with, supports many models via CLI and API.
* vLLM: Best for high-performance, multi-user or server-based deployments.

Choose a model based on your application's required capabilities and available hardware (CPU or discrete GPU):

* **Edge**: very small models for CPUs, integrated graphics, or tight VRAM (roughly up to ~5B active parameters). Fast and cheap to run; weaker at reasoning, instruction following, and agents.
* **Laptop**: consumer laptops with a discrete GPU (often 6–12 GB VRAM). The usual sweet spot for local experimentation.
* **Workstation**: a single high-end GPU (often 16–24 GB VRAM) or a desktop with one large card.
* **Cluster**: datacenter or multi-GPU setups (very large dense models, or MoE bundles that still need tens of gigabytes of VRAM).

Four tables below use the same columns; rows are sorted by ascending hardware within each tier. To use a different local model, add a deployment entry to [`config.yaml`](/src/config.yaml) under `providers.local_ollama.deployments` (use a human-readable key and set `name` to the Ollama catalog name from the table) then make `llm_config.deployment` use the corresponding key.

#### Edge

Runs on CPUs, integrated graphics, or a few gigabytes of VRAM — think phones, IoT, and low-power devices where latency and footprint matter more than reasoning depth.

| Model | Active Params | Context Window | Input modality | Structured Output | Tool Calling | Weights & Arch | License | Hardware Requirements | Ollama Catalog Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **IBM Granite 4 0.35B** | 0.35B | 1000K | Text-only | Native | Native | Open / Open | Apache 2.0 | CPU or GPU, 0.8GB VRAM | `granite4:350m-h` |
| **IBM Granite 4 1B** | 1B | 1000K | Text-only | Native | Native | Open / Open | Apache 2.0 | CPU or GPU, 1.8GB VRAM | `granite4:1b-h` |
| **Google Gemma 4 E2B** | 2.3B | 128K | Text, Image, Audio | Native | Native | Open / Open | Gemma license | CPU or GPU, 2GB VRAM | `gemma4:e2b` |
| **Microsoft Phi-4 Mini 3.8B** | 3.84B | 128K | Text-only | Native\* | Native\* | Open / Open | MIT | CPU or GPU, 2.5GB VRAM | `phi4-mini:3.8b` |
| **IBM Granite 4.2 3B** | 3B | 128K | Text-only | Native | Native | Open / Open | Apache 2.0 | CPU or GPU, ~3GB VRAM | `granite4.2:3b` |
| **Alibaba Qwen 3.5 4B** | 4B | 256K | Text, Image | Native | Native | Open / Open | Apache 2.0 | CPU or GPU, ~4GB VRAM | `qwen3.5:4b` |
| **Google Gemma 4 E4B** | 4.5B | 128K | Text, Image, Audio | Native | Native | Open / Open | Gemma license | CPU or GPU, 4GB VRAM | `gemma4:e4b` |

#### Laptop

Targets a single discrete GPU in a portable PC (often 8-16 GB VRAM): large enough for useful chat and agents, still realistic on a consumer gaming or prosumer laptop.

| Model | Active Params | Context Window | Input modality | Structured Output | Tool Calling | Weights & Arch | License | Hardware Requirements | Ollama Catalog Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **IBM Granite 4.2 8B** | 8B | 128K | Text-only | Native | Native | Open / Open | Apache 2.0 | GPU, ~5.3GB VRAM | `granite4.2:8b` |
| **Meta LLaMA 3.1 8B** | 8B | 128K | Text-only | Native | Native | Open / Open | Community license | GPU, 5GB VRAM | `llama3.1:8b` |
| **Mistral Ministral 3 8B** | 8B | 256K | Text, Image | Native | Native | Open / Open | Apache 2.0 | GPU, ~6GB VRAM | `ministral-3:8b` |
| **Alibaba Qwen 3.5 9B** | 9B | 256K | Text, Image | Native | Native | Open / Open | Apache 2.0 | GPU, ~8GB VRAM | `qwen3.5:9b` |
| **Google Gemma 4 12B** | 12B | 256K | Text, Image | Native | Native | Open / Open | Gemma license | GPU, 8GB VRAM | `gemma4:12b` |

#### Workstation

Assumes one high-end desktop GPU (commonly 16–24 GB VRAM) so you can load bigger dense models or MoE packages that fit on a single card.

| Model | Active Params | Context Window | Input modality | Structured Output | Tool Calling | Weights & Arch | License | Hardware Requirements | Ollama Catalog Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **OpenAI GPT-OSS 20B MoE** | 3.6B | 128K | Text-only | Native | Native | Open / Closed | Apache 2.0 | GPU, 14GB VRAM | `gpt-oss:20b` |
| **Mistral Small 3.2 24B** | 24B | 128K | Text, Images | Native | Native | Open / Open | Apache 2.0 | GPU, 15GB VRAM | `mistral-small3.2:24b` |
| **Google Gemma 4 26B MoE** | 3.8B | 256K | Text, Image | Native | Native | Open / Open | Gemma license | GPU, 17GB VRAM | `gemma4:26b` |
| **Alibaba Qwen 3.8 27B** | 27B | 256K | Text, Image | Native | Native | Open / Open | Apache 2.0 | GPU, ~18GB VRAM | `qwen3.8:27b` |
| **IBM Granite 4.2 30B** | 30B | 128K | Text-only | Native | Native | Open / Open | Apache 2.0 | GPU, ~18GB VRAM | `granite4.2:30b` |
| **Google Gemma 4 31B** | 31B | 256K | Text, Image | Native | Native | Open / Open | Gemma license | GPU, 20GB VRAM | `gemma4:31b` |

#### Cluster

Needs datacenter-scale memory or several GPUs working together — weights and long-context cache exceed what one consumer card can provide.

| Model | Active Params | Context Window | Input modality | Structured Output | Tool Calling | Weights & Arch | License | Hardware Requirements | Ollama Catalog Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **OpenAI GPT-OSS 120B MoE** | 5.1B | 128K | Text-only | Native | Native | Open / Closed | Apache 2.0 | GPU, 65GB VRAM | `gpt-oss:120b` |
| **Alibaba Qwen 3.5 122B** | 122B | 256K | Text, Image | Native | Native | Open / Open | Apache 2.0 | GPU, ~81GB VRAM | `qwen3.5:122b` |


**Notes**:

* **MoE (Mixture-of-Experts)**: multiple specialized models in the bundle (explaining the large total parameter count), but only one is selected based on the query (active parameters).
* **Context window**: measured in tokens (1 token ≈ 4 characters). Dictates the maximum combined length of query, conversation history, system prompts and relevant background information.
* **Input modality**: refers to the type of input data the model accepts. All listed local models produce text-only output. Image generation is a separate topic beyond this tutorial's scope.
* **Emulated support**: the model lacks built-in machinery for structured outputs or tool calling but may comply with clear prompting instructions. This approach often requires custom response parsing since libraries like LangGraph or LlamaIndex typically don't offer support. No strong guarantees of compliance.
* **Native support**: the model has innate ability to understand JSON schema constraints (or similar mechanisms), with strong compliance guarantees.
* **Capabilities marked with `*`**: advertised by the vendor but unreliable in practice, likely due to training / fine-tuning approaches or small parameter counts.

To complete all tutorials, native support for both structured outputs and tool calling is needed. **IBM Granite 4.2 8B** meets these criteria and is able to run at decently low latency on a consumer-grade laptop with a discrete GPU. Opt for **OpenAI GPT-OSS 20B MoE** if your machine has better-than-average hardware.

## A note on sync vs async programming

**Synchronous code** runs one step at a time. When the program executes a network call (like asking an LLM) or accesses a disk, it stops and waits for the response before continuing. This is simple but wasteful, as the process sits idle while waiting.

```python
# Synchronous: waits for each call to finish
def get_info():
    result1 = call_llm("What's the weather?")
    result2 = call_llm("What's the time?")  # starts only after result1
    return f"{result1}\n{result2}
```

**Asynchronous code** lets your program do other work while waiting. It uses an event loop to handle multiple requests concurrently.

```python
# Asynchronous: can run both calls "at the same time"
async def get_info():
    result1 = await call_llm_async("What's the weather?")
    result2 = await call_llm_async("What's the time?")
    return f"{result1}\n{result2}
```

For simplicity, this tutorial uses synchronous code. Most modern Python libraries have both sync and async versions of essential calls. Some of them (like MCP and A2A) are purely asynchronous, so we created wrapper utilities to bridge them to sync code.

Even though async is out of scope here, it's essential for production applications. To learn more, see [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/).

## Further reading

[AI Engineering Pitfalls](https://huyenchip.com/2025/01/16/ai-engineering-pitfalls.html) discusses the thought process behind deciding if GenAI is the right fit for an application, covering common pitfalls and when to avoid LLM-based solutions.

---

🏠 [Overview](/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e01_prompting/README.md)
---|---
