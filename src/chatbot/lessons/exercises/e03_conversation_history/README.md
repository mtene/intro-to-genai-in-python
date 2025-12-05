# Exercise 3: Tracking conversation history

In this exercise, you will make the [chatbot logic](chatbot.py) able to track the user questions and corresponding answers between multiple calls.

## Motivation

It is important to think of LLMs as stateless. They answer millions of requests from different users and are, therefore, not designed to retain individual session information (this is not absolutely true, as some caching is in place for performance reasons, but this should be transparent to you). Therefore, it would be perfectly valid to hand-craft a conversation history, including replies from the assistant, tool calls and results - the LLM will happily continue that thread as if it was created organically.

If the answer depends on previously discussed information, this has to be included as part of the query.

In the exercises completed so far, all question-answer pairs were generated independently of each other. However, the need to reference a previous exchange arises frequently. For example, without chat history tracking:

```plaintext
User: What is a popular food in France?
Assistant: Snails
User: What do they call that dish in French?
Assistant: Sure, I can help you with French translation if you tell me what dish you're interested in.
User: ??
```

The purpose of this exercise is to address this limitation by equipping the chatbot with memory of the past messages in the current conversation. In a real app, this can even be extended to transcend sessions via user profiles.

## Why don't we simply get it from the frontend?

If you've inspected the UI, you've noticed that there is already code to keep track of the conversation history there. So why not pass that directly as an argument when querying the chatbot?

This might seem like a good idea initially, but as applications evolve, it will quickly become a design limitation. The frontend (UI) and backend (chatbot) keep track of messages for very different purposes.

The frontend needs to display a complete history of the messages the user is aware of, i.e. questions and answers exchanged in the current conversation. On the other hand, the chatbot may deal with additional messages behind the scenes, e.g. a system prompt, tool call requests and results. The user is not aware of these and they should not be exposed to avoid confusion.

Additionally, to reduce the context length, avoid biases from old data and maintain focus on what is relevant, it may be beneficial to limit LLM visibility to a sliding window of the N most recent messages (which can be easily achieved as a bonus for this exercise).

## How do I do it?

Inspect the [`ChatHistory`](/src/chatbot/chat_history.py) class and you can also take inspiration from how it is used in the [UI](/src/user_interface/app.py).

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e02_system_prompt/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s03_conversation_history/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e04_structured_outputs/README.md)
---|---|---|---
