from weaviate import WeaviateClient
from typing import List, Dict

def post_chunk(collection_name: str, data_rows: List[Dict[str, str]], instance: WeaviateClient):
    chunks = instance.collections.get(collection_name)
    with chunks.batch.dynamic() as batch:
        for data_row in data_rows:            
            batch.add_object(
                properties=data_row,
            )
    
    print(len(chunks) , " Entries added in the ", collection_name, " collection")
    
    return