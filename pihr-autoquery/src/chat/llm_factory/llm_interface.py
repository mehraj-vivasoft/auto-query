from abc import ABC, abstractmethod
from typing import Dict, Any
from src.chat.llm_factory.prompts.guardrail import GurdrailResponse

class LLMInterface(ABC):            
    
    # generate response from user query, user_id, conversation_id
    @abstractmethod
    async def generate_response(self, query: str, user_id: str, conversation_id: str) -> str:
        pass

    # check if the query is valid
    @abstractmethod
    async def check_validation(self, query: str) -> GurdrailResponse:
        pass