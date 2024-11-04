import os

from utils.logging_config import get_app_logger

def get_connection_string():
    """Get connection string from environment variables"""
    USER = os.getenv("DB_USER", "SA")
    PASSWORD = os.getenv("DB_PASSWORD", "Helloworld1?")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "1433")
    DB_NAME = os.getenv("DB_NAME", "huduri_production20240930")
    
    connection_string = f"mssql+pyodbc://{USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
    get_app_logger().info(f"Connection string from env: {connection_string}")
    
    return connection_string