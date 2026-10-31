import os
import httpx
from mcp.server import MCPServer

server = MCPServer("Search MCP Server")

@server.tool()
def search(query: str,max_result: int = 5) -> str:
    """Search the web for any topic and return the top results."""
    api_key = os.environ["TAVILY_API_KEY"]

    # Send a POST request to Tavily's search API with the query and result limit
    response = httpx.post(
        "https://api.tavily.com/search",
        json={'q': query, 'max_result': max_result},
        headers={"Authorization": f"Bearer{api_key}"},
        timeout=10
    )
    response.raise_for_status()

    results = response.json().get('web', {}).get('results', [])

    if not results:
        return 'No result found'

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['title']}\n   {r['url']}\n   {r.get('description', '')}")
    return "\n\n".join(lines)

if __name__ == "__main__":
    server.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
        stateless_http=True,
        json_response=True
    )
