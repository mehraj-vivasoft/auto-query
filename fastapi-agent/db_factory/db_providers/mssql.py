from contextlib import contextmanager
import os
from typing import Any, Dict, List
from sqlalchemy import create_engine, MetaData, inspect, text
from db_factory.db_interface import DatabaseInterface
from sqlalchemy.orm import sessionmaker
from utils.logging_config import get_app_logger, get_db_logger
from db.schema_helpers import get_column_details, get_foreign_key_details, get_index_details, get_primary_key_details

class MSSQLDatabaseInistance(DatabaseInterface):
    def __init__(self):
        self.connection_string = self.get_connection_string()
        self.engine = None
        self.logger = get_db_logger()
        self.SessionLocal = None
    
    def get_connection_string(self) -> str:
        """Get connection string from environment variables"""
        USER = os.getenv("DB_USER", "SA")
        PASSWORD = os.getenv("DB_PASSWORD", "Helloworld1?")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "1433")
        DB_NAME = os.getenv("DB_NAME", "huduri_production20240930")
        
        connection_string = f"mssql+pyodbc://{USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
        get_app_logger().info(f"Connection string from env: {connection_string}")
        
        return connection_string
    
    async def connect(self) -> None:
        try:
            self.engine = create_engine(self.connection_string, echo=True)
            self.SessionLocal = sessionmaker(bind=self.engine)                  
            self.logger.info(f"Connected to database: {self.connection_string}")
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
        # with self.session_scope() as session:
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
            schemas = inspector.get_schema_names()
            all_tables = {}
            self.logger.info("Retrieving tables from all schemas...")        

            baseTables = inspector.get_table_names()
            all_tables["base"] = baseTables

            for schema in schemas:
                # Get tables for the current schema
                tables = inspector.get_table_names(schema=schema)
                self.logger.info(f"Schema: {schema}, Tables: {tables}")

                # Store tables with schema as key
                all_tables[schema] = tables

            return all_tables
        except Exception as e:
            self.logger.error(f"Failed to get table names: {str(e)}")
            raise

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get comprehensive schema information for a specific table"""
        try:
            schema = None
            table = table_name
            
            # Handle schema.table format
            if "." in table_name:
                schema, table = table_name.split(".")
            else:
                table = table_name
            
            inspector = inspect(self.engine)
            self.logger.info(f"Getting schema for table: {table} in schema: {schema}")
            
            # Get detailed information
            columns = inspector.get_columns(table, schema=schema)
            foreign_keys = inspector.get_foreign_keys(table, schema=schema)
            primary_keys = get_primary_key_details(inspector, table, schema)
            indexes = get_index_details(inspector, table, schema)
            
            # Process column details
            column_details = [get_column_details(col) for col in columns]
            
            # Process foreign key details
            fk_details = [get_foreign_key_details(fk) for fk in foreign_keys]
            
            schema_info = {
                "table_name": table_name,
                "schema": schema,
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
    
    
# Usage example:
# def create_db_client() -> MSSQLDatabaseInistance:
#     db = MSSQLDatabaseInistance()
#     db.connect()
#     return db


# @contextmanager
    # def session_scope(self):
    #     """Provide a transactional scope around a series of operations"""
    #     if not self.session_maker:
    #         raise RuntimeError("Database not connected")
            
    #     session = self.session_maker()
    #     try:
    #         yield session
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()