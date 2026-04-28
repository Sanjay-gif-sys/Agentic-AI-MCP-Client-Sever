from app.schemas.state import AgentState
from app.services.llm_service import LLMService

async def responder_node(state: AgentState, deps: dict) -> dict:
    llm_service = deps["llm_service"]

    answer = await llm_service.generate_response(
        query=state["user_query"],
        context=state.get("aggregated_context", "")
    )

    return {"final_response": answer}