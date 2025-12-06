from dataclasses import dataclass, field
from enum import Enum
from typing import List
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage


class ChatRole(Enum):
    """Represents the role in the conversation of a chat message's sender"""

    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"
    TOOL = "tool"


ChatMessage = BaseMessage
"""An entry in the chat history"""


def system_message(content: str) -> ChatMessage:
    """Creates a system chat message, containing instructions for the LLM"""
    return SystemMessage(content=content)


def user_message(content: str) -> ChatMessage:
    """Creates a chat message sent by the user"""
    return HumanMessage(content=content)


def assistant_message(content: str) -> ChatMessage:
    """Creates a chat message sent by the assistant"""
    return AIMessage(content=content)


def get_messages_from(messages: List[ChatMessage], role: ChatRole) -> List[ChatMessage]:
    """Returns all messages from the specified sender"""
    return [message for message in messages if message.type == role.value]


def get_last_message_from(messages: List[ChatMessage], role: ChatRole) -> ChatMessage:
    """Returns the latest message from the specified sender"""
    filtered_messages = get_messages_from(messages, role)
    assert len(filtered_messages) > 0
    return filtered_messages[-1]


@dataclass
class ChatHistory:
    """Records the conversation messages"""

    messages: List[ChatMessage] = field(default_factory=list)

    def get_messages_from(self, role: ChatRole) -> List[ChatMessage]:
        return get_messages_from(self.messages, role)

    def get_last_message_from(self, role: ChatRole) -> ChatMessage:
        return get_last_message_from(self.messages, role)

    def add_message(self, message: ChatMessage) -> None:
        """Appends a message to the back of the chat history"""
        self.messages.append(message)

    def clear(self) -> None:
        self.messages.clear()
