"""Travel Planning Orchestrator - Coordinates expert agents via A2A protocol"""

import uuid
import yaml
from pathlib import Path
from typing import override
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.services.llm import LLM
from chatbot.utils.a2a import A2AAgentTool


class ChatBot(BaseChatBot):
    """Orchestrator that delegates to expert agents via A2A protocol"""

    def __init__(self):
        llm = LLM()

        # Load agents configuration from YAML
        with open(Path(__file__).parent / "agents.yaml", "r") as f:
            config = yaml.safe_load(f)

        # Create A2A tools from configuration
        agents = [
            A2AAgentTool(
                name=agent["name"],
                description=agent["description"],
                url=agent["url"],
            )
            for agent in config["agents"]
        ]

        # Create orchestrator agent with A2A agents as tools
        # The LLM decides which to consult based on the user's question
        system_prompt = """You are an orchestrator with access to expert agents. Always delegate questions to the appropriate expert rather than answering directly."""

        self._agent: CompiledStateGraph = create_agent(
            model=llm,
            tools=agents,
            system_prompt=system_prompt,
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

        # Call orchestrator agent
        # The agent will decide which expert(s) to consult via A2A
        # Checkpointer automatically manages conversation history
        result = self._agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            config={
                **self.get_config(ctx),
                "configurable": {"thread_id": self._thread_id},
            },
        )

        # Extract final answer
        answer = str(result["messages"][-1].content)
        return answer
