import json
from core.table_finder.domain_selector import domain_selector
from core.table_finder.relevent_table_selector import relevent_table_selector
from utils.logging_config import get_app_logger, get_db_logger

TABLE_DATASET_PATH = "dataset/tables.json"

data = json.load(open(TABLE_DATASET_PATH, "r"))
get_db_logger().info("Loaded table dataset from ", TABLE_DATASET_PATH)
            
def get_domains():
    domains = []    
    for domain, tables in data.get("tables", {}).items():
        # TODO: Add more conditions to filter out irrelevant domains
        domains.append(domain)    
        
    return domains


def table_selector_from_query(query: str):
    """
    Find relevent tables from the table repository in dataset/tables.json format
    """
    domains = get_domains()
    get_db_logger().info("Available domains:", domains)
    
    selected_domains = domain_selector(query, domains)
    get_app_logger().info("Selected relevent domains:", selected_domains)
    
    selected_tables = []
    for domain in selected_domains:        
        prefix = domain + "." if domain != "base" else ""
        relevent_tables = relevent_table_selector(query, tables = [prefix + table for table in data["tables"][domain]])
        selected_tables += relevent_tables    
    
    get_app_logger().info("Selected relevent tables:", selected_tables)
    
    return selected_tables
    

# if __name__ == "__main__":
#     table_selector_from_query("Who are the most absent employees?")