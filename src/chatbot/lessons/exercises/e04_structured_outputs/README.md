# Exercise 4: Structured outputs

⏱️ **Estimated time**: 20 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Configure LLMs to output structured data conforming to a JSON schema
* Define Pydantic models to represent structured outputs
* Use LangChain's `with_structured_output()` method
* Understand how structured outputs bridge natural language and application logic
* Recognize when to use structured outputs vs free-text responses

## Overview

For this exercise, update the [chatbot logic](chatbot.py) so that answers are no longer free-text. Instead we want the LLM to output an object describing a person, according to the class defined at the top of the file.

## Motivation

Dealing with natural-language inputs is tricky with traditional algorithms. LLMs excel at this, but they are also trained to output natural language. By configuring structured outputs, the LLM is instructed to respond in conformance to a specified JSON schema. This makes the responses straightforward to process with algorithmic code. The LLM thus becomes just another function call, acting as a bridge between user input and application logic.

## How do I do it?

In Python, it is natural to capture type constraints as [Pydantic](https://docs.pydantic.dev/latest/) models - classes with annotated fields, where validation is performed upon instantiation. Such a class describing a `Person` is already provided at the top of the exercise code.

Libraries like LangChain use Pydantic's built-in serialization support to seamlessly configure structured outputs for LLMs. Study the docs on [`with_structured_output()`](https://python.langchain.com/docs/how_to/structured_output/).

## Under the hood

Libraries like LangChain, LangGraph and LlamaIndex abstract away the details of sending structured output schemas to the LLM and retrieving responses. However, understanding this process is instructive.

In the [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create?api-mode=chat), LLM requests include a `response_format` field that controls output format. When unspecified, it defaults to `text`:

```json
"response_format": {
  "type": "text"
}
```

To enable structured outputs, the `type` needs to be changed to `json_schema`.

As an example, let's consider an application which maintains a SQL database of movies, where each entry has the following fields:

```plaintext
title: string, max 500 chars
year: integer, between 0 and 2030
genre: enum, with possible values [horror, comedy, drama, thriller, documentary, biography]
rating: float, between 0.0 and 5.0
```

These rules can be used to build a JSON schema, which is passed to the LLM as the expected output format.

```json
"response_format": {
  "type": "json_schema",
  "json_schema": {
    "title": "Movie",
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "maxLength": 500
      },
      "year": {
        "type": "integer",
        "minimum": 0,
        "maximum": 2030
      },
      "genre": {
        "enum": [
          "horror",
          "comedy",
          "drama",
          "thriller",
          "documentary",
          "biography"
        ],
        "type": "string"
      },
      "rating": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 5.0
      }
    },
    "required": ["title", "year", "genre", "rating"]
  }
}
```

You can find more details on what schema constraints are supported in the [OpenAI API](https://platform.openai.com/docs/guides/structured-outputs#supported-schemas).

When equipped with the configuration above, the LLM can then be used to easily scrape records from social media posts. To express this in Python, we create the following Pydantic model:

```python
from typing import Literal, Annotated
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: Annotated[str, Field(max_length=500)]
    year: Annotated[int, Field(ge=0, le=2030)]
    genre: Literal["horror", "comedy", "drama", "thriller", "documentary", "biography"]
    rating: Annotated[float, Field(ge=0.0, le=5.0)]
```

This is more concise than the JSON schema, which can be easily retrieved by LangChain's `with_structured_output()` via Pydantic's built-in `Movie.model_json_schema()`. In addition, the class can be instantiated to obtain `Movie` objects which are validated on construction - exactly what LangChain does for the LLM output, which arrives as a JSON string, that gets parsed into a `dict` and passed to `Movie.model_validate()` to obtain a `Movie` object.

For example, the below will raise a Pydantic `ValidationError` due to the negative value for the year:

```python
movie = Movie(title="Impossible Movie", year=-1, genre="horror", rating=0.1)
```

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e03_conversation_history/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s04_structured_outputs/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e05_tool_calling/README.md)
---|---|---|---
