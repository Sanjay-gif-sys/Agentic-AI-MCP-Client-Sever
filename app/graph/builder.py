from langgraph.graph import StateGraph, START, END
from app.schemas.state import AgentState

from app.graph.nodes.query_analyzer import query_analyzer_node
from app.graph.nodes.planner import planner_node
from app.graph.nodes.mcp_dispatcher import mcp_dispatcher_node
from app.graph.nodes.aggregator import aggregator_node
from app.graph.nodes.responder import responder_node


def build_graph(deps: dict):
    graph = StateGraph(AgentState)

    async def dispatcher_wrapper(state: AgentState):
        return await mcp_dispatcher_node(state, deps)

    async def responder_wrapper(state: AgentState):
        return await responder_node(state, deps)

    graph.add_node("query_analyzer", query_analyzer_node)
    graph.add_node("planner", planner_node)
    graph.add_node("mcp_dispatcher", dispatcher_wrapper)
    graph.add_node("aggregator", aggregator_node)
    graph.add_node("responder", responder_wrapper)

    graph.add_edge(START, "query_analyzer")
    graph.add_edge("query_analyzer", "planner")
    graph.add_edge("planner", "mcp_dispatcher")
    graph.add_edge("mcp_dispatcher", "aggregator")
    graph.add_edge("aggregator", "responder")
    graph.add_edge("responder", END)

    return graph.compile()