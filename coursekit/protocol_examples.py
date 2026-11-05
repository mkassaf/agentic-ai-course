"""Small protocol examples used by the introductory notebooks.

``talk_over_a2a`` and ``review_over_a2a`` are course helpers, not A2A SDK methods. It keeps
Agent Card and server configuration outside the beginner's policy review.
The official SDK still discovers the card and exchanges JSON-RPC messages.
All HTTP requests use an in-process ASGI transport; no port is opened.
"""


async def talk_over_a2a(handler, message: str, *, name: str, description: str,
                        skill: str = "Answer", skill_description: str = "") -> tuple[dict, str]:
    """Serve ``handler`` (text in, text out) as an A2A agent, discover its card, and send one message.

    Returns ``(card, reply)``: the Agent Card the client discovered, as a small dictionary, and the
    agent's reply. Requires ``a2a-sdk[http-server]==1.3.0``. Every request uses an in-process ASGI
    transport, so no port is opened and no network is needed.
    """
    import httpx
    from a2a.client import A2ACardResolver, ClientConfig, create_client
    from a2a.helpers import get_message_text, new_text_message
    from a2a.server.agent_execution import AgentExecutor
    from a2a.server.request_handlers import DefaultRequestHandler
    from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
    from a2a.server.tasks import InMemoryTaskStore
    from a2a.types import (
        AgentCapabilities, AgentCard, AgentInterface, AgentSkill,
        Role, SendMessageRequest,
    )
    from starlette.applications import Starlette

    class FunctionAgent(AgentExecutor):
        async def execute(self, context, event_queue):
            reply = handler(get_message_text(context.message))
            await event_queue.enqueue_event(new_text_message(str(reply)))

        async def cancel(self, context, event_queue):
            raise NotImplementedError("An immediate message creates no task to cancel.")

    card = AgentCard(
        name=name, description=description, version="1.0.0",
        default_input_modes=["text/plain"], default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False),
        supported_interfaces=[AgentInterface(
            protocol_binding="JSONRPC", url="http://agent.local/",
            protocol_version="1.0",
        )],
        skills=[AgentSkill(
            id=skill.lower().replace(" ", "-"), name=skill,
            description=skill_description or description, tags=[skill.lower()],
        )],
    )
    request_handler = DefaultRequestHandler(
        agent_executor=FunctionAgent(), task_store=InMemoryTaskStore(), agent_card=card,
    )
    app = Starlette(routes=(
        create_agent_card_routes(card) + create_jsonrpc_routes(request_handler, "/")
    ))
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://agent.local",
    ) as http:
        discovered = await A2ACardResolver(
            httpx_client=http, base_url="http://agent.local",
        ).get_agent_card()
        remote = await create_client(
            discovered, client_config=ClientConfig(streaming=False, httpx_client=http),
        )
        try:
            request = SendMessageRequest(message=new_text_message(message, role=Role.ROLE_USER))
            reply = None
            async for event in remote.send_message(request):
                if event.HasField("message"):
                    reply = get_message_text(event.message)
        finally:
            await remote.close()
            await request_handler.aclose()
    if reply is None:
        raise RuntimeError("The agent returned no message.")
    found = {"name": discovered.name, "description": discovered.description,
             "skills": [{"name": s.name, "description": s.description} for s in discovered.skills],
             "url": discovered.supported_interfaces[0].url}
    return found, reply


async def review_over_a2a(case: dict, proposal: str) -> tuple[str, str]:
    """Return (discovered agent name, policy report) from a reviewer agent reached over A2A.

    The receiving agent is deterministic and applies the course's fictional
    teaching rule. Agreement with that rule does not establish design quality.
    """
    import json

    if type(case.get("team_size")) is not int or case["team_size"] < 1:
        raise ValueError("team_size must be a positive integer.")
    if type(case.get("independent_deploys")) is not bool:
        raise ValueError("independent_deploys must be a boolean.")

    def reviewer(text):
        request = json.loads(text)
        facts = request["case"]
        expected = ("microservices" if facts["team_size"] >= 8
                    and facts["independent_deploys"] else "modular monolith")
        status = "PASS" if request["proposal"] == expected else "FAIL"
        return f"{status}: course policy expects {expected}."

    card, report = await talk_over_a2a(
        reviewer, json.dumps({"case": case, "proposal": proposal}),
        name="Architecture reviewer", description="Checks the fictional course policy.",
        skill="Review", skill_description="Check an architecture proposal against the course policy.",
    )
    return card["name"], report
