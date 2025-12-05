# Exercise 5: Tool calling

In this exercise, you will program the [chatbot](chatbot.py) to make use of the tools defined at the top of the file.

## Motivation

Continuing on the theme of programmatic uses of GenAI, a popular feature is LLM tool use. Tools give the model the capability to access new data sources or perform actions on behalf of the user.

Tools can be vendor-provided, such as web search, or defined by application developers. In Python, tools are functions with type-annotated parameters, as can be seen at the top of the exercise code (`convert_time` and `convert_currency`).

LangChain provides a [`bind_tools()`](https://docs.langchain.com/oss/python/integrations/chat/openai#chatopenai-bind-tools) to equip an LLM with tools. With this in place, the model can include tool call requests in its responses. However, this only covers the first part of the workflow - in LangChain, calling the requested tools and returning the results is a [manual process](https://python.langchain.com/docs/how_to/tool_results_pass_to_model/) which is cumbersome and error prone.

LangGraph, which is a Python package built on top of LangChain, provides a predefined agent to conveniently handle the whole process of LLM tool calling, [`create_react_agent()`](https://langchain-ai.github.io/langgraph/reference/agents/#langgraph.prebuilt.chat_agent_executor.create_react_agent). ReAct stands for reasoning-acting, a term introduced in this [paper](https://arxiv.org/abs/2210.03629). The diagram of this agent (or any other graph created with LangGraph) can be created for visualization via

```python
chatbot._graph.get_graph(xray=True).draw_mermaid_png(output_file_path="graph.png")
```

![Graph for a ReAct agent](/images/react_graph.png)

Tool call requests and text outputs are not technically mutually exclusive in an LLM response, yet most models will behave as if they were. This behavior is exploited by the agent; it presents the tools to the LLM and invokes it in a loop, resolving tool calls and appending the results to the conversation until no additional tool requests are received and the final answer is reached.

## Under the hood

Functions decorated as `@tool` have associated JSON schemas, which are used to describe their signature to the model. This is similar to the schema for structured outputs, as discussed earlier.

For the following function

```python
from enum import Enum
from langchain_core.tools import tool

class City(Enum):
    Oslo = "Oslo"
    LosAngeles = "Los Angeles"
    Dubai = "Dubai"

@tool
def get_temperature(city: City) -> float:
    """Get the temperature in degC for a given city. Returns a floating-point value."""
    ...
```

the corresponding JSON schema is

```json
"tools": [
  {
    "type": "function",
    "function": {
      "name": "get_temperature",
      "description": "Get the temperature in degC for a given city. Returns a floating-point value.",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "enum": ["Oslo", "Los Angeles", "Dubai"]
          }
        },
        "required": ["city"],
        "additionalProperties": false
      }
    }
  }
]
```

For further details on the syntax, check out the [OpenAI API](https://platform.openai.com/docs/guides/function-calling).

When presented with this, the LLM may choose to call the tool by issuing a special request

```json
{
  "role": "assistant",
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_temperature",
        "arguments": "{ \"city\": \"Oslo\" }"
      }
    }
  ]
}
```

The result is returned via the special response message shown below, where the `tool_call_id` must match the one in the request above

```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "21.3"
}
```

These entries are recorded alongside regular messages in the conversation. They are distinguished by the special `TOOL` role, present in the definition of [`ChatRole`](/src/chatbot/chat_history.py).

## Further reading

The behavior of the LLM when choosing to call tools can be controlled through two parameters:

* `tool_choice`, which can be the default `auto` (0 or more tools) or `none` (0 tools), `required` (1 or more tools), `forced` (where the list of tools that must be called is specified)
* `parallel_tool_calls` which is `true` if the LLM is allowed to request multiple tool calls per exchange, or `false` to force a maximum of 1

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e04_structured_outputs/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s05_tool_calling/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e06_mcp/README.md)
---|---|---|---
