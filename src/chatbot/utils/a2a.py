"""
Utilities for working with A2A (Agent-to-Agent) protocol.

Provides classes to:
- Expose LangChain agents as A2A servers
- Call remote A2A agents as LangChain tools
"""

import logging
import yaml
from pathlib import Path
from typing import Any, Dict, List, override
from urllib.parse import urljoin, urlparse
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from chatbot.services.agent import AgentProtocol
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
    SendMessageResponse,
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

    @override
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

    @override
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
        skills = [
            AgentSkill(
                id=skill.get("id", skill["name"]),
                name=skill["name"],
                description=skill["description"],
                tags=skill.get("tags", []),
            )
            for skill in self._card_data.get("skills", [])
        ]

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
    LangChain tool that calls a specific skill of a remote A2A agent.

    Args:
        agent_url: Base URL of the A2A agent (e.g., "http://127.0.0.1:8002")
        skill_id: The ID of the skill to invoke on the remote agent.
        skill_name: The name of the skill for the LLM tool.
        skill_description: Description of the skill for the LLM tool.
    """

    def __init__(
        self,
        agent_url: str,
        agent_id: str,
        skill_id: str,
        skill_description: str,
        http_client: httpx.Client,
    ):
        super().__init__(name=f"{agent_id}.{skill_id}", description=skill_description)
        self._agent_url = agent_url
        self._agent_id = agent_id
        self._skill_id = skill_id
        self._http_client = http_client

    @override
    def _run(self, query: str) -> str:
        """Called when LLM decides to use this tool"""
        # Construct a message that instructs the remote agent to use a specific skill.
        message_content = f"Execute skill '{self._skill_id}' for query: {query}"

        text_part = TextPart(text=message_content)
        message = Message(
            role=Role.user,
            message_id="1",
            parts=[Part(root=text_part)],
        )
        params = MessageSendParams(message=message)
        request = SendMessageRequest(id=1, params=params)

        try:
            response = self._http_client.post(
                self._agent_url, json=request.model_dump(), timeout=30.0
            )
            response.raise_for_status()
            result = response.json()

            response_data = SendMessageResponse(**result)
            if isinstance(response_data.root, SendMessageSuccessResponse):
                result = response_data.root.result
                if isinstance(result, Message):
                    first_part = result.parts[0].root
                    if isinstance(first_part, TextPart):
                        return first_part.text
            return str(response_data)
        except Exception as e:
            logger.error(
                f"Error calling skill '{self._skill_id}' for A2A agent '{self._agent_id}' at '{self._agent_url}': {repr(e)}"
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
            agent_card = AgentCard(**response.json())

            for skill in agent_card.skills:
                orchestrator_tools.append(
                    A2AAgentTool(
                        agent_url=agent_url,
                        agent_id=agent_id,
                        skill_id=skill.id,
                        skill_description=skill.description,
                        http_client=http_client,
                    )
                )
        except Exception as e:
            logger.error(
                f"Could not load agent card for '{agent_id}' at '{agent_url}': {repr(e)}"
            )
            continue

    return orchestrator_tools
