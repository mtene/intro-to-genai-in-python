from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import ChatHistory, user_message, assistant_message
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
        # a "vanilla" LLM instance - text in, text out
        llm = LLM()
        # we now configure the LLM to produce a Person object
        self._llm_structured = llm.with_structured_output(Person)
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
        response = self._llm_structured.invoke(
            self._chat_history.messages, config=self.get_config(ctx)
        )
        # the output should be an instance of Person
        if not isinstance(response, Person):
            # unless an error had occurred
            raise ValueError(f"Failed to generate structured output, got {response}")
        # we can now rely on having a valid Person
        answer = f"{response.name}, born in {response.year_of_birth}"
        # record answer in chat history
        self._chat_history.add_message(assistant_message(answer))

        return answer
