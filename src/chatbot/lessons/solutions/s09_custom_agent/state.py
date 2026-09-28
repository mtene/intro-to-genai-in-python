from pydantic import BaseModel
from typing import List
from chatbot.chat_history import ChatMessage


# define the state as a Pydantic model
class GraphState(BaseModel):
    messages: List[ChatMessage]
    text: str = ""
    feedback: str = ""
    iteration: int = 1
