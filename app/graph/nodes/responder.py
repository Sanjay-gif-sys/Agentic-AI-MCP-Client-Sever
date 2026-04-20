from app.schemas.state import AgentState


async def responder_node(state: AgentState, deps: dict) -> AgentState:
    llm_service = deps["llm_service"]
    answer = await llm_service.generate_response(
        query=state["user_query"],
        context=state.get("aggregated_context", "")
    )
    state["final_response"] = answer
    return state