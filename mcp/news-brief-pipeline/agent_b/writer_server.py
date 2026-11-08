import re

import uvicorn
from starlette.applications import Starlette

from a2a.helpers import new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill

# Skills, Agent card: description, url, version, protocol
# app, route and serve

# host & port
HOST = "127.0.0.1"
PORT = 8002

# summarizer
def summarize(text:str) -> str:
    sentence = re.split(r'(?<=[.!?])\s+', text.strip())
    bullets = [f'- {s}' for s in sentence[:5]]
    return "\n".join(bullets)

# Agent executor
class WriteExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        raw_text = context.get_user_input()
        brief = summarize(raw_text)
        await event_queue.enqueue_event(new_text_message(brief))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError('nothing to cancel')

# skill
skill = AgentSkill(
    id = 'summarize_brief',
    name = 'summarize into a brief',
    description= 'Take raw text and return 5 bullet point summary',
    tags= ["summary", "tech news", " ai news"],
    examples=["Summarize this article into 3 bullets."]
)

agent_card = AgentCard(
    name= 'write-agent',
    description= 'Turns a raw text into 5 bullet summary.',
    version='1.0.0',
    supported_interfaces= [
        AgentInterface(
            protocol_binding = 'JSONRPC',
            protocol_version = '1.0',
            url=f"http://{HOST}:{PORT}/",
        )
    ],
    capabilities= AgentCapabilities(streaming=False, push_notifications=False),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[skill]
)

request_handler = DefaultRequestHandler(
    agent_executor=WriteExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=agent_card
)

app = Starlette(routes=[
    *create_agent_card_routes(agent_card),
    *create_jsonrpc_routes(request_handler, rpc_url='/')
]
)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)

