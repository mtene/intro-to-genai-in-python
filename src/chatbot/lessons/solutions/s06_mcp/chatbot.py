import logging
import sys
from pathlib import Path
from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import ChatHistory, assistant_message, user_message
from chatbot.services.llm import LLM
from chatbot.services.mcp_client import MCPClient
from langgraph.prebuilt import create_react_agent

logger = logging.getLogger(__name__)


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with tools from Model Context Protocol servers"""

    def __init__(self):
        # connect to MCP servers
        mcp_config = {
            # starts a local MCP server on a separate process with communication via stdio
            "my_mcp_server": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(Path(__file__).parent / "mcp_server.py")],
            },
            # connects to two remote MCP servers using http communication
            "microsoft_learn": {
                "url": "https://learn.microsoft.com/api/mcp",
                "transport": "streamable_http",
            },
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
        self._graph = create_react_agent(model=LLM(), tools=mcp_tools)
        self._chat_history = ChatHistory()

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
        # also pass ctx so that the agent can publish status updates on tool calls to the UI
        response = self._graph.invoke(
            {"messages": self._chat_history.messages}, config=self.get_config(ctx)
        )
        # extract the answer
        # multiple messages may have been generated, the last one is the final response
        answer = str(response["messages"][-1].content)
        # record answer in chat history
        self._chat_history.add_message(assistant_message(answer))

        return answer
