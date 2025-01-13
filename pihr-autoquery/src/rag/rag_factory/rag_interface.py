from abc import ABC, abstractmethod
from typing import Any, Dict, List

class RAGInterface(ABC):
    
    @abstractmethod
    def connect(self) -> None:
        """Establish database connection"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection"""
        pass
    
    @abstractmethod
    def post_chunk(self, collection: str, data: Any) -> List[Any]:
        """Post a document to the RAG"""
        pass
    
    @abstractmethod
    def get_top_k_chunks(self, collection: str, query: str, top_k: int, is_simple: bool = False) -> List[Any]:
        """Get a response from the RAG"""
        pass
    
    @abstractmethod
    def get_all_chunks(self, collection: str) -> List[Any]:
        """Get all responses from the RAG"""
        pass
    
    @abstractmethod
    def get_chunks_by_ids(self, collection: str, id: List[str]) -> List[Any]:
        """Get a response from the RAG"""
        pass
    
    @abstractmethod
    def get_collection_names(self) -> List[str]:
        """Get all table names from database"""
        pass
    
    @abstractmethod
    def delete_chunks_by_id(self, collection: str, ids: List[str]) -> List[Any]:
        """Delete chunks by id"""
        pass
    
    
    