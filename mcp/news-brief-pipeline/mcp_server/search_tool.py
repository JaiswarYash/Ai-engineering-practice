import os
import httpx
from mcp.server.mcpserver import MCPServer
from dotenv import load_dotenv

load_dotenv()

server = MCPServer("Search MCP Server")

@server.tool()
async def search(query: str,max_result: int = 5) -> str:
    """Search the web for any topic and return the top results."""
    api_key = os.getenv("TAVILY_API_KEY")

    # Send a POST request to Tavily's search API with the query and result limit
    response = httpx.post(
        "https://api.tavily.com/search",
        json={'query': query, 'max_results': max_result},
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10
    )
    response.raise_for_status()

    results = response.json().get('results', [])

    if not results:
        return 'No result found'

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"... {r.get('content', '')}")
    return "\n\n".join(lines)

if __name__ == "__main__":
    server.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
        stateless_http=True,
        json_response=True,
    )
