from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class EvidenceItem(BaseModel):
    source: str
    type: str
    content: Dict[str, Any]


class ChatResponse(BaseModel):
    query: str
    answer: str
    selected_servers: List[str] = Field(default_factory=list)
    selected_tools: List[str] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    session_id: Optional[str] = None