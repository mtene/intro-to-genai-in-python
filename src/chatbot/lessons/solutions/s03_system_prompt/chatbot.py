from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import user_message, system_message
from chatbot.services.llm import LLM


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with system prompt"""

    def __init__(self):
        self._llm = LLM()
        # create a static system prompt
        self._system_prompt = """Your role is given by type of user message:
- if it is a question, you have a bubbly personality
- otherwise, you are lazy and slow"""

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # assemble chat history from the system message and user question
        messages = [system_message(self._system_prompt), user_message(question)]
        # call the LLM
        response = self._llm.invoke(messages, config=self.get_config(ctx))
        # extract the answer
        answer = str(response.content)

        return answer
