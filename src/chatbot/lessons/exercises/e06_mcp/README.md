# Exercise 6: Model Context Protocol

In this exercise, you will equip the [chatbot](chatbot.py) with 3rd party tools hosted on Model Context Protocol (MCP) servers.

## Motivation

Giving agents access to tools augments their capabilities with new data sources and the ability to take actions. Self-defined tools limit this to the systems under our control or those with public APIs. What if we need to enable interaction with a black-box?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) solves this by standardizing the way tools are exposed for LLM use. Using it, a 3rd party can wrap proprietary functionality in tools that can be consumed by clients without knowledge of the internals - only the required arguments and type of the expected result.

## How do I do it?

The exercise code already instantiates an MCP client in the constructor

```python
def __init__(self):
    mcp_client = MCPClient(mcp_config)
    mcp_tools = mcp_client.get_tools()
```

## Local MCP server

The MCP connection configuration contains a local server which will be started in a separate process. Communication will happen via console messages (standard I/O).

```python
mcp_config = {
    "my_mcp_server": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [str(Path(__file__).parent / "mcp_server.py")],
    }
}
```

The MCP server logic is defined using [FastMCP](https://github.com/jlowin/fastmcp) in [`mcp_server.py`](mcp_server.py). Notice that there are no tools defined yet.

```python
mcp_server = FastMCP("my_mcp_tools")

if __name__ == "__main__":
    mcp_server.run(transport="stdio")
```

Your first task is to populate the local server with one or more tools and register them by using the `@mcp_server.tool` decorator. Use, for example, the currency conversion tool from the previous exercise.

```python
@mcp_server.tool
def sum_tool(a: int, b: int) -> int:
    return a + b 
```

With this in-place, the tool name should appear in a log message at the console during chatbot construction.

## Remote MCP server

The power of MCP lies in reusing tools defined by others. To leverage this, extend the MCP configuration to connect to public MCP servers on the internet using `streamable_http` transport. Be mindful that tools allow an LLM to execute code controlled externally, which could be exploited for malicious purposes. Therefore, only use MCP servers from reputable vendors and take proactive steps to minimize the attack surface (e.g. hosting the app in a container or VM with limited privileges).

Some examples suitable for this exercise:

* Microsoft Learn MCP: `https://learn.microsoft.com/api/mcp`
* Time utilities MCP: `https://time.mcp.inevitable.fyi/mcp`

## Under the hood

Instead of diving into the detailed structure of the MCP protocol, it is sufficient to discuss the high-level communication pattern.

![MCP Communication](/images/mcp.png)

An MCP server can be hosted locally, on a private intranet or the public internet. Remote servers typically communicate over http or websocket, while local servers may additionally use standard console I/O. Clients connect to the server and send tool call requests via JSON-RPC messages, indicating the tool name and corresponding values for its arguments. For http, the headers are populated with authentication information, if required. The server then executes the tool and returns the result in its reply. In addition, servers can also stream logs or status updates back to the client during execution, so that the client can track progress while waiting for the final output.

## Further reading

MCP clients and server implementations make use of asynchronous programming. This allows input-output-bound operations to execute concurrently without blocking the execution loop. This aspect is abstracted away in the exercise code via the `MCPClient` wrapper. Knowledge and experience with [`async`](https://realpython.com/async-io-python/) is, nonetheless, essential for production-grade applications.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e05_tool_calling/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s06_mcp/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e07_rag/README.md)
---|---|---|---
