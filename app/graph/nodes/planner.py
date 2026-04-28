from app.schemas.state import AgentState


async def planner_node(state: AgentState) -> AgentState:
    selected_servers = state.get("selected_servers", [])
    selected_tools = []

    if "jira" in selected_servers:
        selected_tools.append("get_blocked_tickets")

    if "github" in selected_servers:
        selected_tools.append("list_pull_requests")

    if "docs" in selected_servers:
        selected_tools.append("search_documents")

    state["selected_tools"] = selected_tools
    state["execution_plan"] = ["dispatch", "aggregate", "respond"]
    return state