import uuid
from pathlib import Path
from typing import override
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.services.llm import LLM


class ChatBot(BaseChatBot):
    """Uses a DeepAgent with custom skills"""

    def __init__(self):
        llm = LLM()

        # Make the lessons folder the filesystem root for the agent
        root_path = Path(__file__).parent.parent.parent

        # Convert skills path to POSIX format (DeepAgents limitation on Windows)
        skills_path = (
            f"/{(Path(__file__).parent / 'skills').relative_to(root_path).as_posix()}/"
        )

        # Create the DeepAgent with loaded skills
        # LocalShellBackend provides filesystem access (rooted at root_path)
        # MemorySaver provides in-memory conversation history management
        self._agent = create_deep_agent(
            model=llm,
            skills=[skills_path],
            backend=LocalShellBackend(root_dir=root_path, virtual_mode=True),
            system_prompt="Always use a skill when one matches the user's request.",
            checkpointer=MemorySaver(),
        )
        self._thread_id = str(uuid.uuid4())

    @override
    def reset(self) -> None:
        """Reset chatbot to initial state"""
        # Generate new thread ID to start fresh conversation
        self._thread_id = str(uuid.uuid4())

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")

        # Call DeepAgent with new message
        # Checkpointer automatically manages conversation history
        result = self._agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            config={
                **self.get_config(ctx),
                "configurable": {"thread_id": self._thread_id},
            },
        )
        # Extract final answer from the last message
        answer = str(result["messages"][-1].content)

        return answer
