import os
from typing import Any, Dict, List
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from db_factory.db_interface import DatabaseInterface
from utils.logging_config import get_app_logger, get_db_logger
from db.schema_helpers import get_column_details, get_foreign_key_details, get_index_details, get_primary_key_details

class SQLiteDatabaseInstance(DatabaseInterface):
    def __init__(self):
        self.connection_string = self.get_connection_string()
        self.engine = None
        self.logger = get_db_logger()
        self.SessionLocal = None
    
    def get_connection_string(self) -> str:
        """Get connection string from environment variables"""
        # For SQLite, we typically use a file-based database or in-memory database
        DB_PATH = os.getenv("DB_PATH", ":memory:")
        
        # SQLite connection string uses different format from MSSQL
        connection_string = f"sqlite:///{DB_PATH}"
        get_app_logger().info(f"Connection string from env: {connection_string}")
        
        return connection_string
    
    async def connect(self) -> None:
        try:
            # For SQLite, we use create_engine with a different set of parameters
            self.engine = create_engine(
                self.connection_string, 
                connect_args={'check_same_thread': False},  # Required for SQLite in multithreaded environments
                echo=True
            )
            self.SessionLocal = sessionmaker(bind=self.engine)                  
            self.logger.info(f"Connected to SQLite database: {self.connection_string}")
            print("Connected to database")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            print("Failed to connect to database")
            raise
    
    async def disconnect(self) -> None:
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database disconnected")
    
    def execute_query(self, query: str) -> List[Any]:
        try:
            get_db_logger().info(f"Executing query: {query}")
            with self.SessionLocal() as session:
                result = session.execute(text(query))
                self.logger.info(f"Query executed: {query}")
                return result.fetchall()
        except Exception as e:
            self.logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def get_table_names(self) -> Dict[str, List[str]]:
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            # SQLite typically doesn't have schemas like MSSQL, so we return in a similar structure
            all_tables = {
                "base": tables
            }
            
            self.logger.info(f"Retrieved tables: {tables}")
            return all_tables
        except Exception as e:
            self.logger.error(f"Failed to get table names: {str(e)}")
            raise

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get comprehensive schema information for a specific table"""
        try:
            inspector = inspect(self.engine)
            self.logger.info(f"Getting schema for table: {table_name}")
            
            # Get detailed information
            columns = inspector.get_columns(table_name)
            foreign_keys = inspector.get_foreign_keys(table_name)
            primary_keys = get_primary_key_details(inspector, table_name)
            indexes = get_index_details(inspector, table_name)
            
            # Process column details
            column_details = [get_column_details(col) for col in columns]
            
            # Process foreign key details
            fk_details = [get_foreign_key_details(fk) for fk in foreign_keys]
            
            schema_info = {
                "table_name": table_name,
                "schema": None,  # SQLite doesn't have schemas like MSSQL
                "columns": column_details,
                "primary_keys": primary_keys,
                "foreign_keys": fk_details,
                "indexes": indexes,
            }
            
            self.logger.info(f"Successfully retrieved schema for {table_name}")
            return schema_info
        
        except Exception as e:
            self.logger.error(f"Error getting schema for {table_name}: {str(e)}")
            raise

    def get_schema_list(self, table_names: List[str]) -> List[Dict[str, Any]]:
        """Get schema information for multiple tables"""
        schema_list = []
        for table_name in table_names:
            try:
                schema_info = self.get_table_schema(table_name)
                schema_list.append(schema_info)
            except Exception as e:
                self.logger.error(f"Failed to get schema for {table_name}: {str(e)}")
                continue
        return schema_list