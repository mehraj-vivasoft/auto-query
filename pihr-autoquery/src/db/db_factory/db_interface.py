from abc import ABC, abstractmethod
from typing import Any, Dict, List
from src.db.schemas import ChatMessageModel, AllConversationsResponseModel, MessagesResponseModel

class DBInterface(ABC):
    
    @abstractmethod
    def connect(self) -> None:
        """Establish database connection"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection"""
        pass
    
    @abstractmethod
    def create_conversation(self, conversation_id: str, subject: str, user_id: str) -> None:
        """Create a new conversation in the database"""
        pass
    
    @abstractmethod
    async def post_chat(self, conversation_id: str, user_id: str, role: str, message: str, msg_summary: str) -> ChatMessageModel:
        """Post a chat message to the database"""
        pass
    
    @abstractmethod
    def get_chat_by_page(self, conversation_id: str, page_number: int, limit: int) -> MessagesResponseModel:
        """Get a list of chat conversations and messages, sorted by the latest message's timestamp"""
        pass
    
    @abstractmethod
    def get_chat_context(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get the chat context for a given conversation id"""
        pass
    
    # get all conversations of a user
    @abstractmethod
    def get_all_conversations(self, user_id: str) -> AllConversationsResponseModel:
        """Get all conversations of a user"""
        pass
    