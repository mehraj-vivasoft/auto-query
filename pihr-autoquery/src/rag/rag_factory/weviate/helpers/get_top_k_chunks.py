from weaviate import WeaviateClient


def get_top_k_chunks(collection_name: str, query: str, instance: WeaviateClient, k: int = 3, is_simple: bool = False):
    collection = instance.collections.get(collection_name)
    chunks = collection.query.near_text(query, limit=k).objects    
    
    if is_simple:
        chunks = [chunk.properties["document"] for chunk in chunks]
    
    return chunks