# Exercise: Agent-to-Agent Protocol (A2A)

⏱️ **Estimated time**: 35 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Understand the Agent-to-Agent (A2A) protocol and its benefits
* Design agent cards for A2A discovery
* Expose LangChain agents as A2A servers using HTTP
* Implement simple expert agents using system prompts
* Understand how orchestrators call remote A2A agents as tools
* Compare distributed multi-agent architectures with monolithic agents

## Overview

In this exercise, you will implement two **specialized agents** for a Travel Planning Assistant:

1. **Budget Expert** - Provides cost estimates and budget advice
1. **Destination Expert** - Recommends destinations based on preferences

An additional orchestrator agent is provided as the main entry point. It coordinates the experts to answer user questions.

Each agent runs in its own separate process and communication happens over HTTP using the **A2A protocol**.

[`__main__.py`](__main__.py) automatically starts the orchestrator and both expert agents, making it easy for you to run the [tests](tests.py) in the console and track progress. This is not done by the Streamlit UI, requiring you to start them manually beforehand.

## Motivation

### Why Distributed Agents?

As AI applications grow more sophisticated, **multi-agent systems** are becoming essential. Instead of building one massive agent that does everything, you can compose specialized agents that each excel at specific tasks.

**Monolithic approach** (everything in one agent):

```plaintext
┌────────────────────────────────┐
│   Single Large Agent           │
│                                │
│  • Budget calculations         │
│  • Destination knowledge       │
│  • Weather data                │
│  • Booking systems             │
│  • Reviews aggregation         │
└────────────────────────────────┘
```

Limitations:

* Hard to maintain
* All-or-nothing deployment
* Can't reuse components

**Distributed approach** (specialized agents):

```plaintext
┌──────────────────┐
│  Orchestrator    │────┐
└──────────────────┘    │
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Budget     │ │ Destination  │ │   Weather    │
│   Expert     │ │   Expert     │ │   Expert     │
└──────────────┘ └──────────────┘ └──────────────┘
```

Benefits:

* Independent development & deployment
* Reusable across applications
* Easier to test & maintain
* Each can be scaled independently

### The Agent-to-Agent (A2A) Protocol

