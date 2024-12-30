from weaviate import WeaviateClient


def get_top_k_chunks(collection_name: str, query: str, instance: WeaviateClient, k: int = 3):
    collection = instance.collections.get(collection_name)
    chunks = collection.query.near_text(query, limit=k).objects    
    
    return chunks