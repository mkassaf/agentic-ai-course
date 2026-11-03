"""Small protocol examples used by the introductory notebooks.

``review_over_a2a`` is a course helper, not an A2A SDK method. It keeps
Agent Card and server configuration outside the beginner's policy review.
The official SDK still discovers the card and exchanges JSON-RPC messages.
All HTTP requests use an in-process ASGI transport; no port is opened.
"""


async def review_over_a2a(case: dict, proposal: str) -> tuple[str, str]:
    """Return (discovered agent name, policy report) using A2A 1.0 JSON-RPC.

    Requires ``a2a-sdk[http-server]==1.3.0``. Imports stay inside the helper
    so other course lessons do not need to install this optional dependency.
    The receiving agent is deterministic and applies the course's fictional
    teaching rule. Agreement with that rule does not establish design quality.
    """
    import json
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

    if type(case.get("team_size")) is not int or case["team_size"] < 1:
        raise ValueError("team_size must be a positive integer.")
    if type(case.get("independent_deploys")) is not bool:
        raise ValueError("independent_deploys must be a boolean.")

    class ArchitectureReviewer(AgentExecutor):
        async def execute(self, context, event_queue):
            request = json.loads(get_message_text(context.message))
            facts = request["case"]
            expected = ("microservices" if facts["team_size"] >= 8
                        and facts["independent_deploys"] else "modular monolith")
            status = "PASS" if request["proposal"] == expected else "FAIL"
            report = f"{status}: course policy expects {expected}."
            await event_queue.enqueue_event(new_text_message(report))

        async def cancel(self, context, event_queue):
            raise NotImplementedError("An immediate message creates no task to cancel.")

    card = AgentCard(
        name="Architecture reviewer", description="Checks the fictional course policy.", version="1.0.0",
        default_input_modes=["text/plain"], default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False),
        supported_interfaces=[AgentInterface(
            protocol_binding="JSONRPC", url="http://agent.local/",
            protocol_version="1.0",
        )],
        skills=[AgentSkill(
            id="review", name="Review", description="Check an architecture proposal against the course policy.",
            tags=["architecture", "policy"],
        )],
    )
    handler = DefaultRequestHandler(
        agent_executor=ArchitectureReviewer(), task_store=InMemoryTaskStore(), agent_card=card,
    )
    app = Starlette(routes=(
        create_agent_card_routes(card) + create_jsonrpc_routes(handler, "/")
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
            payload = json.dumps({"case": case, "proposal": proposal})
            message = new_text_message(payload, role=Role.ROLE_USER)
            request = SendMessageRequest(message=message)
            report = None
            async for event in remote.send_message(request):
                if event.HasField("message"):
                    report = get_message_text(event.message)
        finally:
            await remote.close()
            await handler.aclose()
        if report is not None:
            return discovered.name, report
    raise RuntimeError("The agent returned no review message.")
