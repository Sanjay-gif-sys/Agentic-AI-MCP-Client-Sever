from pydantic import BaseModel, Field
from typing import List


class QueryAnalysis(BaseModel):
    query_type: str
    selected_servers: List[str] = Field(default_factory=list)
    requires_tools: bool = True
    requires_resources: bool = False


class ExecutionPlan(BaseModel):
    steps: List[str] = Field(default_factory=list)
    selected_tools: List[str] = Field(default_factory=list)