from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict, total=False):
    user_query: str
    session_id: str

    query_type: str
    selected_servers: List[str]
    selected_tools: List[str]
    execution_plan: List[str]

    available_servers: List[Dict[str, Any]]
    available_tools: List[Dict[str, Any]]

    mcp_results: Dict[str, List[Dict[str, Any]]]
    aggregated_context: str
    final_response: str

    evidence: List[Dict[str, Any]]
    error: Optional[str]