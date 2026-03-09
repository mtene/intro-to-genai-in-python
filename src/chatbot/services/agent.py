"""Agent protocol for type checking."""

from typing import Any, Protocol


class AgentProtocol(Protocol):
    """Protocol for objects that can be used as agents.

    This allows both real LangChain agents (CompiledStateGraph) and
    placeholder/mock agents to be used interchangeably.
    """

    def invoke(self, *args: Any, **kwargs: Any) -> Any:
        """Invoke the agent with input and optional config.

        Accepts flexible arguments to match both CompiledStateGraph
        and simple placeholder agents.
        """
        ...
