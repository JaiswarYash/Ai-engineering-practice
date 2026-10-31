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