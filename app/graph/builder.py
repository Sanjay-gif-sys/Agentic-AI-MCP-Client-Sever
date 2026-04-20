from app.schemas.state import AgentState
from app.graph.nodes.query_analyzer import query_analyzer_node
from app.graph.nodes.planner import planner_node
from app.graph.nodes.mcp_dispatcher import mcp_dispatcher_node
from app.graph.nodes.aggregator import aggregator_node
from app.graph.nodes.responder import responder_node


class SimpleGraphRunner:
    def __init__(self, deps: dict) -> None:
        self.deps = deps

    async def ainvoke(self, state: AgentState) -> AgentState:
        state = await query_analyzer_node(state)
        state = await planner_node(state)
        state = await mcp_dispatcher_node(state, self.deps)
        state = await aggregator_node(state)
        state = await responder_node(state, self.deps)
        return state


def build_graph(deps: dict) -> SimpleGraphRunner:
    return SimpleGraphRunner(deps=deps)