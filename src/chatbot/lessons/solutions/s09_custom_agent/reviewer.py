from typing import Dict, Any
from pydantic import BaseModel, ValidationError
from chatbot.chat_context import ChatContext
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from chatbot.services.llm import LLM
from .state import GraphState


# reviewer node logic
class ReviewerResponse(BaseModel):
    text_meets_or_exceeds_requirements: bool
    feedback: str


_reviewer_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("""You are a **reviewer** in the editorial process.
Your task is to evaluate the following text

```
{text}
```

Rules:
- Consult the last user query in the conversation context.
- Identify the **minimum requirements explicitly stated or implied by the query**.
- Ignore the ambiguous parts of the query - NEVER assume or invent new criteria.
- Evaluate if the text meets or exceeds these requirements.
- If the text falls short, provide feedback for the author of the text.
- Feedback must:
    * Only describe the changes necessary to address the unmet requirements from the query.
    * Avoid introducing new constraints beyond those implied by the query.
    * Be **brief, clear and actionable""
    * NOT repeat or paraphrase the text.
"""),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

_reviewer_llm = _reviewer_prompt | LLM().with_structured_output(ReviewerResponse)


def reviewer(state: GraphState, config: RunnableConfig) -> Dict[str, Any]:
    """Creates a new state with modified feedback, which may be empty"""
    update_status = ChatContext.from_config(config)
    try:
        response = _reviewer_llm.invoke(
            {"text": state.text, "messages": state.messages}, config=config
        )
    except ValidationError:
        update_status("❌ Reviewer: error")
        return {}
    assert isinstance(response, ReviewerResponse)
    if response.text_meets_or_exceeds_requirements:
        update_status("👍 Reviewer ACCEPT")
        return {"feedback": ""}
    else:
        feedback = str(response.feedback).strip()
        update_status(f"👎 Reviewer REVISE: {feedback}")
        return {"feedback": feedback}
