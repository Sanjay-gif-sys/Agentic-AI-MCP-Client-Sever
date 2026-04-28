from typing import Dict, List, Any, Optional


class MCPRegistry:
    def __init__(self) -> None:
        self._servers: Dict[str, Dict[str, Any]] = {}
        self._tools: Dict[str, List[Dict[str, Any]]] = {}

    def register_server(self, server_name: str, metadata: Dict[str, Any]) -> None:
        self._servers[server_name] = metadata

    def register_tools(self, server_name: str, tools: List[Dict[str, Any]]) -> None:
        self._tools[server_name] = tools

    def get_server(self, server_name: str) -> Optional[Dict[str, Any]]:
        return self._servers.get(server_name)

    def get_servers(self) -> List[Dict[str, Any]]:
        return [{"server_name": name, **meta} for name, meta in self._servers.items()]

    def get_tools(self, server_name: str | None = None) -> List[Dict[str, Any]]:
        if server_name:
            return self._tools.get(server_name, [])
        all_tools: List[Dict[str, Any]] = []
        for server, tools in self._tools.items():
            for tool in tools:
                all_tools.append({"server_name": server, **tool})
        return all_tools

    def find_tool(self, server_name: str, tool_name: str) -> Optional[Dict[str, Any]]:
        for tool in self._tools.get(server_name, []):
            if tool.get("tool_name") == tool_name:
                return tool
        return None