from typing import Dict, Any, List
from app.mcp.client_manager import MCPClientManager


class JiraAdapter:
    def __init__(self, client_manager: MCPClientManager) -> None:
        self.client_manager = client_manager
        self.server_name = "jira"

    async def get_blocked_tickets(self, query: str) -> List[Dict[str, Any]]:
        return await self.client_manager.execute_tool(
            server_name=self.server_name,
            tool_name="get_blocked_tickets",
            arguments={"query": query},
        )