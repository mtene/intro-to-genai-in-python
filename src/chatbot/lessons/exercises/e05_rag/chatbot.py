import logging
from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import (
    ChatHistory,
    assistant_message,
    user_message,
)
from chatbot.services.llm import LLM
from chatbot.services.vectordb import VectorDB

logger = logging.getLogger(__name__)


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with Retrieval Augmented Generation"""

    def __init__(self):
        self._llm = LLM()
        self._chat_history = ChatHistory()
        self._build_vector_store()

    def _build_vector_store(self) -> None:
        """Chunks the document and populates a vector database with the content"""
        # create vector store
        self._vectordb = VectorDB()
        # TODO: read the document content from Path(__file__).parents[5] / "data" / "the_great_gatsby.txt"
        # TODO: split the content into chunks representing paragraphs
        # e.g. using langchain_text_splitters.RecursiveCharacterTextSplitter
        # TODO: ingest the chunks into the vector store
        # create a list of langchain_core.documents.Document and pass it to self._vectordb.add_documents

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
        # TODO: fetch relevant chunks to the query from the vector store
        # record question in chat history
        self._chat_history.add_message(user_message(question))
        # call the LLM with all historic messages
        # TODO: include the chunks in the messages passed to the LLM
        response = self._llm.invoke(
            self._chat_history.messages, config=self.get_config(ctx)
        )
        # extract the answer
        answer = str(response.content)
        # record answer in chat history
        self._chat_history.add_message(assistant_message(answer))

        return answer
