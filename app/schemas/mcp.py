from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class MCPServerConfig(BaseModel):
    name: str
    transport: str
    command: Optional[str] = None
    args: List[str] = Field(default_factory=list)
    url: Optional[str] = None
    enabled: bool = True


class MCPToolInfo(BaseModel):
    server_name: str
    tool_name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = Field(default_factory=dict)


class MCPResourceInfo(BaseModel):
    server_name: str
    resource_name: str
    description: Optional[str] = None
    uri: Optional[str] = None