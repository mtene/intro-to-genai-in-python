# Solution 6: Model Context Protocol

In the solution, we connect the [chatbot](chatbot.py) to one local and one public Model Context Protocol (MCP) servers.

Run the [tests](tests.py) in the console and verify that they all pass. Remember that LLMs are non-deterministic, so increase repetition count before drawing conclusions. Also consider setting the `seed` parameter or changing `temperature` and `top_p`.

## Implementation: Local MCP tools

In [mcp_server.py](mcp_server.py) we implemented the currency exchange tool and registered it with the local MCP server:

```python
@mcp_server.tool
def convert_currency(...):
    ...
```

Note that the decorator contains the variable holding the MCP server object. This implies that we could have several local MCP servers, each with their own tool set.

## Implementation: MCP configuration

The MCP client's configuration has been extended to include a remote server, specified using their URL and `streamable_http` transport:

```python
mcp_config = {
    # starts a local MCP server on a separate process with communication via stdio
    "my_mcp_server": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [str(Path(__file__).parent / "mcp_server.py")],
    },
    # connects to a remote MCP server using http communication
    "microsoft_learn" : {
        "url": "https://learn.microsoft.com/api/mcp",
        "transport": "streamable_http",
    },
}
```

## Verification

If the connection to the MCP servers is successful, all available tools will be listed in a log message at chatbot creation.

Ask questions about Microsoft software, the current time or currency conversions and verify that the tools get called by observing the status updates.

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e06_mcp/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e07_rag/README.md)
---|---|---
