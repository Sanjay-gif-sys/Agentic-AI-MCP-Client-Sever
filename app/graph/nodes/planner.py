from app.schemas.state import AgentState


async def planner_node(state: AgentState) -> AgentState:
    selected_servers = state.get("selected_servers", [])
    selected_tools = []
    execution_plan = ["analyze"]

    if "jira" in selected_servers:
        selected_tools.append("get_blocked_tickets")
        execution_plan.append("fetch_jira_data")

    if "github" in selected_servers:
        selected_tools.append("list_pull_requests")
        execution_plan.append("fetch_github_data")

    if "docs" in selected_servers:
        selected_tools.append("search_documents")
        execution_plan.append("fetch_docs_data")

    execution_plan.extend(["aggregate", "respond"])

    state["selected_tools"] = selected_tools
    state["execution_plan"] = execution_plan
    return state