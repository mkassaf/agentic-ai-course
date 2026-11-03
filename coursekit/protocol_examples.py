"""Small protocol examples used by the introductory notebooks.

``greet_over_a2a`` is a course helper, not an A2A SDK method. It keeps
Agent Card and server configuration outside the beginner's greeting example.
The official SDK still discovers the card and exchanges JSON-RPC messages.
All HTTP requests use an in-process ASGI transport; no port is opened.
"""


async def greet_over_a2a(name: str) -> tuple[str, str]:
    """Return (discovered agent name, greeting) using A2A 1.0 JSON-RPC.

    Requires ``a2a-sdk[http-server]==1.3.0``. Imports stay inside the helper
    so other course lessons do not need to install this optional dependency.
    The receiving agent is deterministic; this example teaches interoperability
    independently of model access or response quality.
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

    class Greeter(AgentExecutor):
        async def execute(self, context, event_queue):
            student = get_message_text(context.message).strip()
            await event_queue.enqueue_event(new_text_message(f"Hello, {student}!"))

        async def cancel(self, context, event_queue):
            raise NotImplementedError("An immediate message creates no task to cancel.")

    card = AgentCard(
        name="Greeter", description="Greets a student.", version="1.0.0",
        default_input_modes=["text/plain"], default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False),
        supported_interfaces=[AgentInterface(
            protocol_binding="JSONRPC", url="http://agent.local/",
            protocol_version="1.0",
        )],
        skills=[AgentSkill(
            id="greet", name="Greet", description="Greet a student by name.",
            tags=["greeting"],
        )],
    )
    handler = DefaultRequestHandler(
        agent_executor=Greeter(), task_store=InMemoryTaskStore(), agent_card=card,
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
            message = new_text_message(name, role=Role.ROLE_USER)
            request = SendMessageRequest(message=message)
            greeting = None
            async for event in remote.send_message(request):
                if event.HasField("message"):
                    greeting = get_message_text(event.message)
        finally:
            await remote.close()
        if greeting is not None:
            return discovered.name, greeting
    raise RuntimeError("The agent returned no greeting message.")
