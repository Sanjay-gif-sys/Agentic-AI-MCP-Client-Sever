from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import configure_logging
from app.core.config import get_settings
from app.mcp.registry import MCPRegistry
from app.mcp.client_manager import MCPClientManager
from app.services.llm_service import LLMService
from app.graph.builder import build_graph


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version
    )

    registry = MCPRegistry()
    client_manager = MCPClientManager(registry=registry)
    llm_service = LLMService()

    app.state.settings = settings
    app.state.registry = registry
    app.state.client_manager = client_manager
    app.state.llm_service = llm_service

    deps = {
        "client_manager": client_manager,
        "llm_service": llm_service,
    }
    app.state.graph = build_graph(deps)

    app.include_router(router)

    @app.on_event("startup")
    async def startup_event() -> None:
        await client_manager.connect_servers()

    return app


app = create_app()