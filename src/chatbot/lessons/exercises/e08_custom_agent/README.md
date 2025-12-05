# Exercise 8: Custom agent

In this exercise, you will define your own custom LangGraph agent as part of the [chatbot logic](chatbot.py).

## Task description

Consider a chatbot that takes a user request for text generation and creates an adversarial pair of agents, namely an `author` and `reviewer`, working together to improve the generated text according to the user's stated needs. The author performs modifications based on feedback from the reviewer, who acts as gatekeeper to the process, accepting or sending the text back for revision.

There are many ways this system can be implemented and orchestrated as a graph. To start with, a sample definition of the [`GraphState`](state.py) and a possible implementation of the [`author`](author.py) node is given in the exercise code. The [`reviewer`](reviewer.py) and loop termination condition have mock implementations. This, in essence, leads to a single author pass without any checks.

First, craft a few prompts and list your expectations, then use them to benchmark the performance of this initial graph. As you add modifications, repeat this process and note down if the metrics improve. As a bonus, automate the benchmarking process by using the instance of the chatbot in [`__main__.py`](__main__.py).

The task is to complete the implementation of the nodes, by combining all the different techniques covered in the course so far: system prompts, structured outputs, perhaps even tools. Feel free to alter the architecture of the graph and add new nodes, if needed. There is no single best solution.

## Language graphs

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

When a node executes, the values of fields in the state are used to generate modifications, which are returned as a dictionary. In the case of the `assistant` node from the graph above, `messages` is updated to include the LLM request and response.

```python
return {"messages": state.messages + [llm_request, llm_response]}
```

Note that the unmodified state fields, if any, are simply omitted in the return.

Some fields may have custom reduction operations associated. This is a function that is called with the old value and what the node returns under the corresponding dictionary key to produce the update. For example, in LangChain's [`MessagesState`](https://deepwiki.com/langchain-ai/langchain-academy/3.1-stategraph-and-messagesstate) the `messages` field is annotated with an `add_messages` reduction, which appends the value corresponding to `"messages"` in the result to the list. This is convenient, as the node result only needs to contain `{"messages": [llm_request, llm_response]}`, but sacrifices flexibility for other types of operations - there is no longer a way for a node to remove messages (e.g. for context pruning). Also, callers unaware of this will get duplicated messages. Therefore, it is likely less confusing to avoid custom reductions and use the default replacement behavior.

The possibilities of how a given node's logic can be implemented are endless. They can use algorithms, call LLMs, consult web services / file systems / databases or even invoke their own nested agents. This makes graphs very versatile for advanced AI application development, with the trade-off of implementation and maintenance complexity. This can be mitigated, in part, by using a modular code structure with type annotations, making use of classes split among separate files.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e07_rag/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s08_custom_agent/README.md)
---|---|---
