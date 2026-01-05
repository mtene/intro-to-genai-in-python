import logging
from pathlib import Path
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
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
        # read the document content
        doc_path = Path(__file__).parents[5] / "data" / "the_great_gatsby.txt"
        doc_content = ""
        with open(doc_path, encoding="utf-8") as f:
            doc_content = f.read()
        # split the content into chunks representing paragraphs
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n"],
            chunk_size=2000,
            chunk_overlap=0,
        )
        doc_chunks = splitter.split_text(doc_content)
        logger.info(f"Split {doc_path} into {len(doc_chunks)} chunks")
        # ingest the chunks into the vector store
        self._vectordb.add_documents(
            [
                Document(
                    page_content=chunk,
                    metadata={"document": str(doc_path), "paragraph": i + 1},
                )
                for i, chunk in enumerate(doc_chunks)
            ]
        )

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
        # search the vector store for the top 10 relevant chunks
        relevant_chunks = self._vectordb.similarity_search(question, k=10)
        logger.info(
            f"Retrieved {len(relevant_chunks)} chunks relevant to the query:{''.join(f'\nChunk {doc.metadata["paragraph"]}: {doc.page_content[:30]}' for doc in relevant_chunks)}"
        )
        # augment the user question with the retrieved context
        augmented_question = f"""Answer the following question using ONLY the information in the numbered paragraphs below.
You MUST cite which paragraph number(s) you used in your answer (e.g., "According to paragraph 3..."). If the answer is not in any paragraph, say 'I cannot answer based on the provided context.'

{"\n\n".join(f"{doc.metadata['paragraph']}. {doc.page_content}" for doc in relevant_chunks)}

Question: {question}"""
        # call the LLM with the augmented question and all historic messages
        response = self._llm.invoke(
            self._chat_history.messages + [augmented_question],
            config=self.get_config(ctx),
        )
        # extract the answer
        answer = str(response.content)
        # record original question and answer in chat history
        self._chat_history.add_message(user_message(question))
        self._chat_history.add_message(assistant_message(answer))

        return answer
