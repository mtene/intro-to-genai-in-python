import asyncio
from langchain_core.tools import StructuredTool

from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import Dict, Any


class MCPClient:
    """
    Connects to one or more MCP servers, as specied in the configuration dictionary.
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
        self._client = MultiServerMCPClient(config)

    def get_tools(self):
        tools = asyncio.run(self._client.get_tools())
        # StructuredTool can only be called async, so define a wrapper
        return [
            StructuredTool.from_function(
                func=lambda *args, tool=tool, **kwargs: asyncio.run(
                    tool.arun(args=args, **kwargs)
                ),
                name=tool.name,
                description=tool.description,
                args_schema=getattr(tool, "args_schema", None),
            )
            for tool in tools
        ]
