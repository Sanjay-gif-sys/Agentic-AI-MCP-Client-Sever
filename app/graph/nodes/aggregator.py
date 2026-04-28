from app.schemas.state import AgentState


async def aggregator_node(state: AgentState) -> dict:
    results = state.get("mcp_results", {})
    parts = []

    for source, items in results.items():
        parts.append(f"{source.upper()} RESULTS:")
        for item in items:
            parts.append(f"- {item}")

    return {"aggregated_context": "\n".join(parts)}