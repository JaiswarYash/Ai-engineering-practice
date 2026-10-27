# Session Notes — A2A Protocol Deep Dive

*2026-10-25*

A2A (Agent-to-Agent) is Google's 2025 protocol for standardizing communication between agents running on different servers.

---

## MCP vs A2A

|  | MCP | A2A |
| --- | --- | --- |
| Introduced by | Anthropic | Google |
| Year | 2024 | 2025 |
| Purpose | Provide context, tools, and resources *to* a model | Standardize communication *between* agents |
| Key components | Client + Server | Client + Server |
| What it handles | Tool calls, prompts, external resources | Cross-agent requests over a network |

---

## When A2A Is and Isn't Needed

**The rule:** if both agents are on the same machine in the same application, A2A is not needed — a direct function call (`agent.invoke()`) works. A2A is needed when agents are on different servers.

**Why `invoke()` fails across servers:** `invoke()` is a function call inside the same Python process, reaching into shared memory. When Agent B is on a different machine, there is no shared memory or process — you cannot call a function that lives on another server. You need a network-level request to bridge them.

| Situation | A2A needed? |
| --- | --- |
| Both agents, same app, same server | No — direct handoff works |
| Two apps on the same server | Optional — A2A can be used |
| Agents on different servers/machines | Yes |

**Without A2A:** you can use a plain REST API (`requests.post(server_url, …)`). It works, but every agent may have a different API structure. With 100 companies' agents, you'd need custom integration code for each.

**With A2A:** every compliant agent exposes a standard interface. One client can talk to any server without custom code.

---

## Protocol Bindings

A **protocol binding** is the specific mechanism chosen to carry A2A communication rules over the network. You pick **one** per application — not all three.

| Binding | Full name | Format | Speed | Best for |
| --- | --- | --- | --- | --- |
| JSON-RPC | JavaScript Object Notation Remote Procedure Call | Text (JSON) | Moderate | Most common; readable; default in the A2A package |
| gRPC | Remote Procedure Call (Google) | Binary (Protocol Buffers) | Fastest | High-frequency, performance-critical systems |
| HTTP + JSON | Hypertext Transfer Protocol + JSON | Text (JSON over REST) | Moderate | Simplest; familiar to most developers |

**Key difference — JSON-RPC vs HTTP + JSON:** both use JSON, but:

- JSON-RPC: the method name is specified *inside* the JSON body
- HTTP + JSON: the operation is identified by the HTTP method (GET/POST) and the URL endpoint

The demo from the Oct 24 session used **JSON-RPC**.

---

## Important A2A Terms

**Example used in class:** user asks travel agent → "Find flights from Bangalore to Dubai". Travel agent calls the flight agent.

| Term | Definition | In the example |
| --- | --- | --- |
| A2A Client | The agent that initiates and sends the request | Travel agent |
| A2A Server | The agent that receives and processes the request | Flight agent |
| Agent Card | A digital profile of the agent — name, description, capabilities | Flight agent's identity card |
| Agent Skill | What the agent is capable of doing | "Search and return flight data" |
| Agent Discovery | The process of finding available agents on the network | — |
| Message | The actual content exchanged between agents | "Find flights from Bangalore to Dubai" |
| Task | A trackable unit of work assigned to an agent | The flight search request |
| Task ID | Unique identifier for a specific task | — |
| Task Status | Current execution state of the task | pending / running / complete |
| Artifact | The output or deliverable generated during task execution | The list of available flights returned |
| Context ID | Groups related conversations and tasks under one identifier | Links follow-up queries to the same session |

---

## Next Topic

**Evaluation** — covered in the session after this one.
