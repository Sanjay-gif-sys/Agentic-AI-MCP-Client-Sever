from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseMCPAdapter(ABC):
    @abstractmethod
    async def discover_tools(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        raise NotImplementedError