# Solution: Memory

The [solution](chatbot.py) to the exercise equips the chatbot with a [`ChatHistory`](/src/chatbot/chat_history.py) object.

Run the [tests](tests.py) in the console and verify that they all pass. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## Implementation: Chat history initialization

The chat history must persist between calls to `get_answer`. Store it as a field in the chatbot's state, initialized in the constructor:

```python
    def __init__(self):
        self._chat_history = ChatHistory()
```

## Implementation: Chat history updates

For each exchange, the user question and assistant reply are stored within

```python
self._chat_history.add_message(user_message(question))
self._chat_history.add_message(assistant_message(answer))
```

This allows us to pass the list of all recorded messages to the LLM, making it able to understand the context when the user is referring to previously discussed content

```python
response = self._llm.invoke(self._chat_history.messages, config=self.get_config(ctx))
```

The addition of chat history tracking makes the chatbot stateful, an important stepping stone towards becoming an agent.

## Verification

After a few exchanges, ask the chatbot to translate its first answer to another language.

If you've implemented pruning to keep only the last 5 exchanges, the chatbot will translate its second answer in a conversation with 6 exchanges (since the first was pruned). While this may surprise users, it's rare in practice. The gains in robustness and avoiding context-size errors outweigh this drawback. The optimal sliding window length is application-specific.

## Further reading

### Manual vs. Automatic Memory Management

This exercise demonstrates **manual history management** - explicitly tracking and passing messages to the LLM. This approach is important for understanding the fundamentals of how conversation state works.

In later exercises, you'll use agent frameworks that provide **built-in memory management systems**. For example, LangGraph's checkpointer automatically handles conversation state using a `thread_id`, eliminating the need for manual `ChatHistory` tracking.

Production systems typically use these framework-level abstractions, but understanding manual management first helps you:

* Appreciate what frameworks do behind the scenes
* Debug memory-related issues more effectively
* Implement custom memory strategies when needed

---

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e03_memory/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e04_rag/README.md)
---|---|---
