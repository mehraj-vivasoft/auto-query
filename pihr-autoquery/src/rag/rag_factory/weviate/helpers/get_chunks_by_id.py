from weaviate import WeaviateClient
from typing import List

def get_chunks_by_id(collection_name: str, ids: List[str], instance: WeaviateClient):    
    collection = instance.collections.get(collection_name)
    chunks = collection.query.fetch_objects_by_ids(ids=ids).objects    
    
    return chunks