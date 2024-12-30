from abc import ABC, abstractmethod
from typing import Any, Dict, List

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
    def post_chat(self, thread_id: str, user_id: str, role: str, message: str, msg_summary: str) -> None:
        """Post a chat message to the database"""
        pass
    
    @abstractmethod
    def get_chat_by_page(self, thread_id: str, page_number: int) -> List[Dict[str, Any]]:
        """Get a list of chat threads and messages, sorted by the latest message's timestamp"""
        pass
    
    @abstractmethod
    def get_chat_context(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get the chat context for a given thread id"""
        pass
    
    # get all threads of a user
    @abstractmethod
    def get_all_threads(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all threads of a user"""
        pass
    