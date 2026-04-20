from fastapi import APIRouter, Request
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse, EvidenceItem

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@router.get("/servers")
async def get_servers(request: Request) -> dict:
    client_manager = request.app.state.client_manager
    servers = await client_manager.list_servers()
    return {"servers": servers}


@router.get("/tools")
async def get_tools(request: Request) -> dict:
    client_manager = request.app.state.client_manager
    tools = await client_manager.list_tools()
    return {"tools": tools}


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    graph = request.app.state.graph

    state = {
        "user_query": payload.query,
        "session_id": payload.session_id or "default-session",
    }

    result = await graph.ainvoke(state)

    return ChatResponse(
        query=payload.query,
        answer=result.get("final_response", ""),
        selected_servers=result.get("selected_servers", []),
        selected_tools=result.get("selected_tools", []),
        evidence=[EvidenceItem(**item) for item in result.get("evidence", [])],
        session_id=payload.session_id,
    )