# Multi-Agentic Systems + LangChain: My Notes
Sessions: Sept 26, Sept 27, Oct 4
(Built on top of the original session notes, which are untouched.)

---

# PART A: SIMPLE NOTES (quick revision)

## The big picture
- **LangChain** = building blocks (models, prompts, parsers, tools, chains)
- **LangGraph** = orchestration (nodes, edges, state, human-in-the-loop)
- **LangSmith** = observability, LangChain only
- **LangFuse** = observability, any framework, open source

## Core methods
- `init_chat_model("name")` loads any model with one method
- `.invoke()` one input, one output
- `.batch()` many inputs together
- `.stream()` token by token (use this in production)
- Messages: Human, AI, System, Tool

## Prompts and parsers
- `ChatPromptTemplate.from_messages` for system + human messages
- `MessagesPlaceholder` inserts chat history
- `.partial()` pre-fills some variables
- `StrOutputParser` gives a string, `JsonOutputParser` gives a dict
- `PydanticOutputParser` gives a typed object
- `with_structured_output(Class)` is the cleanest option when the model supports it

## Agents
- `create_agent` = quick ReAct agent (think, call tool, observe, repeat)
- Need custom nodes, routing, or state? Build in LangGraph
- Agent-as-tool: wrap an agent as a tool for a parent agent
- DeepAgent = long tasks, less control, expensive

## Middleware
- Hooks around LLM calls: logging, summarising, human approval, call limits, model routing
- Convenience only; LangGraph can do all of it

## 3 multi-agent patterns
| Pattern | Shape | Use when |
|---|---|---|
| Supervisor | One boss, many workers | Default for production |
| Network / Swarm | Peers hand off to each other | Flexible handoffs |
| Hierarchical | Supervisors of supervisors | Big enterprise workflows |

## Command API
`Command(goto="node", update={...})` updates state and redirects flow in one step.
`resume=` continues a paused human-in-the-loop graph.

## Production rules
1. Hybrid beats fully autonomous
2. Start simple
3. Build evaluation before shipping
4. Human approval for high-stakes or irreversible actions
5. Standard need: `create_agent`. Custom need: LangGraph

## Interview one-liners
- LangSmith works only with LangChain. LangFuse works with anything.
- Supervisor is the most reliable pattern for production.
- Command and middleware are shortcuts, not requirements.

---

# PART B: DETAILED NOTES

## 1. LangChain ecosystem
LangChain Inc. ships four products:

| Module | Role |
|---|---|
| LangChain | Model loading, prompt templates, output parsers, document loaders, tool creation, chains |
| LangGraph | Agent orchestration: nodes, edges, state graphs, workflows, human-in-the-loop |
| LangSmith | Hosted platform for tracing, monitoring, evaluation (LangChain-native only) |
| LangFuse | Open-source, framework-agnostic observability (LangChain, LlamaIndex, Haystack, custom) |

**Choosing:** LangChain/LangGraph project means LangSmith. Multi-framework or custom app means LangFuse. Sunny will demo both in the first end-to-end project.

## 2. Model interaction
**`init_chat_model(model_name)`** is one universal loader for OpenAI, Anthropic, Gemini, Ollama. Swap the name and set the right API key in `.env`; no provider-specific imports.

**Invocation modes**
- `.invoke(input)`: single request, complete response
- `.batch([a, b, c])`: independent inputs processed together
- `.stream(input)`: token-by-token output; same cost, better UX, so use it in production

**Message types**
- `HumanMessage`: user input
- `AIMessage`: model reply
- `SystemMessage`: behaviour instructions
- `ToolMessage`: result of a tool call (used inside agent loops)

**Trimming history:** `trim_messages(messages, max_tokens=N, strategy="last")` keeps the most recent messages. Good to know, but often you write custom logic instead, e.g. summarise old messages rather than drop them.

## 3. Prompts
- `PromptTemplate`: plain text with `{placeholders}`
- `ChatPromptTemplate.from_messages([...])`: system + human messages
- `MessagesPlaceholder`: slot for conversation history inside a chat template
- `.partial(var=value)`: pre-fill fixed variables (e.g. `level="expert"`) so only the rest are passed at runtime

