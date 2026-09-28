from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import user_message
from chatbot.services.llm import LLM


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with conversation history"""

    def __init__(self):
        self._llm = LLM()

    @override
    def reset(self) -> None:
        """Reset chatbot to initial state"""
        # TODO: don't forget to clear chat history here!
        pass

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # TODO: study ChatHistory in chat_history.py
        messages = [user_message(question)]
        # call the LLM
        response = self._llm.invoke(messages, config=self.get_config(ctx))
        # extract the answer
        answer = str(response.content)

        return answer
