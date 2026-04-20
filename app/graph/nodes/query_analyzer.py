from app.schemas.state import AgentState


async def query_analyzer_node(state: AgentState) -> AgentState:
    query = state["user_query"].lower()
    selected_servers = []

    has_jira = any(word in query for word in ["ticket", "jira", "sprint", "blocked"])
    has_github = any(word in query for word in ["github", "pr", "pull request", "repo", "commit"])
    has_docs = any(word in query for word in ["doc", "design", "architecture", "wiki"])

    if has_jira:
        selected_servers.append("jira")
    if has_github:
        selected_servers.append("github")
    if has_docs:
        selected_servers.append("docs")

    if len(selected_servers) > 1:
        query_type = "multi_server_lookup"
    elif selected_servers == ["jira"]:
        query_type = "jira_only"
    elif selected_servers == ["github"]:
        query_type = "github_only"
    elif selected_servers == ["docs"]:
        query_type = "docs_only"
    else:
        query_type = "unknown"

    state["query_type"] = query_type
    state["selected_servers"] = selected_servers
    return state