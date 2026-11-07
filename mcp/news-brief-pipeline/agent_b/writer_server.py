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

# Skills, Agent cart:- description, ulr, version, protocal
# app, route and serve

# host & port
HOST = "127.0.0.1"
PORT = 8002

# summerizer
def summerize(text:str) -> str:
    sentance = re.split(r'(?<=[.!?])\s+', text.strip())
    bullet = [f'-{s}' for s in sentance[:5]]
    return '/n'.join(bullet)

# Agent executor
class WriteExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        raw_text = context.get_user_input()
        brief = summerize(raw_text)
        await event_queue.enqueue_event(new_text_message(brief))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError('nothing to cancel')

# skill
skill = AgentSkill(
    id = 'summerize_brif',
    name = 'sumerize into a brief',
    description= 'Take raw text and return 5 bullet point summery',
    tags= ["summary", "teac news", " ai news"],
    examples=["Summarize this article into 3 bullets."]
)

agentcard = AgentCard(
    
)       