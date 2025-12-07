from typing import Dict, Any
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from chatbot.chat_context import ChatContext
from langchain_core.runnables import RunnableConfig
from chatbot.services.llm import LLM
from .state import GraphState


# author node logic
_author_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("""You are an **author** in the editorial process.
Your task is to improve the following text:

```
{text}
```

based on this feedback: `{feedback}`.

Rules:
- Consult the last user query in the conversation context.
- Identify the **minimum requirements explicitly stated or implied by the query**.
- Ignore the ambiguous parts of the query - NEVER assume or invent new criteria
- Apply the feedback to satisfy them, without introducing unrelated changes
- Preserve the original meaning, tone and style as much as possible.
- Respond with the revised text **only** - no quotation marks, explanations or extra commentary.
- If the feedback is ambiguous, resolve it minimally while keeping the text aligned with the query.
- Stop editing once the requirements and feedback are fully addressed.
"""),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

_author_llm = _author_prompt | LLM()


def author(state: GraphState, config: RunnableConfig) -> Dict[str, Any]:
    """Creates a new state with modified text"""
    update_status = ChatContext.from_config(config)
    response = _author_llm.invoke(
        {"text": state.text, "feedback": state.feedback, "messages": state.messages},
        config=config,
    )
    text = str(response.content).strip()
    update_status(f"🧠 Author: {text}")
    return {"text": text}
