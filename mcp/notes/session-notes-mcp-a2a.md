# Session Notes: MCP & A2A
**Course:** Generative AI Engineering — Krish Naik Academy  
**Topics:** Model Context Protocol (MCP) · Agent-to-Agent Protocol (A2A)

---

## Oct 11 — MCP Introduction
**Instructor:** Krish Naik

### The Problem MCP Solves
Without MCP, every AI app needs custom code to talk to every external tool.

```
10 AI apps × 20 tools = 200 custom integrations to build & maintain
```

With MCP, each tool writes **one server** and each app writes **one client**:

```
10 apps + 20 tools = 30 total integrations
```

Think of MCP like **USB-C** — one standard connector that works with everything, instead of a different cable per device.

### What is MCP?
**Model Context Protocol** — an open standard introduced by Anthropic.  
It standardizes how AI applications connect to external tools, data sources, and resources.

### Architecture

```
[ MCP Client ]  ←──── protocol ────→  [ MCP Server ]
  (AI App)                             (hosts tools, resources, prompts)
```

- **MCP Client** = your AI application (e.g., a LangChain agent)
- **MCP Server** = the thing that hosts what the AI can use

### What a Server Can Host
| Type | What it is |
|---|---|
| Tools | Functions the AI can call (e.g., search, query a DB) |
| Resources | Data the AI can read (e.g., files, docs) |
| Prompts | Pre-built prompt templates |

### Transport Types
| Transport | Use when |
|---|---|
| **STDIO** | Client and server on the **same machine** (local) |
| **HTTP / SSE** | Server is hosted **remotely** (network) |

### Key Python Packages
| Package | Who made it | Purpose |
|---|---|---|
| `mcp` | Anthropic | Official SDK — base protocol |
| `fastmcp` | Zeri Mian (community) | Simpler wrapper for building MCP servers |
| `langchain-mcp-adapter` | LangChain | Connect LangChain agents to MCP servers |

---

## Oct 22 — MCP Extended + A2A Theory
**Instructor:** Sunny Savita

### MCP Extended: Business Trip Co-Pilot Project
- Same MCP concepts applied to a real project
- Used **HTTP transport** (not STDIO) — servers run locally but can be swapped for cloud URLs
- Demonstrated that MCP servers can host tools that call real APIs (flights, hotels, etc.)

### A2A — First Look (Theory Only)
**A2A = Agent-to-Agent Protocol**, introduced by **Google** in 2025.

- MCP connects agents to **external tools**
- A2A connects **agents to agents**
- They solve different problems — both can exist in the same system

### Coming Up (announced)
- Evaluation libraries: **RAGAS** and **DeepEval**
- **LangSmith** = monitoring/observability only — it is NOT an evaluation tool
- Next: A2A practical + Evaluation concepts

---

## Oct 24 — A2A Practical + MCP HTTP Demo
**Instructor:** Sunny Savita

### MCP HTTP Multi-Server Demo
Running multiple MCP servers at the same time for a single AI application.

**Project structure (Business Trip Co-Pilot):**
```
app_http.py          ← MCP Client (AI application)
startServer.py       ← Script that launches all 3 servers at once
  ├── policy_server.py     ← Hosts travel policy data (uses RAG/vector DB)
  ├── travel_server.py     ← Hosts flight search tools
  └── work_server.py       ← Hosts task management tools
```

**How to run:**
1. Start all servers: `python startServer.py`
2. Run the client: `python app_http.py`
3. Client connects to all 3 servers via their localhost URLs

**Key insight:** HTTP transport URLs (e.g., `http://localhost:8001`) can be replaced with cloud URLs (AWS, Azure) for production deployment with zero code change.

---

### A2A — Full Explanation

#### The Problem A2A Solves
Different AI agents are built with different frameworks:

| Framework | Who made it |
|---|---|
| LangGraph | LangChain |
| ADK (Agent Development Kit) | Google |
| Agents SDK | OpenAI |
| AutoGen | Microsoft |

Without A2A, if Agent A (built in LangGraph) wants to talk to Agent B (built in ADK), you need custom integration code. 10 agents = many custom integrations.

**A2A is framework-independent** — it doesn't matter which framework built an agent. If both implement A2A, they can communicate.

#### MCP vs A2A — Side by Side

| | MCP | A2A |
|---|---|---|
| **Connects** | Agent ↔ External tools/data | Agent ↔ Agent |
| **Purpose** | Standardize tool access | Standardize agent communication |
| **Introduced by** | Anthropic | Google (2025) |
| **When to use** | Agent needs to call an API, query a DB, read files | One agent needs to delegate a task to another agent |

**In a real system, you use both:**
```
User
 └── Orchestrator Agent
       ├── A2A ──→ Travel Agent  ──→ MCP ──→ Flight API
       ├── A2A ──→ Finance Agent ──→ MCP ──→ ERP System
       └── A2A ──→ HR Agent      ──→ MCP ──→ HR Database
```

#### A2A Core Concepts

**Agent Card**
- A JSON file that describes what an agent can do
- Other agents discover it by fetching a URL (like `http://localhost:8001/.well-known/agent.json`)
- Contains: agent name, version, skills, capabilities

**Agent Skill**
- A specific capability the agent exposes
- Defines what input it takes, what output it returns

**Standard Protocol Bindings** (how agents actually communicate):
| Binding | Notes |
|---|---|
| **JSON-RPC** | Remote Procedure Call using JSON — most common |
| **gRPC** | Google's binary RPC — faster, typed |
| **HTTP + JSON** | Simple REST-style calls |

Custom bindings also possible: WebSocket, MQTT.

#### A2A Practical Demo
3-agent travel system:

```
Travel Orchestrator
  ├── discovers Flight Agent via its Agent Card
  ├── discovers Hotel Agent via its Agent Card
  ├── sends task to Flight Agent  → gets flight options
  └── sends task to Hotel Agent   → gets hotel options
  → combines results → final travel plan
```

Running it:
```bash
# Terminal 1
python flight_agent.py      # starts on localhost:8001

# Terminal 2  
python hotel_agent.py       # starts on localhost:8002

# Terminal 3
python travel_orchestrator.py  # discovers both agents, runs the task
```

#### When NOT to Use A2A
A2A is not required for every system. Use it only when:
- You have multiple agents that need to communicate
- Those agents may be built on different frameworks
- You want standardized, discoverable agent communication

---

## What's Coming Next
- **Evaluation** — how to measure if your AI system is working well
  - Libraries: **RAGAS** (RAG evaluation), **DeepEval** (general AI eval)
  - LangSmith is NOT eval — it's monitoring only
- **Guardrails + Security** — controlling what the AI can and cannot do
- **End-to-end project** — starts after Diwali (no classes Nov 7–8)
