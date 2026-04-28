from typing import Dict, Any, List
from app.mcp.client_manager import MCPClientManager


class GitHubAdapter:
    def __init__(self, client_manager: MCPClientManager) -> None:
        self.client_manager = client_manager
        self.server_name = "github"

    async def get_recent_prs(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 5,
    ) -> List[Dict[str, Any]]:
        return await self.client_manager.execute_tool(
            server_name=self.server_name,
            tool_name="list_pull_requests",
            arguments={
                "owner": owner,
                "repo": repo,
                "state": state,
                "per_page": per_page,
            },
        )