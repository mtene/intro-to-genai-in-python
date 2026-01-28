# Exercise 9: Observability

⏱️ **Estimated time**: 30 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Explain what kind of data can be observed from application telemetry
* Visualize telemetry traces as a timeline
* Drill down into individual prompts and inspect metadata

## Overview

In this exercise, you will start a telemetry endpoint which receives traces and displays them visually for inspection.

## Task description

Each chatbot implementation explored so far in the course has the capability to export OpenTelemetry traces to an external endpoint, given by the corresponding setting in [`config.yaml`](/src/config.yaml).

We will use [Jaeger](https://www.jaegertracing.io/download) by either downloading and running the binary or using [`podman`](https://podman.io/) to spin it up in a container:

```powershell
podman run --rm --name jaeger -p 16686:16686 -p 4318:4318 cr.jaegertracing.io/jaegertracing/jaeger
```

Upon startup, the chatbot tries to reach the observability endpoint and, if successful, the following messages is shown at the console:

```powershell
INFO     Streaming traces to observability endpoint http://localhost:4318/v1/traces
```

With Jaeger, chatbot traces are streamed via HTTP requests to port `4318` on the local machine and can be visualized by navigating to [`http://localhost:16686/`](http://localhost:16686/). As an example, the screenshot below shows a trace produced by running the custom agent from the previous lesson.

![Trace visualization in Jaeger](/images/observability.png)

## Further reading

[Best LLM Observability Tools of 2025](https://www.comet.com/site/blog/llm-observability-tools/) is a comparison of different trace collection and visualization solutions.

It may also be instructive to study the [OpenTelemetry](https://opentelemetry.io/docs/) framework.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md)
---|---
