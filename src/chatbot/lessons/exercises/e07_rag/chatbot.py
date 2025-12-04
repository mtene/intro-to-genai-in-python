import logging
from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import (
    ChatHistory,
    assistant_message,
    user_message,
    system_message,
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
        # create vector store
        self._vectordb = VectorDB()
        # TODO: read the document content from Path(__file__).parents[5] / "data" / "the_great_gatsby.txt"
        # TODO: split the content into chunks representing paragraphs
        # use langchain_text_splitters.RecursiveCharacterTextSplitter
        # TODO: ingest the chunks into the vector store
        # create a list of langchain_core.documents.Document and pass it to self._vectordb.add_documents

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # record question in chat history
        self._chat_history.add_message(user_message(question))
        # search the vector store for the top 10 relevant chunks
        relevant_chunks = self._vectordb.similarity_search(question, k=10)
        logger.info(
            f"Retrieved {len(relevant_chunks)} chunks relevant to the query:{''.join(f'\nChunk {doc.metadata["paragraph"]}: {doc.page_content[:30]}' for doc in relevant_chunks)}"
        )
        system_prompt = system_message(
            f"Respond to the user ONLY based on the following content:\n{'\n'.join(doc.page_content for doc in relevant_chunks)}"
        )
        # call the LLM with the system prompt and all historic messages
        response = self._llm.invoke(
            [system_prompt] + self._chat_history.messages, config=self.get_config(ctx)
        )
        # extract the answer
        answer = str(response.content)
        # record answer in chat history
        self._chat_history.add_message(assistant_message(answer))

        return answer
