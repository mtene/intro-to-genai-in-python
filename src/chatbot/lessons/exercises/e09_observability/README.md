# Exercise 9: Observability

⏱️ **Estimated time**: 30 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Explain why observability is important in applications using LLMs
* Identify what kind of data can be observed from application telemetry
* Visualize telemetry traces as a timeline
* Drill down into individual prompts and inspect metadata

## Overview

In this exercise, you will start a telemetry endpoint which receives traces and displays them visually for inspection.

## Motivation

As your LLM‑powered application grows more complex, it becomes increasingly important to understand how it behaves internally. While observability is useful in any software system, it is especially critical for LLM‑powered applications dealing with:

* **Complex pipelines**: LLM apps frequently involve multiple dependent steps (retrieval, summarization, scoring, generation). Traces help identify which step contributes to latency or errors.

* **Prompt‑dependent behavior**: Small changes in prompts or context can produce drastically different outputs. Having a detailed record makes these issues reproducible.

* **Cost monitoring**: Token usage directly impacts cost. Observability helps catch spikes early, especially in production environments.

* **Model drift and upgrades**: LLM providers regularly update model versions. Observability detects regressions or changes in model behavior.

* **Debugging hallucinations**: Examining retrieved documents and prompt structure is often key to resolving hallucinations or irrelevant responses.

## Task description

Each chatbot implementation explored so far in the course has the capability to export OpenTelemetry traces to an external endpoint, given by the `observability_config` setting in [`config.yaml`](/src/config.yaml).

First, study the `Telemetry` class, defined in [`telemetry.py`](/chatbot/utils/telemetry.py) and observe its usage as a [context manager](https://www.pythontutorial.net/advanced-python/python-context-managers/) in the `__main__.py` file of any of the chatbot implementations:

```python
with Telemetry(service_name=Path(__file__).parent.name):
    console(ChatBot)
```

To collect and visualize traces in this exercise, we will use [Jaeger](https://www.jaegertracing.io/download), a popular open‑source distributed tracing system. You can either download and run the binary or use [`podman`](https://podman.io/) to start it in a container:

```powershell
podman run --rm --name jaeger -p 16686:16686 -p 4318:4318 cr.jaegertracing.io/jaegertracing/jaeger
```

Once Jaeger is running, start your chatbot, which will probe the observability endpoint and, if successful, show the following message at the console:

```powershell
INFO     Streaming traces to observability endpoint http://localhost:4318/v1/traces
```

In this setup, chatbot traces are streamed via HTTP requests to port `4318` on the local machine and can be visualized by navigating to [`http://localhost:16686/`](http://localhost:16686/). As an example, the screenshot below shows a trace produced by running the custom agent from the previous lesson.

![Trace visualization in Jaeger](/images/observability.png)

Each horizontal bar represents a span, corresponding to one operation in your application - such as constructing the prompt, retrieving documents, or calling the LLM. By selecting a span, you can inspect metadata such as:

* the full prompt and context sent to the model
* token usage (input/output)
* model configuration (temperature, max tokens, model version)
* intermediate operations such as retrieval, rewriting, filtering, or tool calls
* timing for each step in the process

This information is also available when errors occur and can be invaluable when debugging unexpected output, diagnosing latency spikes, or tracking down excessive token usage.

## Further reading

[Best LLM Observability Tools of 2025](https://www.comet.com/site/blog/llm-observability-tools/) is a comparison of different trace collection and visualization solutions.

It may also be instructive to study the [OpenTelemetry](https://opentelemetry.io/docs/) framework.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md)
---|---
