from typing import Any, Dict, List
from app.mcp.client_manager import MCPClientManager


class GitHubAdapter:
    def __init__(self, client_manager: MCPClientManager) -> None:
        self.client_manager = client_manager
        self.server_name = "github"

    async def get_recent_prs(self, query: str) -> List[Dict[str, Any]]:
        return await self.client_manager.execute_tool(
            server_name=self.server_name,
            tool_name="list_pull_requests",
            arguments={"query": query}
        )