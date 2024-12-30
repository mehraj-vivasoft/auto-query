from weaviate.collections.classes.filters import FilterById
from weaviate.client import WeaviateClient
from typing import List

def delete_chunks_by_id(name : str, ids: List[str], instance: WeaviateClient):
    collection = instance.collections.get(name)
    collection.data.delete_many(
        where=FilterById().contains_any(ids)
    )
    instance.close()