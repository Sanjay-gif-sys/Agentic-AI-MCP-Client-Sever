from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Dict, Any, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.mcp.registry import MCPRegistry
from app.schemas.mcp import MCPServerConfig


class MCPClientManager:
    def __init__(
        self,
        registry: MCPRegistry,
        server_configs: List[MCPServerConfig],
    ) -> None:
        self.registry = registry
        self.server_configs = [cfg for cfg in server_configs if cfg.enabled]

        self._exit_stack = AsyncExitStack()
        self._sessions: Dict[str, ClientSession] = {}

    async def connect_servers(self) -> None:
        """
        Connect to all enabled MCP servers.
        """
        for config in self.server_configs:
            try:
                session = await self._connect_stdio_server(config)
                self._sessions[config.name] = session

                self.registry.register_server(
                    config.name,
                    {
                        "name": config.name,
                        "transport": config.transport,
                        "status": "connected",
                    },
                )

                tools = await self._list_tools(session)
                self.registry.register_tools(config.name, tools)

            except Exception as exc:
                self.registry.register_server(
                    config.name,
                    {
                        "name": config.name,
                        "transport": config.transport,
                        "status": "failed",
                        "error": str(exc),
                    },
                )

    async def _connect_stdio_server(self, config: MCPServerConfig) -> ClientSession:
        """
        Connect to one MCP server using stdio transport.
        """
        if config.transport != "stdio":
            raise ValueError(
                f"Unsupported transport '{config.transport}'. "
                f"This version supports only 'stdio'."
            )

        if not config.command:
            raise ValueError(f"Missing command for server '{config.name}'")

        server_params = StdioServerParameters(
            command=config.command,
            args=config.args,
        )

        read_stream, write_stream = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        session = await self._exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await session.initialize()
        return session

    async def _list_tools(self, session: ClientSession) -> List[Dict[str, Any]]:
        """
        Fetch all tools exposed by a connected MCP server.
        """
        result = await session.list_tools()
        tools: List[Dict[str, Any]] = []

        for tool in result.tools:
            tools.append(
                {
                    "tool_name": tool.name,
                    "description": getattr(tool, "description", None),
                    "input_schema": getattr(tool, "inputSchema", {}) or {},
                }
            )

        return tools

    async def list_servers(self) -> List[Dict[str, Any]]:
        return self.registry.get_servers()

    async def list_tools(self, server_name: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.registry.get_tools(server_name)

    async def execute_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Call a real MCP tool on the selected server.
        """
        session = self._sessions.get(server_name)
        if not session:
            raise ValueError(f"No active MCP session found for server '{server_name}'")

        result = await session.call_tool(tool_name, arguments=arguments)
        return self._normalize_tool_result(result)

    def _normalize_tool_result(self, result: Any) -> List[Dict[str, Any]]:
        """
        Convert MCP SDK result into list[dict] format used by the app.
        """
        normalized: List[Dict[str, Any]] = []

        content = getattr(result, "content", None)
        if not content:
            return [{"raw_result": str(result)}]

        for item in content:
            item_type = getattr(item, "type", "unknown")

            if item_type == "text":
                normalized.append(
                    {
                        "type": "text",
                        "text": getattr(item, "text", ""),
                    }
                )
            else:
                normalized.append(
                    {
                        "type": item_type,
                        "value": str(item),
                    }
                )

        return normalized

    async def close(self) -> None:
        """
        Close all open MCP sessions and transports.
        """
        await self._exit_stack.aclose()