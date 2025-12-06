# Solution 4: Structured outputs

The [solution](chatbot.py) configures the LLM to create instances of the `Person` class.

Run the [tests](tests.py) in the console and verify that they all pass. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## Implementation: Structured output configuration

The `Person` class is defined as a Pydantic model, where each field has an associated type

```python
class Person(BaseModel):
    name: str
    year_of_birth: int
```

This can directly be used to configure the LLM for structured outputs

```python
def __init__(self):
    llm = LLM()
    self._llm_structured = llm.with_structured_output(Person)
```

Note that `with_structured_output` creates a new instance of the model. The original `llm` object remains unmodified and would return free-text responses, as usual, if invoked.

Queries are conducted as before

```python
response = self._llm_structured.invoke(self._chat_history.messages, config=self.get_config(ctx))
```

the only difference is the type of the output. We first ensure that no errors had occurred

```python
if not isinstance(response, Person):
    raise ValidationError(f"Failed to generate structured output, got {response}")
```

After this, `response` is guaranteed to be a valid instance of `Person` with all type constraints met.

Finally, the format of the final answer can be defined programmatically, for example

```python
answer = f"{response.name}, born in {response.year_of_birth}"
```

## Verification

Test different queries and confirm that you get the expected formatted output. Also try queries where the answer should contain no references to a person and see what happens!

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e04_structured_outputs/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e05_tool_calling/README.md)
---|---|---
