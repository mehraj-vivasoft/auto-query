from typing import Any, Dict, List

from db.database import get_table_schema
from utils.logging_config import get_db_logger


def get_schema_list(table_names: List[str]) -> List[Dict[str, Any]]:
    """Get schema information for multiple tables"""
    schema_list = []
    for table_name in table_names:
        try:
            schema_info = get_table_schema(table_name)
            schema_list.append(schema_info)
        except Exception as e:
            get_db_logger().error(f"Failed to get schema for {table_name}: {str(e)}")
            continue
    return schema_list