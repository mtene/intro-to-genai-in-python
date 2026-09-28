from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import ChatHistory, assistant_message, user_message
from chatbot.services.llm import LLM
from pydantic import BaseModel


# Define your desired structured output format with pydantic
# for more information on pydantic: https://docs.pydantic.dev/latest/why/
class Person(BaseModel):
    name: str
    year_of_birth: int


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with structured outputs"""

    def __init__(self):
        # TODO: study langchain docs on structured outputs
        # https://python.langchain.com/docs/how_to/structured_output/
        self._llm = LLM()
        self._chat_history = ChatHistory()

    @override
    def reset(self) -> None:
        """Reset chatbot to initial state"""
        self._chat_history.clear()

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # record question in chat history
        self._chat_history.add_message(user_message(question))
        # call the LLM with all historic messages
        # TODO: this should return an instance of Person
        response = self._llm.invoke(
            self._chat_history.messages, config=self.get_config(ctx)
        )
        # extract the answer
        # TODO: you need to create a string based on the structured answer
        answer = str(response.content)
        # record answer in chat history
        self._chat_history.add_message(assistant_message(answer))

        return answer
