# Solution 1: Text prompting

The [solution](chatbot.py) to the exercise uses an LLM to answer user queries.

Run the [tests](tests.py) in the console and verify that they all pass. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## Implementation: LLM initialization

You would obtain the same behavior with the LLM constructed just before use, in `get_answer` and destroyed afterwards. However, this is unnecessarily wasteful and may slow down responses.

As a reusable resource, the LLM should be initialized only once, in the constructor

```python
def __init__(self):
    self._llm = LLM()
```

The `_` prefix is just Python naming convention to signal that the field is for private use only and should not be inspected or modified from the outside. Unlike other languages (C++, C#, Java, etc.), Python syntax provides no privacy safeguards for class fields and methods.

## Implementation: LLM usage

The LLM is queried in `get_answer` by providing the list of messages currently in the conversation. This only includes the user query, for now, as we're not yet tracking chat history (to be tackled later)

```python
messages = [user_message(question)]
response = self._llm.invoke(messages, config=self.get_config(ctx))
```

As mentioned before, passing `ctx` via `config` is done only to enable reporting status updates to the UI and has no consequence for LLM behavior.

## Verification

After completing the exercise, you should be able to prompt the chatbot and get reasonable results, as provided by the LLM. Hallucinations may occur and this is more likely with smaller models in terms of number of active parameters.

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e01_prompting/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e02_system_prompt/README.md)
---|---|---
