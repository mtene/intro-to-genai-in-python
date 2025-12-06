# Exercise 6: Model Context Protocol

⏱️ **Estimated time**: 30 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Understand the purpose and architecture of the Model Context Protocol (MCP)
* Set up and connect to MCP servers from Python applications
* Integrate 3rd party MCP tools into LangGraph agents
* Explain the client-server communication flow in MCP

## Overview

In this exercise, you will equip the [chatbot](chatbot.py) with 3rd party tools hosted on Model Context Protocol (MCP) servers.

## Motivation

Tools augment agent capabilities with new data sources and the ability to take actions. However, self-defined tools limit us to systems under our control or those with public APIs. What if we need to interact with a black-box system?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) solves this by standardizing how tools are exposed for LLM use. Third parties can wrap proprietary functionality in tools that clients can consume without knowing the internals - only the required arguments and expected result type.

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

For this exercise, we will use the Microsoft Learn MCP server `https://learn.microsoft.com/api/mcp`.

## Under the hood

Rather than diving into the detailed MCP protocol structure, let's focus on the high-level communication pattern:

![MCP Communication](/images/mcp.png)

MCP servers can be hosted locally, on a private intranet, or on the public internet. Remote servers typically communicate over HTTP or WebSocket; local servers may additionally use standard console I/O.

**Communication flow**:

1. Clients connect to the server
1. Clients send tool call requests via JSON-RPC messages (specifying the tool name and argument values)
1. For HTTP, headers include authentication information if required
1. The server executes the tool and returns results
1. During execution, servers can stream logs or status updates so clients can track progress

## Further reading

MCP clients and server implementations make use of asynchronous programming. This allows input-output-bound operations to execute concurrently without blocking the execution loop. This aspect is abstracted away in the exercise code via the `MCPClient` wrapper. Knowledge and experience with [`async`](https://realpython.com/async-io-python/) is, nonetheless, essential for production-grade applications.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e05_tool_calling/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s06_mcp/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e07_rag/README.md)
---|---|---|---
