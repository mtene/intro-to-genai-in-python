# Solution 2: System prompt

A possible [solution](chatbot.py) makes the chatbot change roles depending on the type of user message.

## Implementation: System prompt definition

If the system prompt is static, it can be defined once (at the global scope or in the constructor) and reused.

```python
def __init__(self):
    self._system_prompt = """Your role is given by type of user message:
- if it is a question, you have a bubbly personality
- otherwise, you are lazy and slow"""

def get_answer(self, question: str, ctx: ChatContext) -> str:
    messages = [system_message(self._system_prompt), user_message(question)]
    response = self._llm.invoke(messages)
```

Note that the triple quotation marks signal the definition of a multiline string, as it is not uncommon for system prompts to be long.

## Alternative approach: Prompt templates

When only a small fraction of the system prompt's content is dynamic, you can equip the LLM with a fixed [`langchain_core.prompts.ChatPromptTemplate`](https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html) and provide a mapping (dictionary) with the content of the dynamic fields at invocation.

```python
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder

def __init__(self):
    self._llm = LLM()
    self._system_prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a {role}"),
        MessagesPlaceholder(variable_name="messages"),
    ])

def get_answer(self, question: str, ctx: ChatContext) -> str:
    chat_messages = [user_message(question)]
    response = self._llm.invoke({"role": "friendly pirate", "messages": chat_messages})
```

Here, the system prompt has its own dedicated [`langchain_core.prompts.SystemMessagePromptTemplate`](https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.SystemMessagePromptTemplate.html), while all other chat messages are appended afterwards via the [`langchain_core.prompts.MessagesPlaceholder`](https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.MessagesPlaceholder.html).

## Verification

You can verify that the system prompt is effective by observing the changes in the structure or tone of the assistant's replies.

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e02_system_prompt/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e03_conversation_history/README.md)
---|---|---
