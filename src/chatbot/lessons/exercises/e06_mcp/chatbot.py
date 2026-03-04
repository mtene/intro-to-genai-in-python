import logging
import sys
import uuid
from pathlib import Path
from typing import override
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.services.llm import LLM
from chatbot.services.mcp_client import MCPClient

logger = logging.getLogger(__name__)


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with tools from Model Context Protocol servers"""

    def __init__(self):
        # TODO: study langchain.MultiServerMCPClient and figure out how to extend the configuration
        # https://reference.langchain.com/python/langchain_mcp_adapters/#langchain_mcp_adapters.client.MultiServerMCPClient
        mcp_config = {
            # starts a local MCP server on a separate process with communication via stdio
            "my_mcp_server": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(Path(__file__).parent / "mcp_server.py")],
            }
        }
        mcp_client = MCPClient(mcp_config)
        # gather the MCP tools
        mcp_tools = mcp_client.get_tools()
        if not mcp_tools:
            logger.warning("No MCP tools were found!")
        else:
            logger.info(
                f"Available MCP tools:{''.join(f'\n\t{tool.name}' for tool in mcp_tools)}"
            )
        # create an agent that will use the tools
        # MemorySaver checkpointer automatically manages conversation history
        self._agent: CompiledStateGraph = create_agent(
            model=LLM(), tools=mcp_tools, checkpointer=MemorySaver()
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
        # Call the agent with new message
        # Checkpointer automatically loads previous messages and saves new ones
        # also pass ctx so that the agent can publish status updates on tool calls to the UI
        response = self._agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            config={
                **self.get_config(ctx),
                "configurable": {"thread_id": self._thread_id},
            },
        )
        # extract the answer
        # multiple messages may have been generated, the last one is the final response
        answer = str(response["messages"][-1].content)

        return answer
