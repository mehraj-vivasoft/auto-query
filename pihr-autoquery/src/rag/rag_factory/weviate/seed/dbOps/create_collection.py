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

def create_collection(name, properties):
    try:
        client = create_connection()
                
        if client.collections.exists(name):
            print(f"Collection {name} already exists")
        else:
            print(f"Creating collection {name}...")
            client.collections.create(
                name=name,
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
                generative_config=wvc.config.Configure.Generative.openai(),
                properties=properties
            )
            print(f"Collection {name} created")
            
    finally:
        client.close()

pihr_schema = [
    wvc.config.Property(
        name="document",
        data_type=wvc.config.DataType.TEXT,
    ),
    wvc.config.Property(
        name="document_type",
        data_type=wvc.config.DataType.TEXT,
    ),
    wvc.config.Property(
        name="tag",
        data_type=wvc.config.DataType.TEXT_ARRAY,
    )
]

if __name__ == "__main__":
    create_collection("PIHR_DATASET", pihr_schema)