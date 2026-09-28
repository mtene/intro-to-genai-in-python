from fastmcp import FastMCP

mcp_server = FastMCP("my_mcp_tools")

# TODO: define tools and register them with the MCP server
# using the @mcp_server.tool decoarator

if __name__ == "__main__":
    # start the server with stdio transport for local testing
    mcp_server.run(transport="stdio")
