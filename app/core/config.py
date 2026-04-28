from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

from app.schemas.mcp import MCPServerConfig


class Settings(BaseSettings):
    app_name: str = "MCP Agentic Assistant"
    app_version: str = "0.1.0"

    mcp_servers: List[MCPServerConfig] = [
        MCPServerConfig(
            name="demo",
            transport="stdio",
            command="python",
            args=["app/servers/demo_server.py"],
            enabled=True,
        ),
        MCPServerConfig(
            name="github",
            transport="stdio",
            command="python",
            args=["app/servers/github_server.py"],
            enabled=True,
        ),
        
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


def get_settings() -> Settings:
    return Settings()