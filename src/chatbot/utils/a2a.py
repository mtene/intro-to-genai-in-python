"""
Utilities for working with A2A (Agent-to-Agent) protocol.

Provides classes to:
- Expose LangChain agents as A2A servers
- Call remote A2A agents as LangChain tools
"""

import asyncio
import logging
import yaml
from pathlib import Path
from typing import Any, Dict, List, override
from urllib.parse import urljoin, urlparse

import httpx
import uvicorn
from a2a.client import ClientConfig, create_client
from a2a.client.card_resolver import parse_agent_card
from a2a.helpers import get_message_text, get_stream_response_text, new_text_message
from a2a.server.agent_execution import AgentExecutor
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
    Role,
    SendMessageRequest,
)
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from starlette.applications import Starlette

from chatbot.services.agent import AgentProtocol


logger = logging.getLogger(__name__)


# ============================================================================
# Sync/async adapters — lesson code stays synchronous
# ============================================================================


class _A2AServerBridge(AgentExecutor):
    """Inbound: bridges a synchronous LangChain agent to the async A2A server."""

    def __init__(self, sync_agent: AgentProtocol):
        self.sync_agent = sync_agent

    @override
    async def execute(self, context: Any, event_queue: Any) -> None:
        """Execute the agent with incoming A2A message."""
        message = get_message_text(context.message)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.sync_agent.invoke(
                {"messages": [HumanMessage(content=message)]}
            ),
        )

        answer = result["messages"][-1].content
        await event_queue.enqueue_event(
            new_text_message(str(answer), role=Role.ROLE_AGENT)
        )

    @override
    async def cancel(self, context: Any, event_queue: Any) -> None:
        """Cancel the agent execution (required by AgentExecutor)."""
        pass


class _A2AClientBridge:
    """Outbound: bridges a synchronous LangChain tool to the async A2A client."""

    def __init__(self, agent_url: str, skill_id: str):
        self._agent_url = agent_url
        self._skill_id = skill_id

    async def _send(self, query: str) -> str:
        message_content = f"Execute skill '{self._skill_id}' for query: {query}"
        client = await create_client(
            self._agent_url,
            client_config=ClientConfig(streaming=False),
        )
        request = SendMessageRequest(
            message=new_text_message(message_content, role=Role.ROLE_USER)
        )

        result_text = ""
        async for chunk in client.send_message(request):
            text = get_stream_response_text(chunk)
            if text:
                result_text = text
        return result_text or "No response"

    def call_skill(self, query: str) -> str:
        """Synchronous entry point for LangChain tool execution."""
        return asyncio.run(self._send(query))


# ============================================================================
# Server: Expose a LangChain agent via A2A protocol
# ============================================================================


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

        with open(Path(agent_card_path), "r", encoding="utf-8") as f:
            self._card_data = yaml.safe_load(f)

    def _build_agent_card(self) -> AgentCard:
        skills = [
            AgentSkill(
                id=skill.get("id", skill["name"]),
                name=skill["name"],
                description=skill["description"],
                tags=skill.get("tags", []),
            )
            for skill in self._card_data.get("skills", [])
        ]

        capabilities_cfg = self._card_data.get("capabilities", {})
        service_url = self._card_data["url"].rstrip("/") + "/"

        return AgentCard(
            name=self._card_data["name"],
            description=self._card_data["description"],
            version=self._card_data.get("version", "1.0"),
            supported_interfaces=[
                AgentInterface(
                    protocol_binding="JSONRPC",
                    url=service_url,
                )
            ],
            capabilities=AgentCapabilities(
                streaming=capabilities_cfg.get("streaming", False),
            ),
            skills=skills,
            default_input_modes=self._card_data.get("input_modes", ["text"]),
            default_output_modes=self._card_data.get("output_modes", ["text"]),
        )

    def start(self) -> None:
        """Start the A2A server (blocks until stopped)"""
        agent_card = self._build_agent_card()
        handler = DefaultRequestHandler(
            agent_executor=_A2AServerBridge(self.agent),
            task_store=InMemoryTaskStore(),
            agent_card=agent_card,
        )

        routes = []
        routes.extend(create_agent_card_routes(agent_card))
        routes.extend(create_jsonrpc_routes(handler, rpc_url="/"))
        app = Starlette(routes=routes)

        parsed_url = urlparse(self._card_data["url"])
        host = parsed_url.hostname or "127.0.0.1"
        port = parsed_url.port

        logger.info(
            f"🚀 A2A agent '{self._card_data['name']}' is live at {self._card_data['url']}"
        )
        uvicorn.run(app, host=host, port=port, log_level="warning")


# ============================================================================
# Client: Call remote A2A agents as LangChain tools
# ============================================================================


class A2AAgentTool(BaseTool):
    """
    LangChain tool that calls a specific skill of a remote A2A agent.

    Args:
        agent_url: Base URL of the A2A agent (e.g., "http://127.0.0.1:8002")
        skill_id: The ID of the skill to invoke on the remote agent.
        skill_description: Description of the skill for the LLM tool.
    """

    def __init__(
        self,
        agent_url: str,
        agent_id: str,
        skill_id: str,
        skill_description: str,
    ):
        super().__init__(name=f"{agent_id}.{skill_id}", description=skill_description)
        self._agent_url = agent_url
        self._agent_id = agent_id
        self._skill_id = skill_id
        self._client = _A2AClientBridge(agent_url, skill_id)

    @override
    def _run(self, query: str) -> str:
        """Called when LLM decides to use this tool"""
        try:
            return self._client.call_skill(query)
        except Exception as e:
            logger.error(
                f"Error calling skill '{self._skill_id}' for A2A agent "
                f"'{self._agent_id}' at '{self._agent_url}': {repr(e)}"
            )
            return f"Error: {str(e)}"


def create_tools_from_a2a_agent_skills(config: Dict[str, Any]) -> List[BaseTool]:
    """
    Creates a list of LangChain tools for interacting with A2A agent skills.
    Args:
        agents_config: a dictionary, giving 'name' and 'url' for each A2A agent.
    Returns:
        A list of BaseTool instances, one for each agent skill or agent.
    """
    if "agents" not in config:
        logger.error("Invalid A2A agent configuration")
        return []

    orchestrator_tools = []
    http_client = httpx.Client(timeout=60.0)

    for agent_config in config["agents"]:
        agent_id = agent_config["id"]
        agent_url = agent_config["url"]

        try:
            agent_card_url = urljoin(agent_url, "/.well-known/agent-card.json")
            response = http_client.get(agent_card_url)
            response.raise_for_status()
            agent_card = parse_agent_card(response.json())

            for skill in agent_card.skills:
                orchestrator_tools.append(
                    A2AAgentTool(
                        agent_url=agent_url,
                        agent_id=agent_id,
                        skill_id=skill.id,
                        skill_description=skill.description,
                    )
                )
        except Exception as e:
            logger.error(
                f"Could not load agent card for '{agent_id}' at '{agent_url}': {repr(e)}"
            )
            continue

    return orchestrator_tools
