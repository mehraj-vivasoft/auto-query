from sqlalchemy import create_engine, MetaData, inspect
from databases import Database

from utils.logging_config import get_db_logger

DATABASE_URL = "postgresql://postgres:helloworld%3F@localhost:5432/school"

# SQLAlchemy engine and metadata
engine = create_engine(DATABASE_URL)
metadata = MetaData()

logger = get_db_logger()

# Async Database connection
database = Database(DATABASE_URL)

# Connection on startup
async def connect_db():    
    await database.connect()    
    logger.info("Database connected")

# Disconnection on shutdown
async def disconnect_db():
    await database.disconnect()
    logger.info("Database disconnected")

# Function to execute a query
async def execute_query(query: str):
    """Function to execute"""
    logger.info(f"Executing query: {query}")
    return await database.fetch_all(query=query)

# Function to get all table names
def get_table_names():
    inspector = inspect(engine)
    logger.info("Getting table names")
    return inspector.get_table_names()

# Function to get the schema of specific tables
def get_table_schema(table_name: str):
    inspector = inspect(engine)
    # logger.info(f"Getting schema for table: {table_name}")
    columnData = inspector.get_columns(table_name)
    fk_Data = inspector.get_foreign_keys(table_name)
    
    columns = []    
    for column in columnData:
        columns.append(
            {
                "name": column["name"],
                "type": column["type"],                
            }
        )
        
    foreign_keys = []
    for fk in fk_Data:
        foreign_keys.append(
            {
                "name": fk["name"],
                "constrained_columns": fk["constrained_columns"],
                "referred_columns": fk["referred_columns"],
                "referred_table": fk["referred_table"]
            }
        )
        
    schema = {
        "table_name": table_name,
        "columns": columns,
        "foreign_keys": foreign_keys
    }
    logger.info(f"Schema for table {table_name}: {schema}")
    return schema

def get_schema_list(table_names: list[str]):
    schema_list = []
    for table_name in table_names:
        schema_list.append(get_table_schema(table_name))
    return schema_list