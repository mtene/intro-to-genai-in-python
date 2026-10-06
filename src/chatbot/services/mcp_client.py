import asyncio
from typing import Any, Dict, List

from langchain_core.tools import BaseTool, StructuredTool
from langchain_mcp_adapters.client import MultiServerMCPClient

_FASTMCP_STDIO_ENV = {
    "FASTMCP_SHOW_SERVER_BANNER": "false",
    "FASTMCP_CHECK_FOR_UPDATES": "off",
    "FASTMCP_LOG_ENABLED": "false",
}


class MCPClient:
    """
    Connects to one or more MCP servers, as specified in the configuration dictionary.
    Stdio servers get ``FASTMCP_*`` env vars (MCP subprocesses do not inherit the full parent env).

    Example:
        mcp_config = {
            "mcp_tools": {
                "transport": "streamable_http",
                "url": "https://example.com:1234/mcp"
            }
        }
        mcp_client = MCPClient(mcp_config)
        tools = mcp_client.get_tools()
    """

    def __init__(self, config: Dict[str, Any]):
        for server in config.values():
            if isinstance(server, dict) and server.get("transport") == "stdio":
                server["env"] = {**_FASTMCP_STDIO_ENV, **(server.get("env") or {})}
        self._client = MultiServerMCPClient(config)

    def get_tools(self) -> List[BaseTool]:
        tools = asyncio.run(self._client.get_tools())
        # StructuredTool can only be called async, so define a wrapper
        return [
            StructuredTool.from_function(
                func=lambda tool=tool, **kwargs: asyncio.run(tool.arun(kwargs)),
                name=tool.name,
                description=tool.description,
                args_schema=getattr(tool, "args_schema", None),
            )
            for tool in tools
        ]
