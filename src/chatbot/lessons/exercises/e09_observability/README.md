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

Each horizontal bar represents a span, corresponding to one operation in your application - such as constructing the prompt, retrieving documents or calling the LLM. By selecting a span, you can inspect metadata such as:

* the full prompt and context sent to the model
* token usage (input/output)
* model configuration (temperature, max tokens, model version)
* intermediate operations such as retrieval, rewriting, filtering or tool calls
* timing for each step in the process

This information is also available when errors occur and can be invaluable when debugging unexpected output, diagnosing latency spikes or tracking down excessive token usage.

## Under the hood

The [`Telemetry`](src/chatbot/utils/telemetry.py:27-47) class takes a selective instrumentation approach, installing only the telemetry providers needed for the specific frameworks used in this codebase. This involves:

1. **Manual provider setup**: Creating an OpenTelemetry `TracerProvider` with a service name resource attribute that identifies the specific chatbot implementation being traced.

2. **OTLP HTTP exporter**: Using `OTLPSpanExporter` configured to send traces via HTTP to the observability endpoint. The exporter uses `BatchSpanProcessor` to efficiently batch spans before transmission, reducing network overhead.

3. **Targeted instrumentation**: Only instrumenting the libraries actually used in the application:

```python
LangchainInstrumentor().instrument()
OpenAIInstrumentor().instrument()
```

This approach requires manually selecting the specific instrumentation packages to be installed (e.g. `opentelemetry-instrumentation-langchain` and `opentelemetry-instrumentation-openai-v2`), but keeps the dependency tree minimal and gives explicit control over which frameworks are instrumented.

### Alternative: OpenLLMetry

[OpenLLMetry](https://github.com/traceloop/openllmetry) offers a simpler setup that automatically instruments multiple LLM frameworks and vector databases with minimal configuration. With OpenLLMetry, the `Telemetry` class could be simplified to:

```python
from traceloop.sdk import Traceloop

class Telemetry:
    def __init__(self, service_name: str):
        self._service_name = service_name
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        endpoint = config.get_observability_endpoint()
        if not is_endpoint_reachable(endpoint):
            return

        Traceloop.init(
            app_name=self._service_name,
            api_endpoint=endpoint
        )
        self._started = True

    def stop(self) -> None:
        # OpenLLMetry handles shutdown automatically
        pass
```

This single `Traceloop.init()` call automatically instruments LangChain, OpenAI and other supported frameworks without needing to install or invoke separate instrumentors.

The trade-off between these approaches centers on three aspects:

* **Convenience**: OpenLLMetry auto-detects frameworks and instruments them with a single call. The selective approach requires explicitly invoking each instrumentor.
* **Dependencies**: OpenLLMetry pulls instrumentation packages for numerous providers (Anthropic, Bedrock, Cohere, Pinecone, Qdrant and others), even if unused. The selective approach only installs what is needed.
* **Control**: The selective approach provides explicit visibility into which frameworks are instrumented. OpenLLMetry operates implicitly through auto-detection.

### How automatic instrumentation works

The instrumentors use OpenTelemetry's [monkey patching](https://en.wikipedia.org/wiki/Monkey_patch) technique to automatically wrap framework methods with tracing code. This means:

* No changes to application code are required beyond the initial `instrument()` call
* Spans are automatically created for LLM calls, embeddings, retrievals and other operations
* Context propagation happens automatically across async boundaries
* Token usage, prompts and responses are captured as span attributes

The instrumentation captures semantic conventions defined by the [OpenTelemetry Semantic Conventions for AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/), ensuring consistent attribute naming across different tracing implementations.

## Further reading

[Best LLM Observability Tools of 2025](https://www.comet.com/site/blog/llm-observability-tools/) is a comparison of different trace collection and visualization solutions.

It may also be instructive to study the [OpenTelemetry](https://opentelemetry.io/docs/) framework.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md)
---|---
