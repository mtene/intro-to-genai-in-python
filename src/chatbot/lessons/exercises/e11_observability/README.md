# Exercise: Observability

⏱️ **Estimated time**: 30 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Explain why observability is important in applications using LLMs
* Identify what kind of data can be observed from application telemetry
* Browse telemetry traces and inspect prompts, metadata, and cost

## Overview

In this exercise, you will connect your chatbot to an observability backend that receives traces and lets you inspect them in a UI.

## Motivation

As your LLM‑powered application grows more complex, it becomes increasingly important to understand how it behaves internally. While observability is useful in any software system, it is especially critical for LLM‑powered applications dealing with:

* **Complex pipelines**: LLM apps frequently involve multiple dependent steps (retrieval, summarization, scoring, generation). Traces help identify which step contributes to latency or errors.

* **Prompt‑dependent behavior**: Small changes in prompts or context can produce drastically different outputs. Having a detailed record makes these issues reproducible.

* **Cost monitoring**: Token usage directly impacts cost. Observability helps catch spikes early, especially in production environments.

* **Model drift and upgrades**: LLM providers regularly update model versions. Observability detects regressions or changes in model behavior.

* **Debugging hallucinations**: Examining retrieved documents and prompt structure is often key to resolving hallucinations or irrelevant responses.

## Task description

Each chatbot implementation explored so far in the course has the capability to export OpenTelemetry traces to an external endpoint, given by the `observability_config` setting in [`config.yaml`](/src/config.yaml).

First, study the `Telemetry` class, defined in [`telemetry.py`](/src/chatbot/utils/telemetry.py) and observe its usage as a [context manager](https://www.pythontutorial.net/advanced-python/python-context-managers/) in the `__main__.py` file of any of the chatbot implementations:

```python
with Telemetry(service_name=Path(__file__).parent.name):
    console(ChatBot)
```

To collect and visualize traces in this exercise, we will use [Langfuse](https://langfuse.com/), an open‑source LLM observability platform that can act as an OpenTelemetry HTTP backend. To run it locally with [Podman](https://podman-desktop.io/downloads), follow these steps:

1. Ensure you have a Compose provider installed.

   `podman compose` is a thin wrapper that delegates to an external provider (typically `docker-compose` or `podman-compose`). Confirm what Podman will use:

   ```powershell
   podman compose version
   ```

   If you see an error about a missing provider (or `podman compose` is not available), install `podman-compose` (Python) and re-run the command:

   ```powershell
   pip install --user podman-compose
   podman compose version
   ```

2. Create a folder for local Langfuse config (any location is fine) and create a `.env` file there with the following content:

   ```text
   # Core app secrets (local-only placeholders)
   NEXTAUTH_SECRET=dev-secret
   SALT=dev-salt
   # 64 hex chars. Generate securely for anything beyond local dev.
   ENCRYPTION_KEY=0000000000000000000000000000000000000000000000000000000000000000

   # Datastores (must match the docker-compose services)
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=postgres

   CLICKHOUSE_USER=clickhouse
   CLICKHOUSE_PASSWORD=clickhouse

   REDIS_AUTH=myredissecret

   MINIO_ROOT_USER=minio
   MINIO_ROOT_PASSWORD=miniosecret
   ```

   Passwords/secrets are required even for local runs because Postgres/Redis/MinIO need credentials and Langfuse uses secrets to sign sessions and encrypt stored payloads. Use placeholders for local development only, keep services bound to localhost, and don't reuse these values in shared environments.

3. Start Podman:

   ```powershell
   podman machine start
   ```

4. Download the upstream Langfuse `docker-compose.yml` into the same folder as your `.env`:

   ```powershell
   Invoke-WebRequest "https://raw.githubusercontent.com/langfuse/langfuse/main/docker-compose.yml" -OutFile docker-compose.yml
   ```

5. Run Podman Compose from that folder, referencing the downloaded compose file:

   ```powershell
   podman compose --env-file .env -f docker-compose.yml up -d
   ```

6. Ensure [`config.yaml`](/src/config.yaml) `observability_config` points to the Langfuse endpoint and names the environment variables that hold your API keys:

   ```yaml
   observability_config:
     endpoint: http://localhost:3000/api/public/otel/v1/traces
     langfuse_public_key_env_var: LANGFUSE_PUBLIC_KEY
     langfuse_secret_key_env_var: LANGFUSE_SECRET_KEY
   ```

7. Open the Langfuse UI at [`http://localhost:3000/`](http://localhost:3000/) and complete first-time setup: create an account, organization and project, then generate project API keys in the UI:

   * Select your **organization**
   * Select your **project**
   * Go to **Project Settings** → **API Keys**
   * Click **Create new API key**
   * Copy the **Public Key** and **Secret Key**

   Langfuse requires HTTP Basic authentication headers in telemetry messages, where the username is the **public key** and the password is the **secret key**. Set them as user environment variables: **Start** → search **environment variables** → **Edit environment variables for your account** → under *User variables*, add `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` with the values from the Langfuse UI. Restart your IDE afterward so your environment is refreshed to contain them.

Once Langfuse is running and the keys are set, start your chatbot. It will probe the observability endpoint and, if successful, show the following message at the console:

```text
INFO     Streaming traces to observability endpoint http://localhost:3000/api/public/otel/v1/traces for service <chatbot_name>
```

In this setup, traces are exported to the observability backend configured in `config.yaml` and appear in its UI after you run a chatbot implementation.

The dashboard summarizes activity across your project, for example trace counts, model usage, and cost:

![Observability dashboard showing trace counts and model cost](/images/observability_cost.png)

Open an individual trace to see how work is broken down into nested operations, such as agent-to-agent communication, LLM calls or HTTP requests. Selecting an operation reveals details captured by the instrumentation:

![Trace detail view showing prompts sent to the model](/images/observability_prompts.png)

For example, you can inspect:

* the full prompt and context sent to the model
* LLM responses
* token usage and cost
* model identity and provider
* timing for each step
* intermediate operations such as retrieval, rewriting, filtering or tool calls

This information is also available when errors occur and can help debug unexpected output, diagnose latency spikes, or track down excessive token usage.

To shut down Langfuse when you are done:

```powershell
podman compose --env-file .env -f docker-compose.yml down
```

## Under the hood

The [`Telemetry`](/src/chatbot/utils/telemetry.py) class takes a selective instrumentation approach, installing only the telemetry providers needed for the specific frameworks used in this codebase. This involves:

1. **Manual provider setup**: Creating an OpenTelemetry `TracerProvider` with a service name resource attribute that identifies the specific chatbot implementation being traced.

2. **OTLP HTTP exporter**: Using `OTLPSpanExporter` configured to send traces via HTTP to the observability endpoint. The exporter can attach optional HTTP headers—for example API key authentication configured in `observability_config`. It uses `BatchSpanProcessor` to efficiently batch spans before transmission, reducing network overhead.

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
        obs_cfg = config.get_observability_config()
        endpoint = obs_cfg.get("endpoint")
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

---

| 🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e10_a2a/README.md) |
| --- | --- |
