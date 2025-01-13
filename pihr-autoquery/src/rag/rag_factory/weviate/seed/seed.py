# import weaviate
# import weaviate.classes.config as wvccm

# client = weaviate.connect_to_local()

# try:
#     # Note that you can use `client.collections.create_from_dict()` to create a collection from a v3-client-style JSON object
#     collection = client.collections.create(
#         name="TestCollection",
#         vectorizer_config=wvcc.Configure.Vectorizer.text2vec_cohere(),
#         generative_config=wvcc.Configure.Generative.cohere(),
#         properties=[
#             wvcc.Property(
#                 name="title",
#                 data_type=wvcc.DataType.TEXT
#             )
#         ]
#     )

# finally:
#     client.close()
    
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
        client.collections.create(
            name=name,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
            generative_config=wvc.config.Configure.Generative.openai(),
            properties=properties
        )
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

def populate_collection(name, data_rows):
    client = create_connection()
    chunks = client.collections.get(name)
    # for chunk in chunks.query.fetch_objects().objects:
    #     print(chunk)
    # print(len(data_rows))    
    with chunks.batch.dynamic() as batch:
        for data_row in data_rows:
            print("Adding ", data_row)
            batch.add_object(
                properties=data_row,
            )
    print(len(chunks) , " Entries added in the ", name, " collection")
    client.close()


def get_data_rows():
    import csv
    from typing import List, Dict    

    def import_data_from_csv(csv_file_path: str) -> List[Dict[str, str]]:
        data_rows = []
        with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["tag"] = row["tag"].split(",") if "tag" in row and row["tag"] else []
                data_rows.append(row)
        return data_rows
    
    csv_file_path = "src/rag/rag_factory/weviate/data.csv"
    data_rows = import_data_from_csv(csv_file_path)
    
    return data_rows

def get_all_collections():
    instance = create_connection()
    see_all_collections = instance.collections.list_all(simple=False)    
    collections = []
    for collection in see_all_collections:
        collections.append(collection)
    instance.close()
    
    return collections

def get_chunks(name):
    instance = create_connection()
    collection = instance.collections.get(name)
    chunks = collection.query.fetch_objects().objects        
    instance.close()
    
    return chunks

def get_chunk_by_id(name, ids):
    instance = create_connection()
    collection = instance.collections.get(name)
    chunks = collection.query.fetch_objects_by_ids(ids=ids).objects
    instance.close()
    
    return chunks

def delete_chunks_by_id(name, ids):
    instance = create_connection()
    collection = instance.collections.get(name)
    collection.data.delete_many(
        where=FilterById().contains_any(ids)
    )
    instance.close()

def get_top_k_chunks(collection_name: str, query: str, k: int = 3):
    instance = create_connection()
    collection = instance.collections.get(collection_name)
    chunks = collection.query.near_text(query, limit=k).objects
    instance.close()
    
    return chunks

if __name__ == "__main__":
    # create_collection("PIHR_DATASET", pihr_schema)

    # data_rows = get_data_rows()
    # populate_collection("PIHR_DATASET", data_rows)                

    # print(get_all_collections())
    
    # chunks = get_chunks("PIHR_DATASET")
    # print(len(chunks))
    
    # for chunk in chunks:
    #     print(chunk.properties)
    #     print(chunk.uuid)   
    
    
    # chunks = get_chunk_by_id("PIHR_DATASET", ["e74ac6f1-1318-4225-9cbe-fd0949eabcca", "64fe856c-cdaf-4696-95ae-39cdc6ae9e95"])
    
    # for chunk in chunks:
    #     print(chunk.properties)
    
    # delete_chunks_by_id("PIHR_DATASET", ["e74ac6f1-1318-4225-9cbe-fd0949eabcca", "64fe856c-cdaf-4696-95ae-39cdc6ae9e95"])

    # chunks = get_chunk_by_id("PIHR_DATASET", ["e74ac6f1-1318-4225-9cbe-fd0949eabcca", "64fe856c-cdaf-4696-95ae-39cdc6ae9e95"])
    
    # for chunk in chunks:
    #     print(chunk.properties)
    
    # chunks = get_top_k_chunks("PIHR_DATASET", "best hr software?", k=3)
    
    # for chunk in chunks:
    #     print(chunk.properties)
    #     print(chunk.uuid)
    
    print("Done")
    

# response = chunks.query.near_text(query="Who is Mehraj?", limit=3)
# print(response)

# https://weaviate.io/developers/weaviate/starter-guides/generative


# MAKE A CSV

