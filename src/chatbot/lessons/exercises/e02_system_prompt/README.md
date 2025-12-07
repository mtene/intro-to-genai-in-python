# Exercise 2: System prompt

⏱️ **Estimated time**: 10 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Write effective system prompts that guide LLM behavior
* Include various system prompt component such as role, mission, steps, rules and examples
* Understand the difference between system messages and user messages

## Overview

In this exercise, we turn attention to the system prompt. It contains instructions for the LLM, dictating its behavior when tackling user queries. These do not come from the user, they are set by the developers to fit the scope and goals of the application.

Update the [chatbot logic](chatbot.py) with a system prompt. The instructions are up to you. As an example, try to make it respond like a friendly pirate.

Run the [tests](tests.py) in the console to track progress and extend them with your own. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## System prompt structure

Typically, the system prompt contains some or all of the following elements:

* a role: `You are a helpful assistant for users of the ... app`
* a mission: `Your task is to answer the user query`
* a sequence of steps to follow (recipe)
* guardrails and constraints
* desired answer format
* relevant background information
* examples

This content is a key differentiator for the different agents in a multi-agent system. They often use the same underlying LLM, but the system prompt and the tools at their disposal make them produce very different responses to the same user question.

## Just another chat message

The system prompt is bundled with other chat messages in the LLM call. What distinguishes it is the special [`SYSTEM`](/src/chatbot/chat_history.py) role assigned to it.

**Message ordering matters.** When prompting LLMs, information order is critical because the model's "attention span" is limited, especially for models with fewer active parameters. The most important information should appear first, which is why the system prompt should precede all other chat messages.

## Further reading

[Learn Prompting: Introduction to Prompt Engineering](https://learnprompting.org/docs/introduction) provides comprehensive tutorials on prompt engineering techniques, including system prompt design, few-shot learning and advanced prompting strategies.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e01_prompting/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s02_system_prompt/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e03_conversation_history/README.md)
---|---|---|---
