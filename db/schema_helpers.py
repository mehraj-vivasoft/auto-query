from typing import Any, Dict, List

from sqlalchemy import inspect


def get_column_details(column: Dict[str, Any]) -> Dict[str, Any]:
    """Extract detailed column information"""
    return {
        "name": column["name"],
        "type": str(column["type"]),
        "nullable": column["nullable"],
        "default": str(column["default"]) if column["default"] is not None else None,
        "primary_key": column.get("primary_key", False),
        "autoincrement": column.get("autoincrement", False),
    }

def get_foreign_key_details(fk: Dict[str, Any]) -> Dict[str, Any]:
    """Extract detailed foreign key information"""
    return {
        "name": fk["name"],
        "constrained_columns": fk["constrained_columns"],
        "referred_schema": fk["referred_schema"],
        "referred_table": fk["referred_table"],
        "referred_columns": fk["referred_columns"],
    }

def get_primary_key_details(inspector: inspect, table: str, schema: str = None) -> List[str]:
    """Get primary key columns"""
    return inspector.get_pk_constraint(table, schema=schema).get('constrained_columns', [])

def get_index_details(inspector: inspect, table: str, schema: str = None) -> List[Dict[str, Any]]:
    """Get index information"""
    indexes = inspector.get_indexes(table, schema=schema)
    return [{
        "name": idx["name"],
        "columns": idx["column_names"],
        "unique": idx["unique"],
    } for idx in indexes]
