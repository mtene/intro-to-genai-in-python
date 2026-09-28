from typing import Dict, Any
from chatbot.chat_context import ChatContext
from langchain_core.runnables import RunnableConfig
from .state import GraphState


# reviewer node logic
def reviewer(state: GraphState, config: RunnableConfig) -> Dict[str, Any]:
    """Creates a new state with modified feedback, which can be empty"""
    update_status = ChatContext.from_config(config)
    # TODO: add the logic to populate feedback
    feedback = ""
    if not feedback:
        update_status("👍 Reviewer: ACCEPT")
    else:
        update_status(f"👎 Reviewer: {feedback}")
    return {"feedback": feedback}