## 4. Output parsers
| Option | Returns | Note |
|---|---|---|
| `StrOutputParser` | plain string | same as taking `.content` |
| `JsonOutputParser` | dict | |
| `PydanticOutputParser(Person)` | typed object | adds `.get_format_instructions()` to the prompt |
| `model.with_structured_output(Person)` | typed object | native to the model; cleanest when supported |

## 5. `create_agent` vs LangGraph from scratch
`create_agent(model, tools, system_prompt, name)` builds a **ReAct** agent (Reasoning + Action): LLM picks a tool, gets the result, decides again, repeats until it has a final answer.

| Use `create_agent` | Use LangGraph from scratch |
|---|---|
| Simple use case, standard ReAct loop | Custom nodes between steps |
| No custom memory or routing | Fine-grained state management |
| | Conditional routing, human-in-the-loop, subgraphs |

**DeepAgent:** separate module for long-horizon multi-step tasks. Handles planning out of the box but gives less control, and is memory-heavy and API-heavy. Test your budget first.

**Agent-as-tool:** expose a `create_agent` agent as a tool to a parent agent; the parent picks which sub-agent to call. Sunny used this for a report generation system.

## 6. Middleware
Pre-built hooks you attach to an agent:
- `before_model` / `after_model`: run code around every LLM call (logging, timing)
- Summarization middleware: auto-summarise history
- Human-in-the-loop middleware: inject an approval step
- Model call limit middleware: cap LLM calls
- Model router: cheap queries to a small model, complex ones to a large model

Everything middleware does can be built in LangGraph. It is a shortcut.

## 7. Multi-agent patterns

### Supervisor (hub-and-spoke)
```
User -> Supervisor -> Agent A / Agent B / Agent C
        (each agent reports back to the supervisor)
```
- One central LLM chooses the sub-agent
- Sub-agents report back after each step
- Supervisor decides when the task is done
- Most recommended and most reliable for production

### Network / Swarm (peer-to-peer)
```
Agent A <-> Agent B <-> Agent C <-> Agent D
```
- No central coordinator
- Agents hand off directly with `Command(goto="agent_name")`
- Also called the **handoff** pattern

### Hierarchical (supervisor of supervisors)
```
Top Supervisor
 |- Team Supervisor A -> Agent 1, Agent 2
 |- Team Supervisor B -> Agent 3, Agent 4
```
- Supervisor pattern extended across levels
- For complex enterprise workflows (SDLC automation, multi-department systems)
- Sunny's rule: only go deeper if a simpler design cannot do the job

## 8. Command API
`Command(goto="agent_name", update={state_key: value})` updates state **and** redirects flow from inside a node.

- Without it: separate conditional edge + routing function
- With it: the node decides where to go next
- Used in handoff / swarm patterns

| Parameter | Purpose |
|---|---|
| `goto` | node/agent to jump to |
| `update` | state changes applied at the same time |
| `resume` | resume an interrupted graph with human feedback |

Command is a shortcut; conditional edges can do the same.

## 9. Sunny's production rules
1. **Don't default to fully autonomous.** Most production systems are hybrid: deterministic flow with LLM judgment at specific decision points. More reliable and cheaper.
2. **Start simple.** A basic router workflow beats supervisor/hierarchical complexity unless the requirement demands it.
3. **Build an evaluation framework first.** Test, show evidence it works, then ship.
4. **Human-in-the-loop for high stakes.** No irreversible action without approval.
5. **Standard requirements: `create_agent`. Custom logic: LangGraph from scratch.**

## 10. Course timeline
- Next 2 sessions: remaining LangChain + framework comparison (CrewAI, AutoGen, Google ADK, Semantic Kernel)
- Then: MCP, A2A, Guardrails, Evaluation Strategy
- Projects start about Oct 24-25 and run through November
- Batch ends about Nov 29

---

# PART C: CORRECTIONS TO THE ORIGINAL NOTES
Name slips in the original that will break code if copied:
- `trim_message(max_token=N)` is actually `trim_messages(max_tokens=N)`
- `MessagePlaceholder` is actually `MessagesPlaceholder`
- Middleware names are class-style in code, e.g. `SummarizationMiddleware`, `HumanInTheLoopMiddleware`, `ModelCallLimitMiddleware`. Check the current docs for exact names.
- "OpenAI Semantic Kernel" is **Microsoft** Semantic Kernel
- Class names and parameters shift between LangChain versions, so always verify against the official docs before using
