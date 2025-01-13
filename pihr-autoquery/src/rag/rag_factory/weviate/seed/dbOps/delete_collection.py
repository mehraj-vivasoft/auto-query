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

def delete_collection(collection_name):
    client = create_connection()
    
    if client is None:
        raise Exception("Weaviate is not running")        
    
    if client.collections.exists(collection_name):
        print(f"Collection {collection_name} exists")
        client.collections.delete(collection_name)
        print(f"Collection {collection_name} deleted")
    else:
        print(f"Collection {collection_name} does not exist")        
        
    client.close()    
    return

if __name__ == "__main__":
    delete_collection("PIHR_DATASET")