# Solution 3: Tracking conversation history

The [solution](chatbot.py) to the exercise equips the chatbot with a [`ChatHistory`](/src/chatbot/chat_history.py) object.

## Implementation: Chat history initialization

The chat history must persist between calls to `get_answer`, therefore, it needs to be kept as a field in the chatbot's state, initialized in the constructor

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

After a few exchanges, ask the chatbot to translate its first answer to another language. If you've also implemented the pruning of the chat history to the last 5 exchanges, you will observe that the chatbot will translate its 2nd answer in a conversation with 6 exchanges. This will surprise the user, but is a rare occurrence in most practical scenarios. The gains in robustness and avoiding LLM errors due to exceeding the maximum LLM context size are likely worth it. The optimal length of the sliding window of historical messages is application specific.

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e03_conversation_history/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e04_structured_outputs/README.md)
---|---|---
