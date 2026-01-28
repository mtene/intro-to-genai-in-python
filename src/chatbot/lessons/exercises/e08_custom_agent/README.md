# Exercise 8: Custom agent

⏱️ **Estimated time**: 60 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Design and implement custom LangGraph agents from scratch
* Define graph state, nodes and edges for multi-step workflows
* Combine multiple techniques (structured outputs, system prompts, tools) in agent nodes

## Overview

In this exercise, you will define your own custom LangGraph agent as part of the [chatbot logic](chatbot.py).

Run the [tests](tests.py) in the console to track progress and extend them with your own. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## Task description

Consider a chatbot that takes a user request for text generation and creates an adversarial pair of agents, namely an `author` and `reviewer`, working together to improve the generated text according to the user's stated needs. The author performs modifications based on feedback from the reviewer, who acts as gatekeeper to the process, accepting or sending the text back for revision.

There are many ways this system can be implemented and orchestrated as a graph. To start with, a sample definition of the [`GraphState`](state.py) and a possible implementation of the [`author`](author.py) node is given in the exercise code. The [`reviewer`](reviewer.py) and loop termination condition have mock implementations. This, in essence, leads to a single author pass without any checks.

The task is to complete the implementation of the nodes, by combining all the different techniques covered in the course so far: system prompts, structured outputs, perhaps even tools. Feel free to alter the architecture of the graph and add new nodes, if needed. There is no single best solution.

As you work through this exercise, test your implementation with diverse prompts representing different text formats (emails, summaries, creative writing). Observe whether the reviewer provides useful feedback and whether the author incorporates it meaningfully. The command-line interface is helpful for iterative testing.

## LangGraph architecture

As we have seen before, the ReAct agent, predefined in LangGraph, behaves according to the flow of information through the nodes (from `START` towards `END`) and along the edges, as shown in the diagram

![Graph for a ReAct agent](/images/react_graph.png)

## Graph state

Information is captured in a `State` class which, for the graph above, simply contains the list of messages

```python
class State(BaseModel):
    messages: List[ChatMessage]
```

`State` can inherit from any typed class, such as `TypedDict` or Pydantic's `BaseModel`.

## Graph construction

The graph is built only once, upon chatbot construction. This is done by listing all the nodes and edges

```python
graph_builder = StateGraph(GraphState)
# define nodes
graph_builder.add_node("Author", _author)
graph_builder.add_node("Reviewer", _reviewer)
graph_builder.add_node("UpdateIteration", _update_iteration)
# define edges
graph_builder.add_edge(START, "Author")
graph_builder.add_edge("Author", "Reviewer")
graph_builder.add_edge("Reviewer", "UpdateIteration")
graph_builder.add_conditional_edges(
    "UpdateIteration", _end_condition, {"continue": "Author", "finish": END}
)
# build graph
return graph_builder.compile()
```

Each node is defined using a label and a method that implements it. The method takes the state and an optional `RunnableContext` as arguments (the latter is only used for reporting) and returns the dictionary describing the state modifications. Two special nodes, `START` and `END`, mark the entry and exit points in the graph, respectively.

Regular edges simply connect two nodes, specified through their labels.

Conditional edge logic is specified through special methods, that take the state (and the optional context) as arguments and output a string label, signifying the outcome. There is no limit to the possible outcomes of a conditional edge, but it is common that they only have two, e.g. `continue` and `break` to control looping. Each label is then mapped to a node, forming a fork-shaped connection. This can be seen around the `assistant` node in the diagram above, which is conditionally connected to either `tools` or `END`.

## Graph logic

When a node executes, it inspects the current state and generates modifications, which are returned as a dictionary. For example, the `assistant` node from the graph above updates `messages` to include the LLM request and response:

```python
return {"messages": state.messages + [llm_request, llm_response]}
```

Unmodified state fields are simply omitted from the return value. Some fields may have custom reduction functions that combine the old value with the node's returned value. For example, in LangChain's [`MessagesState`](https://deepwiki.com/langchain-ai/langchain-academy/3.1-stategraph-and-messagesstate), the `messages` field uses an `add_messages` reduction that appends new messages to the list.

While convenient (nodes only return `{"messages": [llm_request, llm_response]}`), this sacrifices flexibility. For example, a node cannot easily remove messages (e.g., for context pruning). Also, nodes that were designed without the reduction in mind will return the full list of messages and cause duplication. Therefore, avoiding custom reductions and using the default replacement behavior is often less confusing.

The possibilities of how a given node's logic can be implemented are endless. They can use algorithms, call LLMs, consult web services / file systems / databases or even invoke their own nested agents. This makes graphs very versatile for advanced AI application development, with the trade-off of implementation and maintenance complexity. This can be mitigated, in part, by using a modular code structure with type annotations, making use of classes split among separate files.

## Further reading

[Choose a Design Pattern for Your Agentic AI System](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) explores various agent design patterns including reflection, planning, multi-agent collaboration and tool-use patterns for building production agentic systems.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e07_rag/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s08_custom_agent/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e09_observability/README.md)
---|---|---|---