[A2A](https://a2a-protocol.org/latest/) is an open protocol for agents to communicate over HTTP. It standardizes:

* **Discovery** - Each agent describes its capabilities via an `AgentCard`
* **Communication** - JSON-RPC messages with streaming support
* **Task management** - Asynchronous task execution and progress tracking

**Key concepts:**

* **Agent Server** - Exposes an agent via HTTP
* **Agent Client** - Calls remote agents over HTTP
* **AgentCard** - Metadata describing the agent's name, skills, and capabilities

A2A is **language-agnostic** - an agent written in Python can call one written in TypeScript or C#. This makes it ideal for building heterogeneous multi-agent systems.

### Understanding Agent Cards

An **agent card** is like a business card for your agent. It tells other agents:

* **What the agent does** - Clear description of capabilities
* **What skills it provides** - Specific operations it can perform
* **How to reach it** - URL and port
* **What it expects** - Input and output formats

**Example agent card:**

```yaml
name: weather-service
description: >-
  Provides weather forecasts and climate information for locations worldwide

skills:
  - name: get-forecast
    description: >-
      Returns weather forecast for a specific location and time range

url: "http://127.0.0.1:9000"
```

This metadata enables **agent discovery** - other agents can find and understand what services are available without reading code.

### A2A vs Other Protocols

| Protocol | Purpose | Scope |
| -------- | ------- | ----- |
| **A2A** | Agent-to-agent communication | Distributed AI systems |
| **MCP** | Tool/data source integration | Connecting agents to resources |

A2A complements MCP - you might use MCP to connect an agent to databases, and A2A to connect agents to each other.

## Architecture

This exercise demonstrates a simple A2A architecture:

```plaintext
User Question
     │
     ▼
┌─────────────────────────────────┐
│  Orchestrator (chatbot.py)      │
│  Decides which expert(s) to use │
└─────────────────────────────────┘
     │
     ├──────────────────┬──────────────────┐
     │                  │                  │
     ▼                  ▼                  ▼
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Budget  │      │  Dest.   │      │  Both    │
│  Expert  │      │  Expert  │      │  (Order) │
│  :8001   │      │  :8002   │      │  Varies  │
└──────────┘      └──────────┘      └──────────┘
     │                  │                  │
     └──────────────────┴──────────────────┘
                    │
                    ▼
               Final Answer
```

**How it works:**

1. User asks a question to the orchestrator
2. Orchestrator's LLM decides which expert(s) to call (using tool calling)
3. Expert agents run on separate ports (8001, 8002)
4. Orchestrator calls experts via HTTP using A2A protocol
5. Experts return answers
6. Orchestrator synthesizes final response

## What You'll Build

### 1. Budget Expert [`agents/budget_expert/`](agents/budget_expert/)

A simple agent with expertise in travel costs:

* [`agent.py`](agents/budget_expert/agent.py) - Defines the agent with `create_agent()` and a system prompt (✏️ TODO)
* [`agent_card.yaml`](agents/budget_expert/agent_card.yaml) - Agent metadata for A2A discovery (✏️ TODO)
* [`__main__.py`](agents/budget_expert/__main__.py) - Starts the A2A server on port 8001 (✅ DONE)

### 2. Destination Expert [`agents/destination_expert/`](agents/destination_expert/)

A simple agent with expertise in destination recommendations:

* [`agent.py`](agents/destination_expert/agent.py) - Defines the agent with `create_agent()` and a system prompt (✏️ TODO)
* [`agent_card.yaml`](agents/destination_expert/agent_card.yaml) - Agent metadata for A2A discovery (✏️ TODO)
* [`__main__.py`](agents/destination_expert/__main__.py) - Starts the A2A server on port 8002 (✅ DONE)

### 3. Orchestrator

The main chatbot that coordinates experts:

* [`agents.yaml`](agents.yaml) - Configuration file defining available A2A agents (✅ DONE)
* [`chatbot.py`](chatbot.py) - Loads agents from YAML and creates the orchestrator (✅ DONE)
* [`__main__.py`](__main__.py) - Starts all agents in separate processes (✅ DONE)

The orchestrator:

* Reads [`agents.yaml`](agents.yaml) to discover available expert agents
* Creates `A2AAgentTool` instances for each agent
* Uses LangChain's `create_agent()` with the expert tools
* LLM decides which expert(s) to consult based on the user query

## Your Tasks

### Task 1: Design Budget Expert Agent Card

In [`agent_card.yaml`](agents/budget_expert/agent_card.yaml):

1. Write a clear `description` of what this agent does
   * This is what other agents see when deciding whether to call it
   * Should describe expertise, capabilities, and use cases
2. Define the `estimate-budget` skill with a detailed description
   * What does this skill do?
   * What kind of input does it expect?
   * What kind of output does it provide?

**Why this matters:** The agent card is how agents discover each other in A2A systems. A well-designed card helps orchestrators make better routing decisions.

### Task 2: Implement Budget Expert

In [`agent.py`](agents/budget_expert/agent.py):

1. Create a detailed system prompt string defining the expert's role
   * Focus on budget estimation, cost breakdowns, seasonal pricing
   * Keep responses concise (3-5 sentences)
   * Include an example response format
2. Create the agent `create_agent()` by passing `model=` the LLM instance and `system_prompt=` the system prompt

### Task 3: Design Destination Expert Agent Card

Follow the same pattern in [`agent_card.yaml`](agents/destination_expert/agent_card.yaml).

### Task 4: Implement Destination Expert

Similar for [`agent.py`](agents/destination_expert/agent.py).

## Orchestrator Review

Even though the orchestrator implementation is already complete, it is instructive to review it:

1. **agents.yaml** is an agent discovery configuration file:

```yaml
agents:
   - name: budget_expert
      description: When to use this agent...
      url: http://127.0.0.1:8001
```

2. **chatbot.py** loads agents dynamically:

* Reads [`agents.yaml`](agents.yaml) to discover agents
* Constructs [`A2AAgentTool`](/src/chatbot/utils/a2a.py) for each agent
* Creates a ReAct agent using `create_agent()` and registers the agents as tools
* Defines a generic system prompt guiding orchestration behavior

This exercise follows a **centralized orchestrator pattern** where one agent coordinates all others. However, A2A is a peer-to-peer protocol - there's nothing stopping expert agents from calling each other directly using a similar configuration and tool wrappers as the orchestrator! You could build a fully decentralized mesh network where agents discover and communicate without a central coordinator.

## Running Your Implementation

The expert agents run as independent HTTP servers in dedicated processes. In console mode, simply running the lesson will automatically start all agents to facilitate testing (see [`__main__.py`](__main__.py)). However, when using the Streamlit UI, they must be started manually beforehand, in separate terminals:

```bash
python -m chatbot.lessons.exercises.e10_a2a.agents.budget_expert
python -m chatbot.lessons.exercises.e10_a2a.agents.destination_expert
```

for the exercises, or for the solutions:

```bash
python -m chatbot.lessons.solutions.s10_a2a.agents.budget_expert
python -m chatbot.lessons.solutions.s10_a2a.agents.destination_expert
```

Try these prompts:

**Single expert calls:**

```plaintext
>>> What's a realistic daily budget for visiting Tokyo?
```

(Should call budget expert only)

```plaintext
>>> Recommend destinations for someone who loves hiking
```

(Should call destination expert only)

**Multi-expert orchestration:**

```plaintext
>>> I want to visit Europe on a tight budget. Where should I go?
```

(Should call destination expert, then budget expert, or both)

```plaintext
>>> Plan a 2-week trip to Southeast Asia for $2000
```

(Should coordinate both experts)

**Watch the orchestrator's tool calls** in the terminal output - you'll see which experts are consulted!

## Under the hood

The `chatbot.utils.a2a` module provides two helper classes:

### A2AAgent

Exposes a LangChain agent via A2A protocol:

```python
# Create A2A server
server = A2AAgent(
    agent=my_agent,                      # LangChain agent from create_agent()
    agent_card_path="agent_card.yaml"    # Path to agent card YAML
)
server.start()  # Blocks until Ctrl+C
```

**How it works:**

* Loads agent metadata from YAML file
* Wraps your sync agent in an async bridge (A2A SDK is async)
* Creates an `AgentCard` from the YAML data
* Starts the agent as a server
* Routes A2A requests to your agent's implementation as if they were coming from the user

### A2AAgentTool

Calls a remote A2A agent as a LangChain tool:

```python
tool = A2AAgentTool(
    name="expert_name",              # Tool name for LLM
    description="When to use this",  # Helps LLM decide
    url="http://127.0.0.1:8001"      # A2A agent URL
)
```

**How it works:**

* Creates an A2A client on first use
* Bridges sync tool calling to async A2A calls
* Returns the expert's response as a string

These wrappers handle all data conversion and A2A communication.

## Further Reading

[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Anthropic guide on agent design patterns and best practices

[Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/) - LangChain guide comparing network, supervisor, and hierarchical patterns

[Multi-Agent System Architectures: A Survey](https://arxiv.org/abs/2404.11584) - Academic overview of architectural patterns for LLM agents

[A2A Protocol Specification](https://a2a-protocol.org/latest/) - Official A2A SDK and protocol documentation

---

| 🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e09_deep_agent/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s10_a2a/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e11_observability/README.md) |
| --- | --- | --- | --- |
