from app.schemas.state import AgentState
from app.mcp.adapters.github_adapter import GitHubAdapter
from app.mcp.adapters.jira_adapter import JiraAdapter
from app.mcp.adapters.docs_adapter import DocsAdapter


async def mcp_dispatcher_node(state: AgentState, deps: dict) -> AgentState:
    client_manager = deps["client_manager"]

    github_adapter = GitHubAdapter(client_manager)
    jira_adapter = JiraAdapter(client_manager)
    docs_adapter = DocsAdapter(client_manager)

    query = state["user_query"]
    results = {}
    evidence = []

    for server in state.get("selected_servers", []):
        if server == "jira":
            jira_data = await jira_adapter.get_blocked_tickets(query)
            results["jira"] = jira_data
            evidence.extend([{"source": "jira", "type": "tool_result", "content": item} for item in jira_data])

        elif server == "github":
            github_data = await github_adapter.get_recent_prs(query)
            results["github"] = github_data
            evidence.extend([{"source": "github", "type": "tool_result", "content": item} for item in github_data])

        elif server == "docs":
            docs_data = await docs_adapter.search_documents(query)
            results["docs"] = docs_data
            evidence.extend([{"source": "docs", "type": "tool_result", "content": item} for item in docs_data])

    state["mcp_results"] = results
    state["evidence"] = evidence
    return state