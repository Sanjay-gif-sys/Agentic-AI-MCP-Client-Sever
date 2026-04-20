from typing import Dict, Any, List
from app.mcp.registry import MCPRegistry


class MCPClientManager:
    def __init__(self, registry: MCPRegistry) -> None:
        self.registry = registry
        self.sessions: Dict[str, Any] = {}

    async def connect_servers(self) -> None:
        sample_servers = [
            {"name": "github", "transport": "stdio", "status": "connected"},
            {"name": "jira", "transport": "stdio", "status": "connected"},
            {"name": "docs", "transport": "stdio", "status": "connected"},
        ]

        sample_tools = {
            "github": [
                {"tool_name": "list_pull_requests", "description": "List repository pull requests"},
                {"tool_name": "search_issues", "description": "Search issues by keyword"},
            ],
            "jira": [
                {"tool_name": "search_tickets", "description": "Search Jira tickets"},
                {"tool_name": "get_blocked_tickets", "description": "Get blocked tickets"},
            ],
            "docs": [
                {"tool_name": "search_documents", "description": "Search project documents"},
            ],
        }

        for server in sample_servers:
            self.registry.register_server(server["name"], server)
            self.registry.register_tools(server["name"], sample_tools.get(server["name"], []))

    async def list_servers(self) -> List[Dict[str, Any]]:
        return self.registry.get_servers()

    async def list_tools(self) -> List[Dict[str, Any]]:
        return self.registry.get_tools()

    async def execute_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        if server_name == "jira" and tool_name == "get_blocked_tickets":
            return [
                {
                    "ticket_id": "PAY-101",
                    "title": "Payment retry failure",
                    "status": "Blocked",
                    "priority": "High",
                }
            ]

        if server_name == "github" and tool_name == "list_pull_requests":
            return [
                {
                    "pr_id": 142,
                    "title": "Fix payment retry edge case",
                    "status": "Open",
                }
            ]

        if server_name == "docs" and tool_name == "search_documents":
            return [
                {
                    "doc_name": "payment_design.md",
                    "snippet": "Retry flow handles transient failures up to 3 attempts.",
                }
            ]

        return [{"message": f"No mock result for {server_name}.{tool_name}", "arguments": arguments}]