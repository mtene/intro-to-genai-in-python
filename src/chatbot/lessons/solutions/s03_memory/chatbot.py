from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import ChatHistory, assistant_message, user_message
from chatbot.services.llm import LLM


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with conversation history"""

    def __init__(self):
        self._llm = LLM()
        # create a chat history object to keep track of conversation messages
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
        response = self._llm.invoke(
            self._chat_history.messages, config=self.get_config(ctx)
        )
        # extract the answer
        answer = str(response.content)
        # record answer in chat history
        # bonus: prune this to the last 5 question-answer pairs
        self._chat_history.add_message(assistant_message(answer))

        return answer
