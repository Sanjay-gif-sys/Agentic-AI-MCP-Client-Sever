from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    query: str = Field(..., description="Natural language user query")
    session_id: Optional[str] = Field(default="default-session")
    metadata: Dict[str, Any] = Field(default_factory=dict)