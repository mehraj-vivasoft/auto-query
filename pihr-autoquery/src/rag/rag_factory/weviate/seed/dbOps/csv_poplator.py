import weaviate
import weaviate.classes as wvc
import os
from dotenv import load_dotenv
from weaviate.collections.classes.filters import FilterById

load_dotenv()

def create_connection():
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]  # Replace with your inference API key
        }
    )
    return client

def populate_collection(name, data_rows):
    client = create_connection()
    chunks = client.collections.get(name)    
    with chunks.batch.dynamic() as batch:
        for data_row in data_rows:
            print(">>>> Adding ", data_row)
            batch.add_object(
                properties=data_row,
            )
    print(len(chunks) , " Entries added in the ", name, " collection")
    client.close()
    
    return
    
def get_data_rows():
    import csv
    from typing import List, Dict    

    def import_data_from_csv(csv_file_path: str) -> List[Dict[str, str]]:
        print("Processing CSV file...")
        data_rows = []
        with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["tag"] = row["tag"].split(",") if "tag" in row and row["tag"] else []
                data_rows.append(row)
        print(len(data_rows), " rows processed")
        return data_rows
    
    csv_file_path = "/Users/codermehraj/Documents/codes/vivasoft/auto-query/pihr-autoquery/kb/PIHR_DATASET.csv"
    data_rows = import_data_from_csv(csv_file_path)
    
    return data_rows

if __name__ == "__main__":
    populate_collection("PIHR_DATASET", get_data_rows())