"""
Utilities for working with A2A (Agent-to-Agent) protocol.

Provides classes to:
- Expose LangChain agents as A2A servers
- Call remote A2A agents as LangChain tools
"""

import logging
import yaml
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from chatbot.services.agent import AgentProtocol
from a2a.client import A2AClient
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    Message,
    Role,
    Part,
    TextPart,
    MessageSendParams,
    SendMessageRequest,
    SendMessageSuccessResponse,
)
import httpx
import uvicorn
import asyncio


logger = logging.getLogger(__name__)


# ============================================================================
# Server: Expose a LangChain agent via A2A protocol
# ============================================================================


class _AgentBridge(AgentExecutor):
    """Bridges synchronous LangChain agent to async A2A protocol."""

    def __init__(self, sync_agent: AgentProtocol):
        self.sync_agent = sync_agent

    async def execute(self, context: Any, event_queue: Any) -> None:
        """Execute the agent with incoming A2A message."""
        # Extract incoming message from A2A request
        message = context.message.parts[0].root.text

        # Run sync agent in background thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.sync_agent.invoke(
                {"messages": [HumanMessage(content=message)]}
            ),
        )

        # Send result back as A2A Message
        answer = result["messages"][-1].content

        # Create response message
        text_part = TextPart(text=str(answer))
        response_message = Message(
            role=Role.agent,
            message_id="response-1",
            parts=[Part(root=text_part)],
        )
        await event_queue.enqueue_event(response_message)

    async def cancel(self, context: Any, event_queue: Any) -> None:
        """Cancel the agent execution (required by AgentExecutor)."""
        pass


class A2AAgent:
    """
    A2A server for a LangChain agent.

    Wraps a synchronous LangChain agent and exposes it via A2A protocol
    so other agents can call it over HTTP.
    """

    def __init__(self, agent: AgentProtocol, agent_card_path: Path):
        """
        Initialize A2A server.

        Args:
            agent: Agent with .invoke() method (e.g., from create_agent())
            agent_card_path: Path to agent_card.yaml file
        """
        self.agent = agent

        # Load agent card from YAML
        with open(Path(agent_card_path), "r") as f:
            self._card_data = yaml.safe_load(f)

    def start(self) -> None:
        """Start the A2A server (blocks until stopped)"""
        # Build skills with defaults for required fields
        skills = []
        for skill in self._card_data.get("skills", []):
            skills.append(
                AgentSkill(
                    id=skill.get("id", skill["name"]),  # Default id to name
                    name=skill["name"],
                    description=skill["description"],
                    tags=skill.get("tags", []),  # Default to empty list
                )
            )

        # Build agent card from YAML data
        agent_card = AgentCard(
            name=self._card_data["name"],
            description=self._card_data["description"],
            url=self._card_data["url"],
            version=self._card_data.get("version", "1.0"),
            capabilities=AgentCapabilities(),
            skills=skills,
            default_input_modes=self._card_data.get("input_modes", ["text"]),
            default_output_modes=self._card_data.get("output_modes", ["text"]),
        )

        # create A2A server with request handler
        handler = DefaultRequestHandler(
            agent_executor=_AgentBridge(self.agent), task_store=InMemoryTaskStore()
        )
        app = A2AStarletteApplication(
            agent_card=agent_card, http_handler=handler
        ).build()

        # parse URL to extract host and port
        parsed_url = urlparse(self._card_data["url"])
        host = parsed_url.hostname
        port = parsed_url.port

        # start listening
        logger.info(
            f"🚀 A2A agent '{self._card_data['name']}' is live at {self._card_data['url']}"
        )
        uvicorn.run(app, host=host, port=port, log_level="warning")


# ============================================================================
# Client: Call remote A2A agents as LangChain tools
# ============================================================================


class A2AAgentTool(BaseTool):
    """
    LangChain tool that calls a remote A2A agent.

    This allows your orchestrator to call remote A2A agents as tools.
    The LLM sees the name and description to decide when to use it.

    Args:
        name: Tool name for the LLM
        description: When to use this tool
        url: A2A agent URL (e.g., "http://127.0.0.1:8002")
    """

    def __init__(self, name: str, description: str, url: str):
        super().__init__(name=name, description=description)
        self._url = url
        self._http = httpx.AsyncClient(timeout=60.0)
        self._client = A2AClient(httpx_client=self._http, url=self._url)

    def _run(self, query: str) -> str:
        """Called when LLM decides to use this tool"""
        # Create A2A message request
        text_part = TextPart(text=query)
        message = Message(
            role=Role.user,
            message_id="1",
            parts=[Part(root=text_part)],
        )
        params = MessageSendParams(message=message)
        request = SendMessageRequest(id=1, params=params)

        # Send message via A2A protocol
        # LangChain expects sync, but A2A is async - use asyncio.run to bridge
        response = asyncio.run(self._client.send_message(request))

        # Extract answer from response
        if isinstance(response.root, SendMessageSuccessResponse):
            result = response.root.result
            if isinstance(result, Message):
                first_part = result.parts[0].root
                if isinstance(first_part, TextPart):
                    return first_part.text
        return str(response)
