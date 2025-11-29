from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAgent(ABC):
    @abstractmethod
    async def process_message(self, message: str, session_id: str, file: Optional[bytes] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a user message and return a response.
        """
        pass
