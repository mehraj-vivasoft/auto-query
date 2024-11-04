from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Any
from db.connection_string import get_connection_string
from db.schema_helpers import get_column_details, get_foreign_key_details, get_index_details, get_primary_key_details
from utils.logging_config import get_db_logger

DATABASE_URL = get_connection_string()

metadata = MetaData()
logger = get_db_logger()

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

async def connect_db():
    logger.info(f"Connecting to database: {DATABASE_URL}")
    with engine.connect() as connection:
        logger.info("Database connected")

async def disconnect_db():
    engine.dispose()
    logger.info("Database disconnected")

def execute_query(query: str):
    """Function to execute SQL queries synchronously"""
    get_db_logger().info(f"Executing query: {query}")
    with SessionLocal() as session:
        result = session.execute(text(query))
        logger.info(f"Query executed: {query}")
        return result.fetchall()

def get_table_names() -> Dict[str, List[str]]:
    inspector = inspect(engine)

    # Get all schema names
    schemas = inspector.get_schema_names()
    all_tables = {}

    logger.info("Retrieving tables from all schemas...")        

    baseTables = inspector.get_table_names()
    all_tables["base"] = baseTables

    for schema in schemas:
        # Get tables for the current schema
        tables = inspector.get_table_names(schema=schema)
        logger.info(f"Schema: {schema}, Tables: {tables}")

        # Store tables with schema as key
        all_tables[schema] = tables

    return all_tables

def get_table_schema(table_name: str) -> Dict[str, Any]:
    """Get comprehensive schema information for a specific table"""
    try:
        schema = None
        table = table_name
        
        # Handle schema.table format
        if "." in table_name:
            schema, table = table_name.split(".")
        else:
            table = table_name
        
        inspector = inspect(engine)
        logger.info(f"Getting schema for table: {table} in schema: {schema}")
        
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
        
        logger.info(f"Successfully retrieved schema for {table_name}")
        return schema_info
    
    except Exception as e:
        logger.error(f"Error getting schema for {table_name}: {str(e)}")
        raise