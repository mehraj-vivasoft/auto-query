import json
from core.table_finder.domain_selector import domain_selector
from core.table_finder.relevent_table_selector import relevent_table_selector

data = json.load(open("dataset/tables.json", "r"))

def read_and_iterate_json(file_path):
    # Read JSON data from file
    # with open(file_path, 'r') as file:
    #     data = json.load(file)
    
    # Iterate over the data
    for schema, tables in data.get("tables", {}).items():
        print(f"Schema: {schema}")
        for table in tables:
            print(f" - Table: {table}")
            
def get_domains(file_path):
    # Read JSON data from file
    # with open(file_path, 'r') as file:
    #     data = json.load(file)
        
    domains = []
    
    # Iterate over the data
    for domain, tables in data.get("tables", {}).items():
        domains.append(domain)
    
    return domains


def table_selector_from_query(query: str):
    """
    Find relevent tables from the table repository in dataset/tables.json format
    """
    domains = get_domains("dataset/tables.json")
    print("Available domains:", domains)
    
    selected_domains = domain_selector(query, domains)
    print("Selected domains:", selected_domains)
    
    selected_tables = []
    for domain in selected_domains:        
        prefix = domain + "." if domain != "base" else ""
        relevent_tables = relevent_table_selector(query, tables = [prefix + table for table in data["tables"][domain]])
        selected_tables += relevent_tables    
    
    print("Selected tables:", selected_tables)
    
    return selected_tables
    

if __name__ == "__main__":
    table_selector_from_query("Who are the most absent employees?")