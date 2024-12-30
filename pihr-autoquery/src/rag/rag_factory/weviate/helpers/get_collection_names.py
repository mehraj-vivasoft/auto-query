from weaviate.client import WeaviateClient

def get_collection_names(instance: WeaviateClient):    
    see_all_collections = instance.collections.list_all(simple=False)    
    collections = []
    for collection in see_all_collections:
        collections.append(collection)
    
    return collections