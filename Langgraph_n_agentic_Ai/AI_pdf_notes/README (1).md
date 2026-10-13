# Agentic AI Course Notes

Notes from the agentic AI course.

- [Oct 10 — Agentic Framework Ecosystem + DeepAgent](#oct-10--agentic-framework-ecosystem--deepagent) (Instructor: Sunny)
- [Oct 11 — MCP (Model Context Protocol)](#oct-11--mcp-model-context-protocol) (Instructor: Krish)

---

## Oct 10 — Agentic Framework Ecosystem + DeepAgent

**Instructor:** Sunny

### 1. The Framework Landscape

There are 15+ open-source agentic frameworks. You don't need to learn all of them. The course covers five:

| Framework | Notes |
|---|---|
| **LangGraph** | Primary choice — learn deeply. Concepts transfer everywhere. |
| **OpenAI Agent SDK** | Same core concepts as LangGraph, different syntax |
| **Google ADK** | Use if your company is on GCP |
| **Microsoft ADK** | Successor of AutoGen + Semantic Kernel (merged). Use if your company is on Azure. |
| **CrewAI** | Overview only |

**Framework selection rule:** No universal answer. Company ecosystem decides.
- Azure shop → Microsoft ADK
- GCP shop → Google ADK
- No constraint → LangGraph

**Broader ecosystem beyond the five:**

- **Commercial/enterprise platforms** (subscription-based, not open source): OpenAI Agent Builder, Claude Agent SDK, Amazon Bedrock Agent Core, Microsoft Foundry, Vertex AI Agent Builder
- **Low-code/no-code:** N8N, Langflow, Flowwise (automation without deep code)
- **Specialized tools:** Agno, Pydantic AI, DSPy, MetaGPT, etc.

### 2. Three Ways to Build Agentic Systems in LangChain

| Approach | Use For | Complexity |
|---|---|---|
| `create_agent()` | Single ReAct agent, simple tasks | Low |
| `create_deep_agent()` | Complex/long-horizon, multi-agent | Medium–High |
| LangGraph from scratch | Full control, everything custom | High — most recommended |

> **Sunny's honest take:** He never used `create_deep_agent` in production in 3–4 years. It was introduced ~1 year ago. Use it for POCs or if it fits. LangGraph is always the real production choice.

### 3. `create_deep_agent()` — Full Parameter Reference

```python
from deep_agent import create_deep_agent

agent = create_deep_agent(
    model=chat_model,              # LLM to use
    tools=[search_web, ...],       # tools the MAIN agent can call
    system_prompt="...",           # agent's core instructions
    sub_agents=[research, analyst],# list of sub-agent definitions
    skills=["workspace/skills/finance/skill.md"],  # Markdown instruction files
    memory="workspace/memory/agents.md",            # memory file path
    backend=FileSystemBackend(root="workspace"),    # where files live
    interrupt_on=["send_email", "delete_file"],     # HITL trigger conditions
    response_format=ResearchReport,                 # Pydantic schema for output
    context_schema=UserContext,                     # context schema (user_id, role)
    checkpointer=MemorySaver(),                    # in-memory checkpointer
    store=InMemoryStore(),                         # memory store
    name="deep_research_agent"
)
```

**Sub-agent format (dictionary):**

```python
{
    "name": "researcher",
    "description": "...",
    "system_prompt": "...",
    "tools": [search_docs, search_database]  # sub-agent's OWN tool set
}
```

**Key point:** Each sub-agent can have its own set of tools, different from other sub-agents and from the main deep agent. The main agent's tool list and each sub-agent's tool list are independent.

### 4. What Each Component Does

| Component | What it is |
|---|---|
| **Skills** | Markdown instruction files — written instructions defining how an agent should approach a domain (e.g., "You are a finance analyst who…"). Just `.md` files. |
| **Memory** | Another Markdown file containing persistent agent preferences/state |
| **Backend** | File system root — where workspace docs and DB live |
| **interrupt_on** | List of action names that trigger human approval before execution (HITL) |
| **response_format** | Pydantic schema — validates and structures the final output |
| **sub_agents** | List of agent definitions that the main agent delegates to |

### 5. Demo File Structure

```
project/
├── app.py               ← Streamlit UI entry point
├── deep_agent.py        ← build_agent() function; creates the deep agent
├── tools.py             ← tool definitions (search_docs, search_db, send_email, delete_file)
├── setup_data.py        ← creates local docs + SQLite DB for the knowledge base
└── workspace/
    ├── docs/            ← document files (knowledge base)
    ├── company.db       ← SQLite database
    ├── memory/
    │   └── agents.md    ← memory file
    └── skills/
        ├── finance/skill.md
        └── research/skill.md
```

### 6. Sunny's Bottom Line

Use `create_deep_agent` to learn and build POCs. For anything real: **LangGraph** is the better option. The concepts transfer between all frameworks — master LangGraph first, then reading other frameworks becomes straightforward.

---

## Oct 11 — MCP (Model Context Protocol)

**Instructor:** Krish

### 1. The Problem MCP Solves

- **Without MCP:** every AI application needs its own custom integration code for every external system.
  `N apps × M external systems = N×M custom integrations to write and maintain`
- **With MCP:** one standardized protocol. Write the integration once, expose it on a server, any AI app connects to it.

**Analogy:** MCP is the USB-C port of AI apps — one standard that any compatible device can plug into.

> **Important clarification:** MCP does not replace APIs, LLMs, or databases. Everything stays in place. What changes is the way AI applications connect to external systems — that connectivity is now standardized.

### 2. Architecture

```
AI Application (MCP Client)
        ↕  STDIO or HTTP/HTTPS
   MCP Server
        ↕
External System (DB / GitHub / Calendar / Slack / etc.)
```

**Terminology:**
- **MCP Client** — any AI application (your LangChain app, Claude Code, GitHub Copilot, etc.)
- **MCP Server** — the server that hosts your tools/resources/prompts
- **MCP Host** — the full application the user interacts with (less critical term; client and host are often treated as synonymous)

### 3. What You Can Expose on an MCP Server

Three types — remember them as **do / know / guide**:

| Type | What it is | Example |
|---|---|---|
| **Tools** (do) | Executable functions — things the agent does | `search_flight`, `book_hotel`, `send_email` |
| **Resources** (know) | Data the app reads and provides to the model as context | Company policies, travel preferences, calendar events |
| **Prompts** (guide) | Reusable instruction templates | "plan_vacation" template, "book_flight" template |

**Code pattern (using `mcp` package):**

```python
from mcp.server import MCPServer

mcp = MCPServer("my_server")

@mcp.tool          # → this function is a TOOL
def search_flight(origin, destination):
    ...

@mcp.resource      # → this function exposes a RESOURCE
def get_company_policy():
    ...

@mcp.prompt        # → this function exposes a PROMPT template
def plan_vacation():
    ...
```

The decorator (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`) is what categorizes each function. `mcp` is just your variable name for the `MCPServer` instance.

### 4. Transport Methods

| Transport | Use When |
|---|---|
| **STDIO** | Client and server are on the same machine (local development, testing) |
| **HTTP / HTTPS** | Client and server are on different machines (deployed server, remote access) |

**Practical decision:** building locally and testing → STDIO. Hosting on AWS/GCP and connecting from another app → HTTP.

### 5. Three Packages

| Package | Source | Use Case |
|---|---|---|
| `mcp` | Anthropic (official Python SDK) | Core package — everything is available from here, including `MCPServer` |
| `fastmcp` | PrefectHQ (community wrapper) | Simpler API on top of `mcp`; in the latest `mcp` versions, the `FastMCP` class is available from `mcp` directly |
| `langchain-mcp-adapter` | LangChain | Use when building LangChain-based agents (what the course projects will use) |

**Course project approach:** `langchain-mcp-adapter` for the main projects. Krish will also show `mcp` and `fastmcp` for comparison.

### 6. A2A (Agent-to-Agent Protocol)

Mentioned briefly — not covered in this session. A small concept coming in a future class. It is **not** a replacement for MCP (different purpose): MCP is AI → external system; A2A is agent → agent.
