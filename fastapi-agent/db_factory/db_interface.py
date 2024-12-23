from abc import ABC, abstractmethod
from typing import Any, Dict, List

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Establish database connection"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> List[Any]:
        """Execute a SQL query"""
        pass
    
    @abstractmethod
    def get_table_names(self) -> Dict[str, List[str]]:
        """Get all table names from database"""
        pass
    
    @abstractmethod
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get comprehensive schema information for a specific table"""
        pass
    
    @abstractmethod
    def get_schema_list(self, table_names: List[str]) -> List[Dict[str, Any]]:
        """Get schema information for multiple tables"""
        pass