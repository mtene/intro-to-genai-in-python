# Solution: Tool calling

In the solution, we provide the [chatbot](chatbot.py) with a ReAct agent configured with our tools of interest.

## Implementation: ReAct agent setup

```python
def __init__(self):
    llm = LLM()
    tools = [convert_time, convert_currency]
    self._agent = create_agent(model=llm, tools=tools, checkpointer=MemorySaver())
    self._thread_id = str(uuid.uuid4())
```

The agent sets up a [`langchain_core.prompts.ChatPromptTemplate`](https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html) internally (though you can provide your own). It configures the provided LLM instance to use tools via LangChain's [`bind_tools()`](https://docs.langchain.com/oss/python/integrations/chat/openai#chatopenai-bind-tools). As with structured outputs, the original `llm` object remains unmodified and continues to return free-text responses when invoked.

The `MemorySaver` checkpointer automatically manages conversation history, storing all messages (including tool calls and results) keyed by `thread_id`.

The agent is used as below

```python
@override
def get_answer(self, question: str, ctx: ChatContext) -> str:
    response = self._agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        config={
            **self.get_config(ctx),
            "configurable": {"thread_id": self._thread_id}
        }
    )
    answer = str(response["messages"][-1].content)
```

Notice we pass only the **new HumanMessage**, not the entire history. The checkpointer automatically loads previous messages using the `thread_id` and saves all new messages (including tool calls and results) after execution.

To clear the conversation, simply generate a new `thread_id` in the `reset()` method:

```python
def reset(self) -> None:
    self._thread_id = str(uuid.uuid4())
```

The response contains a list of all messages generated during this turn. They include any tool calls and results, but usually, only the last one, which gives the final answer, is of interest.

```python
answer = str(response["messages"][-1].content)
```

## Verification

Ask questions involving time or currency conversions and verify that the tools get called by observing the status updates.

## Testing and evaluation

Separate the visible answer from the tool trajectory. Mock deterministic tools to validate selected names and arguments; use answer metrics only for the final synthesis, and do not confuse API outages with agent failures.

---

| 🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e07_tool_calling/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e08_mcp/README.md) |
| --- | --- | --- |
