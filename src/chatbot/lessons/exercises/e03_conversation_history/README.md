# Exercise 3: Tracking conversation history

⏱️ **Estimated time**: 20 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Explain why LLMs are stateless and what this means for applications
* Implement conversation history tracking using the `ChatHistory` class
* Manage state in the chatbot by storing history between method calls
* Implement a sliding window to prevent context overflow

## Overview

In this exercise, you will make the [chatbot logic](chatbot.py) able to track the user questions and corresponding answers between multiple calls.

Run the [tests](tests.py) in the console to track progress and extend them with your own. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## Motivation

LLMs are fundamentally stateless. They process millions of requests from different users and are not designed to retain individual session information. Some caching exists for performance, but this is transparent to you while prompting.

This statelessness means you can hand-craft a conversation history - including assistant replies, tool calls and results - the LLM will continue the thread as if it unfolded organically. When an answer depends on previously discussed information, that context must be included with the query.

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
