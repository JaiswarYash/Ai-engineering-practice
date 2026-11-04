# Challenge: News Brief Pipeline

# Build a two-agent system that takes a topic from the user and returns a short written brief on it.

# What to build:

# Agent A — Research Agent uses an MCP server with one tool: a web search or URL fetch tool. It takes the user’s topic, calls the tool, and gets raw content back.
# Agent B — Writer Agent runs as a standalone A2A server. It receives raw content and returns a 3-bullet summary.
# Agent A acts as the A2A client — after researching, it calls Agent B over JSON-RPC and passes the content. Agent B processes it and returns the brief.

# The constraint that makes it real: Agent B must run as a separate process (different port, different script). Agent A cannot import it directly — it can only reach it over the network via A2A.

# Suggested split:
# Day 1 — Build the MCP server (one tool) and get Agent A calling it successfully
# Day 2 — Build Agent B as an A2A server, test it independently with a manual request
# Day 3 — Wire Agent A as the A2A client, run the full pipeline end-to-end

import uvicorn

from a2a.helpers import get_message_text, new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from starlette.applications import Starlette

#===== MCP Client =====#
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def search(query: str)-> str:
    async with streamablehttp_client("127.0.0.1", 8001) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("search", query=query)
            return "\n".join(c.text for c in result.content if c.type == "text")

#===== Research Agent =====#
class ResearchAgentExecutor(AgentExecutor):
    async def execute(self, request_context: RequestContext, event: EventQueue) -> None:
        query = get_message_text(request_context.request)
        