# Solution: Agent-to-Agent Protocol (A2A)

This solution demonstrates how to build a distributed multi-agent system using the A2A protocol.

## Implementation Overview

### Expert Agents

Both experts follow the same pattern:

**agent_card.yaml:**

```yaml
name: expert-name
description: >-
  Clear description of what this agent does...

skills:
  - name: skill-name
    description: >-
      What this skill accomplishes...

url: "http://127.0.0.1:8001"
```

**agent.py:**

```python
# Define detailed system prompt string
_system_prompt = """You are a **[Expert Role]**..."""

# Create agent with system prompt
# No tools needed - just responds based on expertise
agent = create_agent(model=LLM(), system_prompt=_system_prompt)
```

**Key design choices:**

* **Agent cards first** - Design metadata before implementation
* **Clear expertise** - Each agent has a well-defined domain
* **Concise responses** - System prompts encourage brevity
* **Specific formats** - Prompts guide output structure

### Agent Card Design

The agent card is crucial for A2A discovery. Good agent cards have:

**Clear descriptions:**

```yaml
description: >-
  Provides travel budget estimates and cost-saving advice for destinations worldwide.
  Offers realistic daily budget breakdowns covering accommodation, food, transportation,
  and activities. Considers seasonal pricing patterns and travel styles.
```

This tells other agents exactly when to use this expert.

**Well-defined skills:**

```yaml
skills:
  - name: estimate-budget
    description: >-
      Estimates realistic daily travel budgets for specific destinations,
      breaking down costs by category and considering seasonal variations.
```

Skills describe specific capabilities, making it easier for orchestrators to route complex queries.

### Budget Expert System Prompt

The budget expert prompt includes:

* Role definition (budget expert for travel)
* Specific expertise areas (estimations, cost breakdowns, seasonal patterns)
* Response guidelines (format, level of detail)
* Example response showing the expected style

This gives the LLM clear guardrails for generating useful budget advice.

### Destination Expert System Prompt

The destination expert prompt includes:

* Role definition (destination recommendations)
* Expertise areas (matching preferences, seasonal advice, activities)
* Response structure (2-3 destinations with reasoning)
* Example response showing the format

This ensures recommendations are actionable and well-organized.

### Orchestrator Configuration

The orchestrator loads agent configuration from [`agents.yaml`](agents.yaml). Thes include the connection URL, a name and description which will be used in the corresponding tool definitions for the ReAct loop:

```yaml
agents:
  - name: budget_expert
    url: http://127.0.0.1:8001
    description: Provides travel budget estimates and cost-saving advice

  - name: destination_expert
    url: http://127.0.0.1:8002
    description: Recommends travel destinations based on preferences
```

This makes it:

* **Easy to add agents** - Just add a new entry to `agents.yaml`
* **No code changes** - Orchestrator loads agents dynamically
* **Version control friendly** - Easy to see what changed
* **Reusable** - Same pattern works for any number of agents

**Example - Adding a weather expert:**

```yaml
agents:
  ...
  - name: weather_expert
    url: http://127.0.0.1:8003
    description: Provides weather forecasts and seasonal information
```

**chatbot.py:** loads agents dynamically and creates tools

```python
# Load agents configuration from YAML
with open(Path(__file__).parent / "agents.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create A2A tools from configuration
agents = [
    A2AAgentTool(
        name=agent["name"],
        description=agent["description"],
        url=agent["url"],
    )
    for agent in config["agents"]
]

# Create orchestrator with tools (same pattern as lesson 6)
self._agent: CompiledStateGraph = create_agent(
    model=llm,
    tools=agents,
    checkpointer=MemorySaver(),
)
```
**Agent Cards vs Tool Descriptions**

Notice how we define agent metadata in **two places**:

1. **Agent card (YAML)** - For the agent server:

```yaml
description: Provides travel budget estimates...
```

1. **Tool description** - For the orchestrator:

```python
A2AAgentTool(
    name="budget_expert",
    description="Get travel budget estimates...",  # Similar but for LLM
    url="http://127.0.0.1:8001",
)
```

**Why the duplication?**

* **Agent card** - Used by A2A discovery (agents finding each other)
* **Tool description** - Used by LLM routing (deciding when to call)

In a production A2A system, the orchestrator could fetch agent cards automatically and generate tool descriptions from them. For this lesson, we deliberately keep them separate for simplicity.

**How agent routing works:**

The orchestrator doesn't use keyword matching or rules. Instead, the LLM:

1. Reads the user's question
2. Sees tool descriptions (loaded from [`agents.yaml`](agents.yaml))
3. Decides which tool(s) to call
4. May call tools in sequence or parallel
5. Synthesizes final answer

## Design Patterns

### 1. Progressive Complexity

* Start with simple agents (no RAG, no tools)
* Add orchestration layer
* Extend with more agents (breadth) or increase logic complexity (depth)

### 2. Clear Separation of Concerns

* Each agent is an expert
* Orchestrator chooses the appropriate agent(s) and combines their output
* Communication is handled via the A2A protocol and can be combined with MCP

### 3. Reusability

* Agents could be used in other workflows
* Each agent implementation can be modified independently
* Protocol is language-agnostic

## A2A Protocol Flow

Here's what happens when you ask: "What's a good budget for Paris?"

```plaintext
1. User → Orchestrator
   "What's a good budget for Paris?"

2. Orchestrator → LLM
   Context: User question + available tools (budget_expert, destination_expert)
   LLM Decision: Call budget_expert tool

3. Orchestrator → Budget Expert (via A2A/HTTP)
   POST http://127.0.0.1:8001
   {"role": "user", "content": "What's a good budget for Paris?"}

4. Budget Expert → Orchestrator
   Response: "For mid-range Paris, budget $150-200/day..."

5. Orchestrator → LLM
   Context: User question + tool result
   LLM Decision: Enough info, respond to user

6. Orchestrator → User
   "For a mid-range trip to Paris, you should budget $150-200/day..."
```

For complex questions, the orchestrator may call multiple experts or make multiple rounds of calls.

## Extensions

Want to go further? Try to:

1. **Add a third expert** (e.g., weather, activities)
2. **Add RAG to destination expert** (load destination database)
3. **Add tools to budget expert** (currency conversion API)
4. **Implement parallel calls** (orchestrator calls both experts simultaneously)
5. **Add error handling** (what if an expert is down?)
6. **Switch to DeepAgents** (use `create_deep_agent` with skills)

## Key Takeaways

1. **Agent cards are essential** - Design them before implementation
2. **A2A enables distributed agent systems** - Each agent runs independently
3. **LLM-driven routing** - No hardcoded rules, the orchestrator decides dynamically
4. **Simple agents can be powerful** - System prompts provide expertise
5. **HTTP adds latency** - Trade-off between modularity and speed
6. **Tool descriptions guide routing** - They help the LLM make good decisions

---

| 🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e10_a2a/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e11_observability/README.md) |
| --- | --- | --- |
